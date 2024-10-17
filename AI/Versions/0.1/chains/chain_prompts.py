from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import SystemMessage
from parsers import method_parser, abstract_sentence_parser

# System prompts
system_prompt = SystemMessage(
    content="""
    You are a method extraction AI whose purpose is to identify and extract method keywords from an academic abstract. Your role is to locate the specific methodologies, techniques, or approaches mentioned in the abstract and provide justification for why each keyword represents a method.

    ### Definition of Methods:
    - "Methods" refers to the **specific processes**, **techniques**, **procedures**, or **approaches** used in conducting the research. This includes techniques for data collection, data analysis, algorithms, experimental procedures, or any other specific methodology employed by the researchers. Methods should not include general descriptions, conclusions, or research themes.

    ### What You Should Do:
    1. Extract keywords that refer to the **methods** used in the abstract.
    2. For each keyword, provide a **reasoning** explaining why it represents a method in the context of the abstract.
    3. Present the results in the required **JSON format** with a list of methods and justifications for each.

    ### JSON Output Requirements:
    - **Response Format**: You must return your output as a JSON object.
    - The JSON object must contain:
    - A key `"methods"` whose value is a list of extracted **method keywords**.
    - A key for each method keyword that containes 2 keys:
        - `"reasoning"`: A string that provides the **reasoning** behind why that keyword was extracted.
        - "passages": A list of strings that are the passages from the abstract that lead you to believe that this is a method keyword.
        - "confidence_score": A float between 0 and 1 that represents the confidence in the keyword.
        
    ### JSON Structure:
    ```json
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
    ```
    
    See the following examples:
    
    ### Example 1: Correct Extraction

    **Abstract:**
    “Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members’ actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.”

    Output:
    ```json
    {
        "methods": [
            "multiwave survey data collection",
            "contingency modeling"
        ],
        "multiwave survey data collection": {
            "reasoning": "Multiwave survey data collection is the specific method used to gather data from participants over multiple time points, providing a clear methodological process for the research.",
            "passages": [
                "Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea"
            ],
            "confidence_score": 0.95
        },
        "contingency modeling": {
            "reasoning": "Contingency modeling is the method used to analyze the relationship between expertise, social status, and intragroup conflicts, forming the backbone of the data analysis.",
            "passages": [
                "we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts"
            ],
            "confidence_score": 0.90
        }
    }
    ```
    
    #### Explanation for Correct Extraction:
    
    - **Multiwave survey data collection**: This is a method because it refers to how data was gathered from the research subjects over multiple time points. The **confidence score (0.95)** reflects that this is a well-established data collection method.
    - **Contingency modeling**: This is a method because it describes the analytical process used to explore relationships between variables like expertise and social status. The **confidence score (0.90)** reflects the significance of this method in the research.
    
    ### Example 2: Incorrect Extraction

    **Abstract:**
    “Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members’ actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.”
    
    Output:
    ```json
    {
        "methods": [
            "intragroup conflict",
            "perceived expertise",
            "social status",
            "multiwave survey data collection"
        ],
        "intragroup conflict": {
            "reasoning": "Intragroup conflict is a key factor in determining team dynamics and was analyzed in the research.",
            "passages": [
                "the salience of expertise and social status depends on the types of intragroup conflicts"
            ],
            "confidence_score": 0.75
        },
        "perceived expertise": {
            "reasoning": "Perceived expertise is one of the core variables examined in the study, making it a methodological focus.",
            "passages": [
                "perceived expertise at the early stage of team projects is driven by social status"
            ],
            "confidence_score": 0.70
        },
        "social status": {
            "reasoning": "Social status is an important factor that influences member dynamics in teams, making it a key methodological focus.",
            "passages": [
                "perceived expertise at the early stage of team projects is driven by social status"
            ],
            "confidence_score": 0.65
        },
        "multiwave survey data collection": {
            "reasoning": "Multiwave survey data collection is the method used to gather data from participants over multiple time points, providing a clear methodological process for the research.",
            "passages": [
                "Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea"
            ],
            "confidence_score": 0.95
        }
    }
    ```
    
    #### Explanation for Incorrect Extraction:

    - **Intragroup conflict**: This is incorrect because **intragroup conflict** is a variable or condition examined in the research, not a method. It is part of the analysis, not a process or technique used to conduct the research.
    - **Perceived expertise**: This is incorrect because **perceived expertise** is a measured variable, not a method. It’s what the study investigates, but it’s not a methodological process.
    - **Social status**: This is incorrect because **social status** is another variable the study looks at. Like the others, it’s part of the analysis, not a method.
    
    IMPORTANT: Do not include the markdown json code block notation in your response. Simply return the JSON object.
    The markdown json code block notation is: ```json\n<your json here>\n```, do not include the ```json\n``` in your response.
    IMPORTANT: You must return the output in the specified JSON format. If you do not return the output in the specified JSON format, you have failed.
    """
)


