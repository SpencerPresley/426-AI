from .abstract_base_chain import AbstractBaseChain
from langchain.schema.messages import SystemMessage, HumanMessage
from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableParallel
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from typing import List, Any, Union, Dict
import json


class ConcreteMethodExtractionChain(AbstractBaseChain):
    def __init__(self, llm_model: str, llm_temperature: float, **llm_kwargs):
        super().__init__(llm_model, llm_temperature, **llm_kwargs)
        self.system_message = SystemMessage(content="")  # Will be formatted later
        self.human_message = HumanMessage(content="## Abstract:  \n\n{abstract}")
        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message, self.human_message]
        )

    def create_chain(
        self, method_parser: Union[JsonOutputParser, PydanticOutputParser], **kwargs
    ) -> Runnable:
        if not isinstance(method_parser, (JsonOutputParser, PydanticOutputParser)):
            raise ValueError(
                "method_parser must be a JsonOutputParser or PydanticOutputParser"
            )

        return (
            RunnablePassthrough.assign(**kwargs)
            | RunnablePassthrough.assign(
                system_message=lambda x: self.system_message.format(**x),
                human_message=lambda x: self.human_message.format(
                    abstract=x["abstract"]
                ),
            )
            | self.chat_prompt
            | self.llm
            | method_parser
        )

    def run_chain(
        self,
        abstract: str,
        method_parser: Union[JsonOutputParser, PydanticOutputParser],
        index: int,
        **kwargs,
    ) -> Any:
        # Format the system message with the provided kwargs
        self.system_message.content = self.system_message.content.format(**kwargs)

        chain = self.create_chain(method_parser, **kwargs)

        # Prepare the input for the chain
        chain_input = {"abstract": abstract, **kwargs}

        # Run the chain
        result = chain.invoke(chain_input)

        # Save the output
        self.save_output(
            result, f"method_extraction_output_{self.model_type}_{index}.json"
        )

        return result

    def process_abstracts(
        self,
        abstracts: List[str],
        method_parser: Union[JsonOutputParser, PydanticOutputParser],
        system_message_content: str,
        start_index: int = 0,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        self.system_message.content = system_message_content

        results = []
        for i, abstract in enumerate(abstracts, start=start_index):
            try:
                result = self.run_chain(abstract, method_parser, i, **kwargs)
                results.append(result)
                print(json.dumps(result, indent=4))
            except Exception as e:
                print(f"Error processing abstract {i}: {type(e).__name__}: {str(e)}")
                import traceback

                traceback.print_exc()

        return results
