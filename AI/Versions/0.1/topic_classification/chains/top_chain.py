import json
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from .prompts.top import top_classification_parser, method_json_format, sentence_analysis_json_example, json_structure, TopClassificationOutput, chat_prompt, topic_system_prompt, human_message_prompt
from typing import List, Dict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    streaming=True,
    temperature=0.0,
)

def debug_format_human_message(x):
    # print(f"Debug: Formatting abstract: {x['abstract']['abstract']}")
    # input("Press Enter to continue...")
    return human_message_prompt.format(abstract=x["abstract"]["abstract"])

def create_top_classification_chain(*, categories, method_json_format, sentence_analysis_json_example, json_structure, method_json_output, abstract_chain_output, abstract_summary_output, abstract, chat_prompt, json_classification_form):
    # print(f"ABSTRACT IN CREATE TOP CLASSIFICATION CHAIN: {abstract}")
    # input("Press Enter to continue...")
    temp_categories = categories
    categories = ""
    for i, category in enumerate(temp_categories):
        categories += f"{str(i+1)}. {category}\n"
    
    categories = categories.replace('[', '').replace(']', '')
    # print(f"Categories: {categories}")
    # input("Press Enter to continue...")
    
    return (
        RunnablePassthrough.assign(
            topic_system_prompt=lambda x: topic_system_prompt.format(
                method_json_output=json.dumps(method_json_output, indent=4),
                abstract_chain_output=json.dumps(abstract_chain_output, indent=4),
                abstract_summary_output=json.dumps(abstract_summary_output, indent=4),
                json_classification_format=json_classification_form,
                json_structure=json_structure,
                method_json_format=method_json_format,
                sentence_analysis_json_example=sentence_analysis_json_example,
                categories=categories,
                categories_list_2=categories
            ),
            human_message_prompt=lambda x: human_message_prompt.format(abstract=abstract)
        )
        | chat_prompt
        | llm
        | top_classification_parser
    )

def print_top_classification_output(top_classification_output: TopClassificationOutput):
    print(json.dumps(top_classification_output, indent=4))

def get_json_outputs(i):
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/outputs/method_extraction/method_json_output_{i}.json", "r") as f:
        method_json_output = json.load(f)
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/outputs/sentence_analysis/abstract_chain_output_{i}.json", "r") as f:
        abstract_chain_output = json.load(f)
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/outputs/summary/summary_chain_output_{i}.json", "r") as f:
        abstract_summary_output = json.load(f)
    return method_json_output, abstract_chain_output, abstract_summary_output

