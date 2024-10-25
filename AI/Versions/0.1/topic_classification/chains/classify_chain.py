from typing import List, Dict
from prompts.top import (
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
from langchain_openai import ChatOpenAI
import os
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
import json
import logging
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.taxonomy_util import Taxonomy


class AbstractClassifier:
    def __init__(self, taxonomy, abstracts: List[str]):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.info("Initializing AbstractClassifier")
        self.taxonomy = taxonomy
        self.abstracts = abstracts
        self.logger.info("Initialized taxonomy and abstracts")
        self.llm = self._initialize_llm()
        self.logger.info("Initialized LLM")
        self.classification_results = {}
        for i in range(len(abstracts)):
            self.classification_results[f"abstract_{i}"] = {}
        self.logger.info("Initialized classification results")
        self.logger.info(self.classification_results)
        # input("Press Enter to continue...")
        self.raw_classification_outputs = []
        self.chat_prompt = chat_prompt
        self.top_classification_parser = top_classification_parser
        self.current_abstract_index = 0

    def _initialize_llm(self):
        self.logger.info("Loading environment variables")
        load_dotenv()
        self.logger.info("Environment variables loaded")
        self.logger.info("Initializing LLM")
        return ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    def create_classification_chain(self):
        return (
            RunnablePassthrough()
            | self.chat_prompt
            | self.llm
            | self.top_classification_parser
        )

    def classify_abstract(
        self,
        *,
        abstract: str,
        abstract_index: int,
        categories: List[str],
        level: str,
        method_json_output,
        abstract_chain_output,
        abstract_summary_output,
        parent_category=None,
    ):
        self.logger.info(f"Classifying abstract at {level} level")
        json_classification_form = self.get_json_classification_form()
        classification_chain = self.create_classification_chain()

        classification_output = classification_chain.invoke(
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

        self.raw_classification_outputs.append(classification_output.model_dump())

        classified_categories = self.extract_classified_categories(
            classification_output
        )
        self.logger.info(
            f"Classified categories at {level} level: {classified_categories}"
        )

        result = {}
        for category in classified_categories:
            if level == "top":
                subcategories = self.taxonomy.get_mid_categories(category)
                next_level = "mid"
            elif level == "mid":
                subcategories = self.taxonomy.get_low_categories(
                    parent_category, category
                )
                next_level = "low"
            else:
                subcategories = []
                next_level = None

            if subcategories:
                result[category] = self.classify_abstract(
                    abstract=abstract,
                    abstract_index=abstract_index,
                    categories=subcategories,
                    level=next_level,
                    method_json_output=method_json_output,
                    abstract_chain_output=abstract_chain_output,
                    abstract_summary_output=abstract_summary_output,
                    parent_category=category,
                )
            else:
                result[category] = {}

        if level == "top":
            self.classification_results[f"abstract_{abstract_index}"] = result

        return result

    def extract_classified_categories(
        self, classification_output: TopClassificationOutput
    ) -> List[str]:
        self.logger.info("Extracting classified categories")
        categories = []
        for classification in classification_output.classifications:
            categories.extend(
                classification.categories
            )  # extend used instead of append to have a flat list
        self.logger.info("Extracted classified categories")
        return categories

    def get_json_classification_form(self) -> str:
        self.logger.info("Returning JSON classification form")
        return """
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

    def classify(self):
        for i, abstract in enumerate(self.abstracts):
            self.logger.info(f"Processing abstract {i+1} of {len(self.abstracts)}")
            method_json_output, abstract_chain_output, abstract_summary_output = (
                self._get_json_outputs(i)
            )
            self.classify_abstract(
                abstract=abstract,
                abstract_index=i,
                categories=self.taxonomy.get_top_categories(),
                level="top",
                method_json_output=method_json_output,
                abstract_chain_output=abstract_chain_output,
                abstract_summary_output=abstract_summary_output,
            )
            self.logger.info(f"Completed classification for abstract {i+1}")
            self.logger.info(
                f"Current classification results: {self.classification_results}"
            )
            # input("Press Enter to continue to the next abstract...")

    def _get_json_outputs(self, index):
        self.logger.info(f"Getting JSON outputs for abstract {index}")
        method_json_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"outputs/method_extraction/method_json_output_{index}.json",
        )
        with open(method_json_path, "r") as f:
            method_json_output = json.load(f)

        abstract_chain_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"outputs/sentence_analysis/abstract_chain_output_{index}.json",
        )
        with open(abstract_chain_path, "r") as f:
            abstract_chain_output = json.load(f)

        abstract_summary_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"outputs/summary/summary_chain_output_{index}.json",
        )
        with open(abstract_summary_path, "r") as f:
            abstract_summary_output = json.load(f)

        self.logger.info(f"Got JSON outputs for abstract {index}")
        return method_json_output, abstract_chain_output, abstract_summary_output

    def save_classification_results(self, output_path: str):
        self.logger.info("Saving classification results")
        with open(output_path, "w") as f:
            json.dump(self.classification_results, f, indent=4)

    def get_raw_classification_outputs(self):
        self.logger.info("Getting raw classification outputs")
        return self.raw_classification_outputs


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting classification process")
    from abstract import abstracts

    try:
        taxonomy = Taxonomy()
        classifier = AbstractClassifier(taxonomy=taxonomy, abstracts=abstracts)
        logger.info("Classifier initialized")
        classifier.classify()
        logger.info("Classification completed")
        classifier.save_classification_results("outputs/classification_results.json")
        logger.info("Classification results saved")
        raw_classification_outputs = classifier.get_raw_classification_outputs()
        with open(
            "outputs/raw_classification_outputs.json", "w"
        ) as f:
            json.dump(raw_classification_outputs, f, indent=4)
        logger.info("Raw classification outputs saved")
    except Exception as e:
        logger.error(f"Error during classification: {e}")
