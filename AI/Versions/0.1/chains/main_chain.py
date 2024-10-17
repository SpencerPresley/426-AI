import json
from typing import List
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from .chain_prompts import (
    chat_prompt,
    abstract_summary_system_template,
    system_prompt,
    abstract_analysis_system_prompt,
)
from .util_chains import llm, method_chain, abstract_chain
from parsers import summary_parser
from .utils import json_print_to_file


def create_summary_chain(
    json_structure, method_json_format, setence_analysis_json_example, i
):
    return (
        RunnableParallel(
            {
                "method_json_output": method_chain,
                "abstract_chain_output": abstract_chain,
                "abstract": RunnablePassthrough.assign(
                    abstract=lambda x: x["abstract"]
                ),
                "json_structure": RunnablePassthrough.assign(
                    json_structure=lambda x: json_structure
                ),
                "method_json_format": RunnablePassthrough.assign(
                    method_json_format=lambda x: method_json_format
                ),
                "setence_analysis_json_example": RunnablePassthrough.assign(
                    setence_analysis_json_example=lambda x: setence_analysis_json_example
                ),
            }
        )
        | RunnablePassthrough.assign(
            abstract_summary_system_prompt=lambda x: abstract_summary_system_template.format(
                method_json_output=json.dumps(x["method_json_output"], indent=4),
                abstract_chain_output=json.dumps(x["abstract_chain_output"], indent=4),
                setence_analysis_json_example=setence_analysis_json_example,
                method_json_format=method_json_format,
                json_structure=json_structure,
            ),
        )
        | RunnablePassthrough.assign(
            method_json_output=lambda x: (
                json_print_to_file(f"method_json_output_{i}", x["method_json_output"]),
                x["method_json_output"],
            )[1],
            abstract_chain_output=lambda x: (
                json_print_to_file(
                    f"abstract_chain_output_{i}", x["abstract_chain_output"]
                ),
                x["abstract_chain_output"],
            )[1],
        )
        | chat_prompt
        | llm
        | summary_parser
    )


def process_abstracts(
    abstracts: List[str],
    json_structure: str,
    method_json_format: str,
    setence_analysis_json_example: str,
    index: int = 0
):

    for i, abstract in enumerate(abstracts):
        try:
            summary_chain = create_summary_chain(
                json_structure,
                method_json_format,
                setence_analysis_json_example,
                i=index + i,
            )
            summary_chain_output = summary_chain.invoke(
                {
                    "abstract": abstract,
                    "system_prompt": system_prompt.content,
                    "abstract_analysis_system_prompt": abstract_analysis_system_prompt.content,
                    "setence_analysis_json_example": setence_analysis_json_example,
                    "method_json_format": method_json_format,
                    "json_structure": json_structure,
                }
            )
            print(json.dumps(summary_chain_output, indent=4))

            json_print_to_file(
                f"summary_chain_output_{index + i}", summary_chain_output
            )
        except Exception as e:
            print(f"Error: {type(e).__name__}: {str(e)}")
            import traceback

            traceback.print_exc()