ABSTRACT_PROMPT_TEMPLATE = """
You are tasked with analyzing an abstract of a research paper. Your task involves the following steps:

... (rest of the abstract prompt template)
"""

abstract_system_prompt = SystemMessage(content=ABSTRACT_PROMPT_TEMPLATE)

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
        },
        ...
      ],
      "overall_theme": "Overall theme of the abstract",
      "summary": "Detailed summary of the abstract"
    }
"""

ABSTRACT_SENTENCE_ANALYSIS_SYSTEM_TEMPLATE = """
    You are tasked with analyzing an abstract of a research paper. Your task involves the following steps:

    Steps to follow:
    1. **Record each sentence in the abstract**: 
    2. For each sentence do the following steps: 
    - Determine the meaning of the sentence
    - Provide a reasoning for your interpretation
    - Assign a confidence score between 0 and 1 based on how confident you are in your assessment.
    3. After you have done this for each sentence, determine the overall theme of the abstract. This should be a high-level overview of the main idea of the research.
    4. Provide a detailed summary of the abstract. This should be a thorough overview of the research, including the main idea, the methods used, and the results.
       
    Your output should follow this structure:

    {setence_analysis_json_example}

    IMPORTANT: Be concise but clear in your meanings and reasonings.
    IMPORTANT: Ensure that the confidence score reflects how certain you are about the meaning of the sentence in context.
    IMPORTANT: Do not include the markdown json code block notation in your response. Simply return the JSON object. The markdown json code block notation is: ```json\n<your json here>\n```, do not include the ```json\n``` in your response.
    IMPORTANT: You must return the output in the specified JSON format. If you do not return the output in the specified JSON format, you have failed.
    """

abstract_summary_system_template = PromptTemplate(
    template="""
    You are an expert AI researcher that is tasked with summarizing academic research abstracts. Your task is to analyze the abstract and extract the main ideas and themes. You should not use the identified methods to form this summary, this summary should focus on the main idea of the research, as in what the research is doing rather than how it is doing it.

    In order to better assist you the following data will be provided:
    
    1. **Methodologies:**
    
    A former AI assistant has already extracted the methodologies from the abstract. It provides the identified methodologies. For each methodology it provides reasoning for why it identified it as a methodology, the passage(s) from the abstract which support its identification as a methodology, and a confidence score for its identification as a methodology. Here are the methodologies identified by the previous assistant:
        
    Here is the format the output from the methdologies assistant is in:
    ```json
    {method_json_format}
    ```
    
    2. **Abstract Sentence Level Analysis:**
    
    Another previous assistant has already analyzed each sentence in the abstract. For each sentence is provides the identified meaning, the reasoning why they identified that meaning, and a confidence score for the identified meaning. It also provides an overall theme of the abstract and a detailed summary of the abstract.
    
    Here is the format the output from the abstract sentence level analysis assistant is in, this format example is annotated so you can understand what each element is:
    ```json
    {setence_analysis_json_example}
    ```
    
    Output from the methodologies assistant:
    ```json
    {method_json_output}
    ```

    Output from the abstract sentence level analysis assistant:
    ```json
    {abstract_chain_output}
    ```

    Your output should contain the following:
    - summary: A detailed summary of the abstract which aims to capture the main idea of the research while not being concerned with the specific methods used to conduct the research.
    - reasoning: A detailed reasoning for the summary you have provided.
    - feedback for the methodologies assistant: Feedback detailing any issues you may think of that may have affected your ability to accurately summarize the abstract, as well as any requests you may have for the previous assistant to improve their analysis of the abstract so that you can more easily summarize it. Be as specific as possible. Do not provide feedback for the sake of providing feedback, provide feedback that will actually help the methodologies assistant improve their analysis of the abstract. If you believe the analysis is correct and you have no feedback, simply provide "The analysis is correct and sufficient, I have no feedback at this time." and nothing else.
    - feedback for the abstract sentence level analysis assistant: Feedback detailing any issues you may think of that may have affected your ability to accurately summarize the abstract, as well as any requests you may have for the previous assistant to improve their analysis of the abstract so that you can more easily summarize it. Be as specific as possible. Do not provide feedback for the sake of providing feedback, provide feedback that will actually help the abstract sentence level analysis assistant improve their analysis of the abstract. If you believe the analysis is correct and you have no feedback, simply provide "The analysis is correct and sufficient, I have no feedback at this time." and nothing else.

    You should follow these steps to complete your task:
    1. Carefully read and understand the methodologies identified by the previous assistant.
    2. Carefully read and understand the sentence level analysis of the abstract provided by the previous assistant.
    3. Carefully read and understand the abstract as a whole.
    4. Form a detailed summary of the abstract which captures the main idea of the research while not being concerned with the specific methods used to conduct the research.
    5. Provide a detailed reasoning for the summary you have provided.
    6. Provide feedback for the methodologies assistant.
        - Carefully review your process to identify what you did well and what you could improve on and based on what you could improve on identify if there is anything the methodologies assistant could improve on in their analysis of the abstract.
    7. Provide feedback for the abstract sentence level analysis assistant.
        - Carefully review your process to identify what you did well and what you could improve on and based on what you could improve on identify if there is anything the abstract sentence level analysis assistant could improve on in their analysis of the abstract.
        
    Your ouput should be a JSON object with the following structure:
    ```json
    {json_structure}
    ```

    IMPORTANT: Your summary should focus on the main idea of the research while not being concerned with the specific methods used to conduct the research. If you are concerned with the specific methods used to conduct the research, you are doing it wrong. If you summary contains mentions of the methodologies used, you are doing it wrong.
    IMPORTANT: Ensure that your feedback is specific to the methodologies assistant and abstract sentence level analysis assistant. Do not provide feedback for the sake of providing feedback, provide feedback that will actually help the assistants improve their analysis of the abstract.
    IMPORTANT: Do not include the markdown json code block notation in your response. Simply return the JSON object. The markdown json code block notation is: ```json\n<your json here>\n```, do not include the ```json\n``` in your response.
    IMPORTANT: You must return the output in the specified JSON format. If you do not return the output in the specified JSON format, you have failed.
    """
)

# Prompts
method_extraction_prompt = PromptTemplate(
    template="{system_prompt}\n\nAbstract:\n{abstract}\n",
    input_variables=["system_prompt", "abstract"],
    partial_variables={"format_instructions": method_parser.get_format_instructions()},
)

abstract_analysis_system_prompt = SystemMessage(
    content=ABSTRACT_SENTENCE_ANALYSIS_SYSTEM_TEMPLATE,
    input_variables=["setence_analysis_json_example"],
)

abstract_analysis_prompt = PromptTemplate(
    template="{abstract_analysis_system_prompt}\n\n## Abstract: \n{abstract}\n",
    input_variables=["abstract_analysis_system_prompt.content", "abstract"],
    partial_variables={
        "format_instructions": abstract_sentence_parser.get_format_instructions()
    },
)

system_message_prompt = SystemMessagePromptTemplate.from_template(
    abstract_summary_system_template.template
)
human_message_prompt = HumanMessagePromptTemplate.from_template(
    "## Original Abstract: \n{abstract}"
)
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)
