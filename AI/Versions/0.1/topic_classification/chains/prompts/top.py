from pydantic import BaseModel
from typing import List, Dict, Union
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class Feedback(BaseModel):
    assistant_name: str
    feedback: str


class Classification(BaseModel):
    abstract: str
    categories: List[str]
    reasoning: str
    confidence_score: float


class TopClassificationOutput(BaseModel):
    classifications: List[Classification]
    reflection: str
    feedback: List[Feedback]


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

sentence_analysis_json_example = """
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

json_structure = """
    "{
        "summary": "Detailed summary of the abstract",
        "reasoning": "Detailed reasoning for the summary",
        "feedback": {
            "methodologies_feedback": "Feedback for the methodologies assistant",
            "abstract_sentence_analysis_feedback": "Feedback for the abstract sentence analysis assistant"
        }
    }
"""

taxonomy_example = """
'Education': {
    'Education leadership and administration': [
        'Educational leadership and administration, general',
        "Higher education and community college administration",
        "Education leadership and administration nec"
    ],
    'Education research': [
        'Curriculum and instruction',
        'Educational assessment, evaluation, and research methods',
        'Educational/ instructional technology and media design',
        'Higher education evaluation and research',
        'Student counseling and personnel services',
        'Education research nec'
    ],
    "Teacher education": [
        "Adult, continuing, and workforce education and development",
        "Bilingual, multilingual, and multicultural education",
        "Mathematics teacher education",
        "Music teacher education",
        "Special education and teaching",
        "STEM educational methods",
        "Teacher education, science and engineering",
        "Teacher education, specific levels and methods",
        "Teacher education, specific subject areas"
    ],
    "Education, other": [
        "Education, general",
        "Education nec"
    ]
}
"""

top_classification_system_message = PromptTemplate(
    template="""
    You are an expert in topic classification of research paper abstracts. Your task is to classify the abstract into one or more of the categories which have been provided, you are only to classify the abstract into the categories which have been provided, you are not to make up your own categories. A correct classification is one that captures the main idea of the research while not being directly concerned with the specific methods used to conduct the research, the use of methods is only relevant if it is the main focus of the research or if it helps obtain more contextual understanding of the abstract. You can use methods to help obtain more contextual understanding of the abstract, but the abstract should not be classified based on the specific methods used to conduct the research.
    
    ## Categories you can classify the abstract into:
    {categories}
    
    In order to better assist you, several previous AI assistants have already processed the abstract in various ways. Here is a summary of the previous assistants and the data they have processed from the abstract:
    
    1. **Methodologies:**
    
    A former AI assistant has already extracted the methodologies from the abstract. It provides the identified methodologies. For each methodology it provides reasoning for why it identified it as a methodology, the passage(s) from the abstract which support its identification as a methodology, and a confidence score for its identification as a methodology. Here are the methodologies identified by the previous assistant:
        
    This is the format the output from the methdologies assistant is in:
    ```json
    {method_json_format}
    ```
    
    2. **Abstract Sentence Level Analysis:**
    
    Another previous assistant has already analyzed each sentence in the abstract. For each sentence is provides the identified meaning, the reasoning why they identified that meaning, and a confidence score for the identified meaning. It also provides an overall theme of the abstract and a detailed summary of the abstract.
    
    This is the format the output from the abstract sentence level analysis assistant is in, this format example is annotated so you can understand what each element is:
    ```json
    {sentence_analysis_json_example}
    ```
    
    3. **Abstract Summary:**
    
    Another previous assistant has already created a summary of the abstract. It provides the summary, the reasoning why it created the summary, and a confidence score for the summary.
    
    This is the format the output from the abstract summary assistant is in:
    ```json
    {json_structure}
    ```
    
    Output from the methodologies assistant:
    ```json
    {method_json_output}
    ```

    Output from the abstract sentence level analysis assistant:
    ```json
    {abstract_chain_output}
    ```
    
    Output from the abstract summary assistant:
    ```json
    {abstract_summary_output}
    ```

    ### Steps to Follow:
    1. Carefully read and understand the provided categories.
    2. Review the method extraction, sentence analysis, and abstract summary information.
    3. Classify the abstract into one of the provided categories. For each category you classify the abstract into provide a detailed reasoning for why you classified it into that category and a confidence score for your reasoning.
    4. Reflect on any parts you struggled with and explain why. This reflection should be detailed and specific to the task at hand.
    5. Provide feedback for the method extraction, sentence analysis, and abstract summary assistants.
        - Carefully review your process to identify what you did well and what you could improve on and based on what you could improve on identify if there is anything the abstract sentence level analysis assistant could improve on in their analysis of the abstract.
        - Provide this feedback in a structured format, for each assistant provide feedback seperately.
        - If you believe the analysis is correct and you have no feedback, simply provide "The analysis is correct and sufficient, I have no feedback at this time." and nothing else.

    ### Output Format:
    Your output should be a JSON object with the following structure:

    ```json
    {json_classification_format}
    ```
    
    IMPORTANT: You are only allowed to classify the abstract into the provided categories. Do NOT make up your own categories. When you give your output you are to label the categories you classified the abstract into as they appear in the categories list.
    
    Again, here is the list of categories you can classify the abstract into:
    {categories_list_2}
    
    
    
    IMPORTANT: Your classifications are focused on THE THEMES OF THE RESEARCH DESCRIBED IN THE ABSTRACT. The categories you are being provided are ACADEMIC RESEARCH CATEGORIES, this means something like education involves RESEARCH AROUND education, not just the art of education.
    
    For example, here is a full block item from the taxonomy:
    ```json
    {taxonomy_example}
    ```
    
    IMPORTANT: Do not classify based on the specific methods used to conduct the research, the use of methods is only relevant if it is the main focus of the research or if it helps obtain more contextual understanding of the abstract. The classifications should be representative of the core theme behind the research, as in what the research is doing but not how it is doing it.
    IMPORTANT: Your output should always be a JSON object following the provided structure, if you do not follow the provided structure and/ or do not provide a JSON object, you have failed.
    IMPORTANT: Do not include the markdown json code block notation in your response. Simply return the JSON object.
"""
)

top_classification_parser = PydanticOutputParser(
    pydantic_object=TopClassificationOutput
)
pytdantic_parser = PydanticOutputParser(pydantic_object=TopClassificationOutput)

from langchain.prompts import PromptTemplate

# topic_classication_prompt = PromptTemplate.from_template(
#     template="""
#     {top_classification_system_message}

#     Abstract:
#     {abstract}
#     """,
#     input_variables=[
#         "method_json_format",
#         "sentence_analysis_json_example",
#         "json_structure",
#         "categories",
#         "method_json_output",
#         "abstract_chain_output",
#         "abstract_summary_output",
#         "top_classification_system_message",
#         "abstract"
#     ]
# )


topic_system_prompt = SystemMessagePromptTemplate.from_template(
    top_classification_system_message.template
)
human_message_prompt = HumanMessagePromptTemplate.from_template(
    "## Original Abstract: \n{abstract}"
)
chat_prompt = ChatPromptTemplate.from_messages(
    [topic_system_prompt, human_message_prompt]
)
