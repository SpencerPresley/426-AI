from chains.main_chain import process_abstracts
import os
import json
abstracts = []

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
abstracts_file = os.path.join(data_dir, "ALL_ABSTRACTS.json")
with open(abstracts_file, "r") as f:
    raw_abstracts = json.load(f)["abstracts"]

abstracts = []
for abstract in raw_abstracts:
    if abstract == "" or abstract == None:
        continue
    abstracts.append(abstract)

print(abstracts[13])
input("Press Enter to continue...")

print(len(abstracts))
# print(len(abstracts))
print(f"abstract left = {len(abstracts) - 296}")
abstracts = abstracts[296:]
# print(abstracts)
print(len(abstracts))




json_structure = """
    {
        "summary": "Detailed summary of the abstract",
        "reasoning": "Detailed reasoning for the summary",
        "feedback": {
            "methodologies_feedback": "Feedback for the methodologies assistant",
            "abstract_sentence_analysis_feedback": "Feedback for the abstract sentence analysis assistant"
        }
    }
"""

method_json_format = """
    {
        "methods": [
            "<method_keyword_1>",
            "<method_keyword_2>"
        ],
        "<method_keyword_1>": {
            "reasoning": "<explain why this is a method keyword>",
            "passages": ["<list of passages from the abstract which lead you to believe this is a method keyword>"],
            "confidence_score": <confidence score float value between 0 and 1>
        },
        "<method_keyword_2>": {
            "reasoning": "<explain why this is a method keyword>"
            "passages": ["<list of passages from the abstract which lead you to believe this is a method keyword>"],
            "confidence_score": <confidence score float value between 0 and 1>
        }
    }
"""

setence_analysis_json_example = """
    {
      "sentence_details": [
        {
          "sentence": "Original sentence 1",
          "meaning": "Meaning of the sentence.",
          "reasoning": "Why this is the meaning of the sentence.",
          "confidence_score": Confidence score (0.0 - 1.0)
        },
        {
          "sentence": "Original sentence 2",
          "meaning": "Meaning of the sentence.",
          "reasoning": "Why this is the meaning of the sentence.",
          "confidence_score": Confidence score (0.0 - 1.0)
        }
      ],
      "overall_theme": "Overall theme of the abstract",
      "summary": "Detailed summary of the abstract"
    }
"""

process_abstracts(abstracts, json_structure, method_json_format, setence_analysis_json_example, index=296)