def process_top_classification_chain(abstracts: List[str], taxonomy):
    categories = taxonomy.get_top_categories()
    # print(categories)
    # input("Press Enter to continue...")
    top_classification_outputs: List[TopClassificationOutput] = []
    
    json_classification_form = """
        {
            "classifications": [
                {
                    "abstract": "<abstract>",
                    "categories": [
                        "<first category you decided to classify the abstract into>",
                        "<second category you decided to classify the abstract into>"
                        ...
                    ],
                    "reasoning": "<reasoning for the classification>",
                    "confidence_score": <confidence score float value between 0 and 1>
                },
                {
                    "abstract": "<abstract>",
                    "categories": [
                        "<first category you decided to classify the abstract into>",
                        "<second category you decided to classify the abstract into>"
                        ...
                    ],
                    "reasoning": "<reasoning for the classification>",
                    "confidence_score": <confidence score float value between 0 and 1>
                }
            ],
            "reflection": "<reflection on parts you struggled with and why, and what could help alleviate that>",
            "feedback": [
                {
                    "assistant_name": "<name of the assistant you are providing feedback to>",
                    "feedback": "<feedback for the assistant>"
                },
                {
                    "assistant_name": "<name of the assistant you are providing feedback to>",
                    "feedback": "<feedback for the assistant>"
                },
                ...
            ]
        }
    """

    for i, abstract in enumerate(abstracts):
        method_json_output, abstract_chain_output, abstract_summary_output = get_json_outputs(i)
        
        # print(f"ABSTRACT: {abstract}")
        # input("Press Enter to continue...")
        
        try:
            top_classification_chain = create_top_classification_chain(categories=categories, method_json_format=method_json_format, sentence_analysis_json_example=sentence_analysis_json_example, json_structure=json_structure, method_json_output=method_json_output, abstract_chain_output=abstract_chain_output, abstract_summary_output=abstract_summary_output, abstract=abstract, chat_prompt=chat_prompt, json_classification_form=json_classification_form)
            top_classification_output = top_classification_chain.invoke({
                "abstract": abstract,
                "categories": categories,
                "method_json_output": method_json_output,
                "abstract_chain_output": abstract_chain_output,
                "abstract_summary_output": abstract_summary_output,
                "method_json_format": method_json_format,
                "sentence_analysis_json_example": sentence_analysis_json_example,
                "json_structure": json_structure,
                "json_classification_format": json_classification_form,
                "categories_list_2": categories
            })
            print(json.dumps(top_classification_output, indent=4))
            top_classification_outputs.append(top_classification_output)
            with open(f"{os.path.dirname(os.path.abspath(__file__))}/outputs/top_classification/top_classification_output_{i}.json", "w") as f:
                json.dump(top_classification_output, f, indent=4)
                
        except Exception as e:
            print(f"Error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()

    with open(f"{os.path.dirname(os.path.abspath(__file__))}/outputs/top_classification/top_classification_outputs.json", "w") as f:
        json.dump(top_classification_outputs, f, indent=4)

def process_top_classification_chain_map(abstracts: Dict[str, str], taxonomy):
    categories = taxonomy.get_top_categories()
    # print(categories)
    # input("Press Enter to continue...")
    top_classification_outputs: List[TopClassificationOutput] = {}
    
    json_classification_form = """
        {
            "classifications": [
                {
                    "abstract": "<abstract>",
                    "categories": [
                        "<first category you decided to classify the abstract into>",
                        "<second category you decided to classify the abstract into>"
                        ...
                    ],
                    "reasoning": "<reasoning for the classification>",
                    "confidence_score": <confidence score float value between 0 and 1>
                },
                {
                    "abstract": "<abstract>",
                    "categories": [
                        "<first category you decided to classify the abstract into>",
                        "<second category you decided to classify the abstract into>"
                        ...
                    ],
                    "reasoning": "<reasoning for the classification>",
                    "confidence_score": <confidence score float value between 0 and 1>
                }
            ],
            "reflection": "<reflection on parts you struggled with and why, and what could help alleviate that>",
            "feedback": [
                {
                    "assistant_name": "<name of the assistant you are providing feedback to>",
                    "feedback": "<feedback for the assistant>"
                },
                {
                    "assistant_name": "<name of the assistant you are providing feedback to>",
                    "feedback": "<feedback for the assistant>"
                },
                ...
            ]
        }
    """

    for i, (title, abstract) in enumerate(abstracts.items()):
        method_json_output, abstract_chain_output, abstract_summary_output = get_json_outputs(i)
        
        # print(f"ABSTRACT: {abstract}")
        # input("Press Enter to continue...")
        
        try:
            top_classification_chain = create_top_classification_chain(categories=categories, method_json_format=method_json_format, sentence_analysis_json_example=sentence_analysis_json_example, json_structure=json_structure, method_json_output=method_json_output, abstract_chain_output=abstract_chain_output, abstract_summary_output=abstract_summary_output, abstract=abstract, chat_prompt=chat_prompt, json_classification_form=json_classification_form)
            top_classification_output = top_classification_chain.invoke({
                "abstract": abstract,
                "categories": categories,
                "method_json_output": method_json_output,
                "abstract_chain_output": abstract_chain_output,
                "abstract_summary_output": abstract_summary_output,
                "method_json_format": method_json_format,
                "sentence_analysis_json_example": sentence_analysis_json_example,
                "json_structure": json_structure,
                "json_classification_format": json_classification_form,
                "categories_list_2": categories
            })
            print(json.dumps(top_classification_output, indent=4))
            top_classification_outputs [title] = top_classification_output
            # with open(f"{os.path.dirname(os.path.abspath(__file__))}/outputs/top_classification/top_classification_output_{i}.json", "w") as f:
            #     json.dump({title: top_classification_output}, f, indent=4)
                
        except Exception as e:
            print(f"Error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()

    with open("outputs/top_classification/top_classification_outputs.json", "w") as f:
        json.dump(top_classification_outputs, f, indent=4)