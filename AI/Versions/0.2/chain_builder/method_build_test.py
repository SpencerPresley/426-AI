from ChainBuilder import ChainManager

from dotenv import load_dotenv

from langchain_core.output_parsers import JsonOutputParser
from typing import List
from pydantic import BaseModel
from abstracts import abstracts
import os
import json

load_dotenv()

class MethodDetail(BaseModel):
    reasoning: str
    passages: List[str]
    confidence_score: float

class MethodOutput(BaseModel):
    methods: List[str]
    method_details: dict[str, MethodDetail]

method_json_structure = """
{
    "methods": [
        "<method_keyword_1>",
        "<method_keyword_2>"
    ],
    "method_details": {
        "<method_keyword_1>": {
            "reasoning": "<explain why this is a method keyword>",
            "passages": [
                "<list of passages from the abstract which lead you to believe this is a method keyword>"
            ],
            "confidence_score": <confidence score float value between 0 and 1>
        },
        "<method_keyword_2>": {
            "reasoning": "<explain why this is a method keyword>",
            "passages": [
                "<list of passages from the abstract which lead you to believe this is a method keyword>"
            ],
            "confidence_score": <confidence score float value between 0 and 1>
        }
    }
}
"""

method_correct_example_json = """
{
    "methods": [
        "multiwave survey data collection",
        "contingency modeling"
    ],
    "method_details": {
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
}
"""

method_incorrect_example_json = """    
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
"""

method_system_prompt = """
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
    {method_json_structure}
    ```
    
    See the following examples:
    
    ### Example 1: Correct Extraction

    **Abstract:**
    “Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members’ actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.”

    Output:
    ```json
    {method_correct_example_json}
    ```
    
    #### Explanation for Correct Extraction:
    
    - **Multiwave survey data collection**: This is a method because it refers to how data was gathered from the research subjects over multiple time points. The **confidence score (0.95)** reflects that this is a well-established data collection method.
    - **Contingency modeling**: This is a method because it describes the analytical process used to explore relationships between variables like expertise and social status. The **confidence score (0.90)** reflects the significance of this method in the research.
    
    ### Example 2: Incorrect Extraction

    **Abstract:**
    “Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members’ actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.”
    
    Output:
    ```json
    {method_incorrect_example_json}
    ```
    
    #### Explanation for Incorrect Extraction:

    - **Intragroup conflict**: This is incorrect because **intragroup conflict** is a variable or condition examined in the research, not a method. It is part of the analysis, not a process or technique used to conduct the research.
    - **Perceived expertise**: This is incorrect because **perceived expertise** is a measured variable, not a method. It’s what the study investigates, but it’s not a methodological process.
    - **Social status**: This is incorrect because **social status** is another variable the study looks at. Like the others, it’s part of the analysis, not a method.
    
    IMPORTANT: Do not include the markdown json code block notation in your response. Simply return the JSON object.
    The markdown json code block notation is: ```json\n<your json here>\n```, do not include the ```json\n``` in your response.
    IMPORTANT: You must return the output in the specified JSON format. If you do not return the output in the specified JSON format, you have failed.
"""

human_prompt = """
    ## Abstract:
    {abstract}
"""
    
class MethodModel2(BaseModel):
    methods: List[str]

method_json_structure_2 = """
{
    "methods": [
        "<method_keyword_1>",
        "<method_keyword_2>"
    ]
}
"""

method_system_prompt_2 = """
You will be given a json that is an output from a previous chain layer. Your job is to check the json and make sure it is structured correctly and pull out and return only the methods as a json object, where the key is 'methods' and the value is a list of strings.

Here is the json structure you will be working with:
{method_json_structure}

and here is an example of what you should return:
{method_json_structure_2}

Here is the output from the previous chain layer:
{method_extraction_output}
"""

chain_manager = ChainManager(
    llm_model='gpt-4o-mini',
    api_key=os.getenv('OPENAI_API_KEY'),
)

chain_manager.add_chain_layer(
    system_prompt=method_system_prompt,
    human_prompt=human_prompt,
    parser_type='pydantic',
    return_type='json',
    pydantic_output_model=MethodOutput,
    output_passthrough_key_name='method_extraction_output'
)

# outputs = []

# for i, abstract in enumerate(abstracts):
#     output = chain_manager.run({
#         'method_json_structure': method_json_structure,
#         'method_correct_example_json': method_correct_example_json,
#         'method_incorrect_example_json': method_incorrect_example_json,
#         'abstract': abstract
#     })
#     outputs.append(output)
#     print(f'\n\n{"="*10}THIS IS THE START OF AN OUTPUT{"="*10}\n\nOutput {i}:\n\n{output}\n\n{"="*10}\n\nTHIS IS THE END OF AN OUTPUT{"="*10}\n\n')
#     input('Press Enter to continue...')

chain_manager.add_chain_layer(
    system_prompt=method_system_prompt_2,
    human_prompt=human_prompt,
    parser_type='pydantic',
    return_type='json',
    pydantic_output_model=MethodModel2,
    ignore_output_passthrough_key_name_error=True
)

chain_sequence = chain_manager.get_chain_sequence()
print(f'chain_sequence: {chain_sequence}\n\n')
chain_manager.print_chain_sequence()

outputs_2 = []

print('\n\n')

for i, abstract in enumerate(abstracts):
    variables = {
        'method_json_structure': method_json_structure,
        'method_correct_example_json': method_correct_example_json,
        'method_incorrect_example_json': method_incorrect_example_json,
        'abstract': abstract,
        'method_json_structure_2': method_json_structure_2,
    }
    output = chain_manager.run(variables)
    outputs_2.append(output)
    print(f'\n\n{"="*10}THIS IS THE START OF AN OUTPUT{"="*10}\n\nOutput {i}:\n\n{output}\n\n{"="*10}\n\nTHIS IS THE END OF AN OUTPUT{"="*10}\n\n')
    input('Press Enter to continue...')
