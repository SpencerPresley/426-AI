import json
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from .prompts.top import (
    top_classification_parser,
    method_json_format,
    sentence_analysis_json_example,
    json_structure,
    TopClassificationOutput,
    chat_prompt,
    topic_system_prompt,
    human_message_prompt,
    taxonomy_example,
)
from typing import List
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


from langchain_google_genai import (
    GoogleGenerativeAI,
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

print("Setting up classification environment...")
print("Loading environment variables...")
load_dotenv()
print("Environment variables loaded.")
google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

print("Initializing LLM...")
llm = GoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=google_api_key,
    streaming=True
)
print("LLM initialized.")

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     openai_api_key=os.getenv("OPENAI_API_KEY"),
#     streaming=True,
#     temperature=0.0,
# )


def debug_format_human_message(x):
    # print(f"Debug: Formatting abstract: {x['abstract']['abstract']}")
    # input("Press Enter to continue...")
    return human_message_prompt.format(abstract=x["abstract"]["abstract"])


def create_top_classification_chain(
    *,
    categories,
    method_json_format,
    sentence_analysis_json_example,
    json_structure,
    method_json_output,
    abstract_chain_output,
    abstract_summary_output,
    abstract,
    chat_prompt,
    json_classification_form,
    taxonomy_example,
):
    # print(f"ABSTRACT IN CREATE TOP CLASSIFICATION CHAIN: {abstract}")
    # input("Press Enter to continue...")
    temp_categories = categories
    categories = ""
    for i, category in enumerate(temp_categories):
        categories += f"{str(i+1)}. {category}\n"

    categories = categories.replace("[", "").replace("]", "")
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
                categories_list_2=categories,
                taxonomy_example=taxonomy_example,
            ),
            human_message_prompt=lambda x: human_message_prompt.format(
                abstract=abstract
            ),
        )
        | chat_prompt
        | llm
        | top_classification_parser
    )


def print_top_classification_output(top_classification_output: TopClassificationOutput):
    print(json.dumps(top_classification_output, indent=4))


def get_json_outputs(i):
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/outputs/method_extraction/method_json_output_{i}.json",
        "r",
    ) as f:
        method_json_output = json.load(f)
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/outputs/sentence_analysis/abstract_chain_output_{i}.json",
        "r",
    ) as f:
        abstract_chain_output = json.load(f)
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/outputs/summary/summary_chain_output_{i}.json",
        "r",
    ) as f:
        abstract_summary_output = json.load(f)
    return method_json_output, abstract_chain_output, abstract_summary_output


def process_top_classification_chain(abstracts: List[str], taxonomy, parent_category=None):
    print("Processing top classification chain...")
    print("Getting top categories...")
    categories = taxonomy.get_top_categories()
    # print(categories)
    # input("Press Enter to continue...")
    top_classification_outputs: List[TopClassificationOutput] = []
    print("Top categories retrieved.")
    print("Creating json classification form...")
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
    print("Json classification form created.")

    abstract_cat_dict = {abstract_i: {'top': None, 'mid': None, 'low': None} for abstract_i in range(len(abstracts))}
    
    print("Processing top classification chain...")
    for i, abstract in enumerate(abstracts):
        print(f"Processing abstract {i+1} of {len(abstracts)}...")
        print("Getting json outputs...")
        method_json_output, abstract_chain_output, abstract_summary_output = (
            get_json_outputs(i)
        )
        print("Json outputs retrieved.")
        # print(f"ABSTRACT: {abstract}")
        # input("Press Enter to continue...")

        print("Creating top classification chain...")
        try:
            low_level_classified = False
            while not low_level_classified:
                level_for_file = 'top_classification_output_'
                top_classification_chain = create_top_classification_chain(
                    categories=categories,
                    method_json_format=method_json_format,
                    sentence_analysis_json_example=sentence_analysis_json_example,
                    json_structure=json_structure,
                    method_json_output=method_json_output,
                    abstract_chain_output=abstract_chain_output,
                    abstract_summary_output=abstract_summary_output,
                    abstract=abstract,
                    chat_prompt=chat_prompt,
                    json_classification_form=json_classification_form,
                )
                print("Top classification chain created.")
                print("Invoking top classification chain...")
                top_classification_output = top_classification_chain.invoke(
                    {
                        "abstract": abstract,
                        "categories": categories,
                        "method_json_output": method_json_output,
                        "abstract_chain_output": abstract_chain_output,
                        "abstract_summary_output": abstract_summary_output,
                        "method_json_format": method_json_format,
                        "sentence_analysis_json_example": sentence_analysis_json_example,
                        "json_structure": json_structure,
                        "json_classification_format": json_classification_form,
                        "categories_list_2": categories,
                        "taxonomy_example": taxonomy_example,
                    }
                )
                print("Top classification chain invoked.")
                # print(json.dumps(top_classification_output, indent=4))
                top_classification_outputs.append(top_classification_output)
                print("Top classification output appended to list of results.")
                print("Writing to file...")
                with open(
                    f"{os.path.dirname(os.path.abspath(__file__))}/outputs/top_classification/{level_for_file}{i}.json",
                    "w",
                ) as f:
                    print(
                        f"Writing to file: {f} at path {os.path.dirname(os.path.abspath(__file__))}/outputs/top_classification/{level_for_file}{i}.json"
                    )
                    json.dump(top_classification_output, f, indent=4)
                print("File written.")
            
            print("Accessing top categories for each classification...")

                
        except Exception as e:
            print(f"Error: {type(e).__name__}: {str(e)}")
            import traceback

            traceback.print_exc()

    print("Writing top classification outputs to file...")
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/outputs/top_classification/top_classification_outputs.json",
        "w",
    ) as f:
        json.dump(top_classification_outputs, f, indent=4)
    print("Top classification outputs written to file.")