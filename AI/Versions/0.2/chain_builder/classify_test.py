import os
import json
import logging
from typing import List, Dict
from dotenv import load_dotenv
from utils.taxonomy_util import Taxonomy
from ChainBuilder import ChainManager
from prompts.top import TopClassificationOutput, method_json_format, sentence_analysis_json_example, json_structure, taxonomy_example, top_classification_system_message, human_message_prompt

class AbstractClassifier:
    def __init__(self, taxonomy, abstracts: List[str]):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.info("Initializing AbstractClassifier")
        self.taxonomy = taxonomy
        self.abstracts = abstracts
        self.logger.info("Initialized taxonomy and abstracts")
        self.chain_manager = self._initialize_chain_manager()
        self.logger.info("Initialized ChainManager")
        self.classification_results = {f"abstract_{i}": {} for i in range(len(abstracts))}
        self.logger.info("Initialized classification results")
        self.raw_classification_outputs = []

    def _initialize_chain_manager(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        return ChainManager(llm_model="gpt-4", api_key=api_key, llm_temperature=0.7)

    def create_classification_chain(self):
        self.chain_manager.add_chain_layer(
            system_prompt=top_classification_system_message,
            human_prompt=human_message_prompt,
            parser_type="pydantic",
            return_type="json",
            pydantic_output_model=TopClassificationOutput,
            ignore_output_passthrough_key_name_error=True
        )

    def classify_abstract(self, abstract: str, abstract_index: int, categories: List[str], level: str, method_json_output, abstract_chain_output, abstract_summary_output, parent_category=None):
        self.logger.info(f"Classifying abstract at {level} level")
        
        prompt_variables = {
            "abstract": abstract,
            "categories": categories,
            "method_json_output": json.dumps(method_json_output),
            "abstract_chain_output": json.dumps(abstract_chain_output),
            "abstract_summary_output": json.dumps(abstract_summary_output),
            "method_json_format": method_json_format,
            "sentence_analysis_json_example": sentence_analysis_json_example,
            "json_structure": json_structure,
            "json_classification_format": self.get_json_classification_form(),
            "categories_list_2": categories,
            "taxonomy_example": taxonomy_example,
        }
        
        try:
            classification_output = self.chain_manager.run(prompt_variables)
            self.logger.info(f"Raw classification output: {classification_output}")
            
            if isinstance(classification_output, str):
                classification_output = json.loads(classification_output)
            
            classification_output = TopClassificationOutput(**classification_output)
        except Exception as e:
            self.logger.error(f"Error during classification: {e}")
            self.logger.error(f"Raw output: {classification_output}")
            return {}

        self.raw_classification_outputs.append(classification_output.model_dump())

        classified_categories = self.extract_classified_categories(classification_output)
        self.logger.info(f"Classified categories at {level} level: {classified_categories}")

        result = {}
        for category in classified_categories:
            if level == "top":
                subcategories = self.taxonomy.get_mid_categories(category)
                next_level = "mid"
            elif level == "mid":
                subcategories = self.taxonomy.get_low_categories(parent_category, category)
                next_level = "low"
            else:
                subcategories = []
                next_level = None

            if subcategories:
                result[category] = self.classify_abstract(
                    abstract, abstract_index, subcategories, next_level,
                    method_json_output, abstract_chain_output, abstract_summary_output, category
                )
            else:
                result[category] = {}

        if level == "top":
            self.classification_results[f"abstract_{abstract_index}"] = result

        return result

    def extract_classified_categories(self, classification_output: TopClassificationOutput) -> List[str]:
        self.logger.info("Extracting classified categories")
        categories = [cat for classification in classification_output.classifications for cat in classification.categories]
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
                }
            ]
        }
        """

    def classify(self):
        self.create_classification_chain()
        for i, abstract in enumerate(self.abstracts):
            self.logger.info(f"Processing abstract {i+1} of {len(self.abstracts)}")
            method_json_output, abstract_chain_output, abstract_summary_output = self._get_json_outputs(i)
            self.classify_abstract(
                abstract, i, self.taxonomy.get_top_categories(), "top",
                method_json_output, abstract_chain_output, abstract_summary_output
            )
            self.logger.info(f"Completed classification for abstract {i+1}")
            self.logger.info(f"Current classification results: {self.classification_results}")

    def _get_json_outputs(self, index):
        self.logger.info(f"Getting JSON outputs for abstract {index}")
        base_path = os.path.dirname(os.path.abspath(__file__))
        \
        with open(os.path.join(base_path, f"outputs/method_extraction/method_json_output_{index}.json"), "r") as f:
            method_json_output = json.load(f)
        
        with open(os.path.join(base_path, f"outputs/sentence_analysis/abstract_chain_output_{index}.json"), "r") as f:
            abstract_chain_output = json.load(f)
        
        with open(os.path.join(base_path, f"outputs/summary/summary_chain_output_{index}.json"), "r") as f:
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
    from abstracts import abstracts

    try:
        taxonomy = Taxonomy()
        classifier = AbstractClassifier(taxonomy=taxonomy, abstracts=abstracts)
        logger.info("Classifier initialized")
        classifier.classify()
        logger.info("Classification completed")
        classifier.save_classification_results("outputs/classification_results.json")
        logger.info("Classification results saved")
        raw_classification_outputs = classifier.get_raw_classification_outputs()
        with open("outputs/raw_classification_outputs.json", "w") as f:
            json.dump(raw_classification_outputs, f, indent=4)
        logger.info("Raw classification outputs saved")
    except Exception as e:
        logger.error(f"Error during classification: {e}")