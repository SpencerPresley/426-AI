I have this abstract:

## Abstract: 
Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.

And I run it through several AI chains, a method extractor, a sentence analysis, and a summary generator, these are the prompts and results for those.

## Method prompt:
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

## Method results
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
        "confidence_score": 0.9
    }
}


## Sentence analysis prompt:
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

    IMPORTANT: Be concise but clear in your meanings and reasonings.
    IMPORTANT: Ensure that the confidence score reflects how certain you are about the meaning of the sentence in context.
    IMPORTANT: Do not include the markdown json code block notation in your response. Simply return the JSON object. The markdown json code block notation is: ```json\n<your json here>\n```, do not include the ```json\n``` in your response.
    IMPORTANT: You must return the output in the specified JSON format. If you do not return the output in the specified JSON format, you have failed.
    """


## Sentence Analysis results:
{
    "sentence_analysis": [
        {
            "sentence": "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise.",
            "meaning": "The research investigates how the real expertise and social status of team members affect their influence on team dynamics, particularly through the lens of perceived expertise.",
            "reasoning": "The mention of 'expectation states theory' and 'expertise utilization literature' indicates a theoretical framework guiding the analysis of influence, suggesting a focus on how expertise and status interplay in team settings.",
            "confidence_score": 0.9
        },
        {
            "sentence": "We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams.",
            "meaning": "The study looks into the situations that dictate whether teams prioritize perceived expertise or social status when assessing influence among members.",
            "reasoning": "The use of 'conditions' implies a contextual analysis, indicating that the impact of perceived expertise and social status varies depending on specific circumstances within teams.",
            "confidence_score": 0.85
        },
        {
            "sentence": "To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts.",
            "meaning": "The authors propose a model that outlines how the importance of expertise and social status is influenced by different types of conflicts that arise within teams.",
            "reasoning": "The term 'contingency model' suggests a structured approach to understanding the dynamics of influence and conflict, indicating that the relationship is not fixed but rather conditional.",
            "confidence_score": 0.88
        },
        {
            "sentence": "Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise.",
            "meaning": "The research utilizes survey data from student teams to demonstrate that real expertise and social status impact team influence, both directly and indirectly, via perceived expertise.",
            "reasoning": "The specificity of the data source and the mention of 'direct and indirect effects' indicates a thorough empirical investigation into the relationships being studied.",
            "confidence_score": 0.9
        },
        {
            "sentence": "Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise.",
            "meaning": "The findings reveal that in the initial phases of projects, social status influences perceived expertise, while in later phases, actual expertise takes precedence.",
            "reasoning": "The differentiation between early and later stages suggests a dynamic shift in influence determinants over time, highlighting the evolving nature of team interactions.",
            "confidence_score": 0.92
        },
        {
            "sentence": "Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low.",
            "meaning": "The research concludes that perceived experts have greater influence in scenarios characterized by high task conflict or low relationship conflict.",
            "reasoning": "The contrast between task and relationship conflict highlights the conditions under which perceived expertise is most effective, suggesting practical implications for team management.",
            "confidence_score": 0.87
        },
        {
            "sentence": "We discuss the implications of these findings for research and practice.",
            "meaning": "The authors will elaborate on the significance of their results for both academic research and practical applications in team settings.",
            "reasoning": "The phrase 'discuss the implications' indicates a forward-looking perspective, emphasizing the relevance of the findings beyond the study itself.",
            "confidence_score": 0.85
        }
    ],
    "overall_theme": "The research investigates the interplay between actual expertise and social status in determining influence within teams, emphasizing the role of perceived expertise and the impact of intragroup conflicts.",
    "detailed_summary": "This study examines how team members' actual expertise and social status affect their influence over team processes through perceived expertise, guided by expectation states theory and expertise utilization literature. It explores the conditions under which teams prioritize perceived expertise or social status, presenting a contingency model that links the importance of these factors to types of intragroup conflicts. Utilizing multiwave survey data from 50 student project teams at a national research institute in South Korea, the findings reveal that both actual expertise and social status have direct and indirect effects on member influence through perceived expertise. Notably, social status drives perceived expertise in the early stages of projects, while actual expertise becomes more significant in later stages. Additionally, perceived experts are more influential in high task conflict situations or low relationship conflict scenarios. The authors conclude by discussing the implications of these findings for future research and practical applications in team dynamics."
}


## Summary prompt
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
    {
        "summary": "Detailed summary of the abstract",
        "reasoning": "Detailed reasoning for the summary",
        "feedback": {
            "methodologies_feedback": "Feedback for the methodologies assistant",
            "abstract_sentence_analysis_feedback": "Feedback for the abstract sentence analysis assistant"
        }
    }
    ```

    IMPORTANT: Your summary should focus on the main idea of the research while not being concerned with the specific methods used to conduct the research. If you are concerned with the specific methods used to conduct the research, you are doing it wrong. If you summary contains mentions of the methodologies used, you are doing it wrong.
    IMPORTANT: Ensure that your feedback is specific to the methodologies assistant and abstract sentence level analysis assistant. Do not provide feedback for the sake of providing feedback, provide feedback that will actually help the assistants improve their analysis of the abstract.
    IMPORTANT: Do not include the markdown json code block notation in your response. Simply return the JSON object. The markdown json code block notation is: ```json\n<your json here>\n```, do not include the ```json\n``` in your response.
    IMPORTANT: You must return the output in the specified JSON format. If you do not return the output in the specified JSON format, you have failed.
    """
)

## Summary results
{
    "summary": "This study investigates how the actual expertise and social status of team members influence their ability to affect team processes through perceived expertise. It examines the conditions under which teams prefer perceived expertise over social status in their influence dynamics. The authors propose a contingency model that links the significance of expertise and social status to different types of intragroup conflicts. The research, based on multiwave survey data from 50 student project teams, reveals that both actual expertise and social status directly and indirectly affect influence through perceived expertise. Notably, social status is more influential in the early stages of projects, while actual expertise becomes more dominant later. The findings also indicate that perceived experts are particularly influential in contexts of high task conflict or low relationship conflict, highlighting practical implications for team dynamics and management.",
    "reasoning": "The summary captures the essence of the research by highlighting the main focus on the interplay between actual expertise, social status, and perceived expertise within team dynamics. It emphasizes the development of a contingency model and the empirical findings derived from the survey data, providing a clear picture of how these factors interact across different contexts of intragroup conflict. The reasoning is rooted in the abstract's structure, which delineates the objectives, methods, and key findings, ensuring a comprehensive yet concise representation of the research.",
    "feedback": {
        "methodologies_feedback": "The analysis is correct and sufficient, I have no feedback at this time.",
        "abstract_sentence_analysis_feedback": "The analysis is correct and sufficient, I have no feedback at this time."
    }
}


Then I run it through a classification, where I explore the classified categories like a tree, here is an example of one full category tree item:
    "Social sciences": {
        "Anthropology": [
            "Anthropology, general",
            "Cultural anthropology",
            "Physical and biological anthropology",
            "Anthropology nec"
        ],
        "Area, ethnic, cultural, gender, and group studies": [
            "Area studies",
            "Ethnic studies",
            "Area, ethnic, cultural, gender, and group studies nec"
        ],
        "Economics": [
            "Agricultural economics",
            "Applied economics",
            "Development economics and international development",
            "Econometrics and quantitative economics",
            "Economics, general",
            "Environmental/ natural resource economics",
            "Economics nec"
        ],
        "Political science and government": [
            "Political science and government, general",
            "Political science and government nec"
        ],
        "Public policy analysis": [
            "Education policy analysis",
            "Health policy analysis",
            "Public policy analysis, general",
            "Public policy nec"
        ],
        "Sociology, demography, and population studies": [
            "Sociology, general",
            "Sociology, demography, and population studies nec"
        ],
        "Social sciences, other": [
            "Applied linguistics",
            "Archeology",
            "Criminal justice and corrections",
            "Criminology",
            "Geography and cartography",
            "International relations and national security studies",
            "Linguistics",
            "Social sciences nec"
        ]
    },

Here is the classification prompt:

## Classifiaction prompt:
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
    
    IMPORTANT: Do not classify based on the specific methods used to conduct the research, the use of methods is only relevant if it is the main focus of the research or if it helps obtain more contextual understanding of the abstract. The classifications should be representative of the core theme behind the research, as in what the research is doing but not how it is doing it.
    IMPORTANT: Your output should always be a JSON object following the provided structure, if you do not follow the provided structure and/ or do not provide a JSON object, you have failed.
    IMPORTANT: Do not include the markdown json code block notation in your response. Simply return the JSON object.
"""
)



Here are the raw results from the llm. You'll see top category, mid category, and low category classification. (Each level (top, mid, low) is handled individually, it provides reasoning for each category at each level.)
[
    {
        "classifications": [
            {
                "abstract": "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.",
                "categories": [
                    "Social sciences",
                    "Business",
                    "Education"
                ],
                "reasoning": "The research focuses on the dynamics of team processes, specifically how expertise and social status influence team member interactions and decision-making. This falls under social sciences as it examines social behaviors and structures. Additionally, the implications for team dynamics and influence relate to business contexts, particularly in organizational behavior. The educational aspect is evident as the study involves student project teams, highlighting the implications of team processes in educational settings.",
                "confidence_score": 0.85
            }
        ],
        "reflection": "I found it challenging to determine the exact balance between the categories of 'Social sciences' and 'Business' since the research touches on elements relevant to both fields. The core theme of team dynamics could fit into various categories, but I believe the emphasis on social behaviors solidifies its classification under social sciences while also being pertinent to business contexts. A clearer delineation of the research's primary focus could help alleviate this ambiguity in future classifications.",
        "feedback": [
            {
                "assistant_name": "methodologies assistant",
                "feedback": "The methodologies identified are suitable for understanding the research approach, particularly the use of multiwave survey data. However, further clarification on how the contingency model functions in practical terms could enhance understanding."
            },
            {
                "assistant_name": "abstract sentence analysis assistant",
                "feedback": "The analysis is correct and sufficient, I have no feedback at this time."
            },
            {
                "assistant_name": "abstract summary assistant",
                "feedback": "The summary encapsulates the main points effectively, but it could benefit from elaborating on the implications for practical application, which is a significant aspect of the research findings."
            }
        ]
    },
    {
        "classifications": [
            {
                "abstract": "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.",
                "categories": [
                    "Sociology, demography, and population studies",
                    "Social sciences, other"
                ],
                "reasoning": "The abstract focuses on the dynamics within teams, specifically examining how social status and expertise influence team processes and member interactions. This aligns closely with sociological themes of group dynamics and influence. Additionally, the exploration of team conflicts and the implications of social status and expertise fits within broader social science discussions, justifying the classification under 'Social sciences, other'.",
                "confidence_score": 0.9
            }
        ],
        "reflection": "I found it relatively straightforward to classify the abstract into the categories provided. The main challenge was ensuring that I focused on the overarching themes rather than the specific methodologies or data collection methods mentioned, such as the multiwave survey data. However, the abstract's emphasis on team dynamics and social influence made the classification clear. If there were more ambiguity in the themes, it could have been more challenging to categorize effectively.",
        "feedback": [
            {
                "assistant_name": "methodologies assistant",
                "feedback": "The methodologies identified are relevant, but it would be useful to clarify how the specific methods relate to the overall contributions of the research. Additionally, the focus should be on how these methodologies help understand the broader implications rather than just detailing the methods used."
            },
            {
                "assistant_name": "abstract sentence analysis assistant",
                "feedback": "The analysis is correct and sufficient, I have no feedback at this time."
            },
            {
                "assistant_name": "abstract summary assistant",
                "feedback": "The summary captures the essence of the research effectively. However, it could benefit from a clearer articulation of the implications discussed in the findings, as this is a significant aspect of the research that could enhance understanding."
            }
        ]
    },
    {
        "classifications": [
            {
                "abstract": "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.",
                "categories": [
                    "Sociology, general"
                ],
                "reasoning": "The abstract explores the dynamics of team processes, specifically how social status and expertise influence member relationships and decision-making within teams, which falls under the purview of general sociology. It discusses theoretical implications and social behavior in group settings, aligning with sociological inquiry into human interactions and group dynamics.",
                "confidence_score": 0.85
            }
        ],
        "reflection": "I found it straightforward to classify the abstract into the category of 'Sociology, general' as it discusses social dynamics within teams, focusing on expertise and social status. However, I had to carefully consider whether the specifics of team processes and intragroup conflicts might imply a narrower focus, but the broader implications for social behavior supported the classification.",
        "feedback": [
            {
                "assistant_name": "methodologies assistant",
                "feedback": "The methodologies identified seem relevant; however, it would be beneficial to clarify how these methods specifically contribute to understanding the social dynamics discussed in the abstract. A more detailed contextual connection between methodology and findings could enhance the clarity."
            },
            {
                "assistant_name": "abstract sentence level analysis assistant",
                "feedback": "The analysis is correct and sufficient, I have no feedback at this time."
            },
            {
                "assistant_name": "abstract summary assistant",
                "feedback": "The summary captures the main themes effectively, but it could benefit from a more explicit mention of the implications for theory and practice, as this is highlighted in the abstract."
            }
        ]
    },
    {
        "classifications": [
            {
                "abstract": "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.",
                "categories": [
                    "Social sciences nec"
                ],
                "reasoning": "The abstract discusses team dynamics, influence, and the effects of social status and expertise in team processes, which all fall under social sciences. It does not specifically pertain to any other defined categories such as criminology, linguistics, or geography.",
                "confidence_score": 0.95
            }
        ],
        "reflection": "I felt confident in identifying the primary theme as it relates to social dynamics within teams, which aligns well with the 'Social sciences nec' category. The comprehensive analysis of expertise and social status as they pertain to team influence processes reinforced this classification. There were no significant struggles in classifying this abstract due to the clear focus on social science concepts.",
        "feedback": [
            {
                "assistant_name": "methodologies assistant",
                "feedback": "The methodologies identified are relevant and support the context of the abstract well. However, more clarity on how these methods interact with the findings could enhance understanding."
            },
            {
                "assistant_name": "abstract sentence analysis assistant",
                "feedback": "The analysis is correct and sufficient, I have no feedback at this time."
            },
            {
                "assistant_name": "abstract summary assistant",
                "feedback": "The summary captures the essence of the abstract well. However, it could be slightly more concise to improve readability while maintaining the key points."
            }
        ]
    },
    {
        "classifications": [
            {
                "abstract": "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.",
                "categories": [
                    "Business administration and management"
                ],
                "reasoning": "The abstract focuses on the dynamics of team influence, expertise, and social status within teams, which are critical elements in business management and organizational behavior. It discusses how these factors affect team processes and decision-making, making it highly relevant to business administration.",
                "confidence_score": 0.95
            }
        ],
        "reflection": "I found it straightforward to classify this abstract as it clearly relates to concepts in business administration, particularly regarding team dynamics and influence. There was no significant struggle in identifying the relevant category since the themes presented align well with the provided categories.",
        "feedback": [
            {
                "assistant_name": "methodologies assistant",
                "feedback": "The methodologies identified in the abstract were not extracted in the provided data, but it would be beneficial for future analyses to highlight methods such as contingency modeling or survey analysis. This could provide clearer context for how the research was conducted."
            },
            {
                "assistant_name": "abstract sentence analysis assistant",
                "feedback": "The analysis is correct and sufficient, I have no feedback at this time."
            },
            {
                "assistant_name": "abstract summary assistant",
                "feedback": "The summary accurately captures the essence of the abstract, but it could be enhanced by explicitly mentioning the implications for research and practice, which is a key aspect of the findings discussed."
            }
        ]
    },
    {
        "classifications": [
            {
                "abstract": "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.",
                "categories": [
                    "Organizational leadership"
                ],
                "reasoning": "The research focuses on the influence dynamics within teams, specifically how team members' expertise and social status affect their influence on team processes. This aligns closely with themes of organizational leadership, as it delves into understanding how leadership and influence are shaped in team settings, which is a core concern of organizational dynamics.",
                "confidence_score": 0.95
            }
        ],
        "reflection": "I struggled a bit with distinguishing whether the abstract also warranted classification under 'Business management and administration', given that team dynamics can often relate to broader business contexts. However, the focus is more on the leadership aspect within the organizational framework rather than the administration of business itself. Therefore, 'Organizational leadership' is the more fitting category.",
        "feedback": [
            {
                "assistant_name": "methodologies assistant",
                "feedback": "The methodologies identified were appropriate for understanding the research context, but it would be beneficial to clarify how the methods tie into the conclusions drawn. Providing more explicit connections between methodology and findings could enhance the overall understanding."
            },
            {
                "assistant_name": "abstract sentence analysis assistant",
                "feedback": "The analysis is correct and sufficient, I have no feedback at this time."
            },
            {
                "assistant_name": "abstract summary assistant",
                "feedback": "The summary captures the essence of the research well, but it could be more succinct while maintaining clarity. A more concise summary might improve readability without losing important details."
            }
        ]
    },
    {
        "classifications": [
            {
                "abstract": "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.",
                "categories": [
                    "Education research",
                    "Teacher education"
                ],
                "reasoning": "The abstract focuses on examining the influence of actual expertise and social status in team dynamics, particularly in an educational context involving student project teams. It discusses the implications of these findings for research and practice, indicating a contribution to the field of education research. Additionally, since the study involves student project teams, it makes relevant contributions to teacher education, particularly in understanding team processes in educational settings.",
                "confidence_score": 0.85
            }
        ],
        "reflection": "I initially struggled with clearly identifying the primary focus of the research in terms of the categories provided. The abstract discusses both educational settings (student project teams) and broader research implications, which could lead to multiple classifications. However, I eventually determined that the emphasis on team dynamics in an educational context warranted classifications under both 'Education research' and 'Teacher education'. Clarifying the specific educational implications further helped in making this determination.",
        "feedback": [
            {
                "assistant_name": "methodologies assistant",
                "feedback": "The methodologies identified seem relevant, but there could be more clarity on how the data collection and analysis methods directly contribute to the findings presented. A more detailed explanation of the methodologies could enhance understanding."
            },
            {
                "assistant_name": "abstract sentence level analysis assistant",
                "feedback": "The analysis is correct and sufficient, I have no feedback at this time."
            },
            {
                "assistant_name": "abstract summary assistant",
                "feedback": "The summary captures the essence of the research well, but it could include more emphasis on the educational context of the study. Additionally, mentioning the implications for practice could provide a fuller picture."
            }
        ]
    },
    {
        "classifications": [
            {
                "abstract": "Drawing on expectation states theory and expertise utilization literature, we examine the effects of team members' actual expertise and social status on the degree of influence they exert over team processes via perceived expertise. We also explore the conditions under which teams rely on perceived expertise versus social status in determining influence relationships in teams. To do so, we present a contingency model in which the salience of expertise and social status depends on the types of intragroup conflicts. Using multiwave survey data from 50 student project teams with 320 members at a large national research institute located in South Korea, we found that both actual expertise and social status had direct and indirect effects on member influence through perceived expertise. Furthermore, perceived expertise at the early stage of team projects is driven by social status, whereas perceived expertise at the later stage of a team project is mainly driven by actual expertise. Finally, we found that members who are being perceived as experts are more influential when task conflict is high or when relationship conflict is low. We discuss the implications of these findings for research and practice.",
                "categories": [
                    "Higher education evaluation and research",
                    "Education research nec"
                ],
                "reasoning": "The abstract focuses on examining the influence of team members' expertise and social status within student project teams, which directly relates to the evaluation and research of higher education contexts. Additionally, the findings have broader implications for education research not specifically covered by other categories.",
                "confidence_score": 0.85
            }
        ],
        "reflection": "I found it somewhat challenging to determine the most appropriate categories due to the abstract's focus on team dynamics and influence, which could fit into various educational contexts. However, the emphasis on student teams in a research setting guided my classification towards higher education evaluation and education research. A clearer delineation of how this research contributes to educational practices would have aided in making a more confident classification.",
        "feedback": [
            {
                "assistant_name": "methodologies assistant",
                "feedback": "The identified methodologies are relevant and accurately reflect the approaches taken in the research. However, providing additional context on how these methodologies directly connect to the research findings would enhance understanding."
            },
            {
                "assistant_name": "abstract sentence analysis assistant",
                "feedback": "The analysis is correct and sufficient, I have no feedback at this time."
            },
            {
                "assistant_name": "abstract summary assistant",
                "feedback": "The summary accurately captures the essence of the research. It effectively highlights the influence of expertise and social status in team processes, although a mention of the implications for educational practices could strengthen it further."
            }
        ]
    },
    {
        "classifications": [],
        "reflection": "I struggled with finding an appropriate category because the abstract is focused on team processes and social dynamics rather than education or teacher training. The absence of relevant themes related to the provided categories made it clear that none fit well.",
        "feedback": [
            {
                "assistant_name": "methodologies assistant",
                "feedback": "The methodologies identified do not apply to the categories provided, as they focus on social dynamics rather than educational strategies. It may be beneficial to include a broader range of contexts in future analyses."
            },
            {
                "assistant_name": "abstract sentence analysis assistant",
                "feedback": "The analysis is correct and sufficient, I have no feedback at this time."
            },
            {
                "assistant_name": "abstract summary assistant",
                "feedback": "The summary is accurate, but it could clarify the educational context if applicable. However, since this abstract does not relate to education, this context may not be necessary."
            }
        ]
    }
]

Here is the result for the abstract given:
    "abstract_0": {
        "Social sciences": {
            "Sociology, demography, and population studies": {
                "Sociology, general": {}
            },
            "Social sciences, other": {
                "Social sciences nec": {}
            }
        },
        "Business": {
            "Business administration and management": {
                "Organizational leadership": {}
            }
        },
        "Education": {
            "Education research": {
                "Higher education evaluation and research": {},
                "Education research nec": {}
            },
            "Education, other": {
                "Education, general": {}
            }
        }
    },

Additionally we got this feedback from the author on a previous system:

Top Level Categories: Social and Information Sciences, Mathematics, Quantitative Biology

Mid-Level Categories: Human-Computer Interaction, Computation and Language, Computational Complexity, Quantitative Methods

Bottom Level Categories: Expertise Utilization, Team Processes, Intragroup Conflicts, Perceived Expertise, Social Status, Influence Relationships

Feedback from author:
        •   Top-level category: Social science (not mathematics or quantitative biology)

        •   Mid-level categories: Quantitative methods (not human-computer interaction, computation and language, or computational complexity)

        •   Bottom-level categories: This looks good.

Do these actually look accurate to the themes and not the methods?
Any idea why education may be appearing? 
Any advice to enhancing the prompts or providing more data? 

We get the current data from crossref api, here is an example of an item (note the same data applies to all items, but this item is not corresponding to this abstract, purely use this to see what author data I can provide to the ai):

## Crossref api return item example: 
    {
        "indexed": {
            "date-parts": [
                [
                    2023,
                    12,
                    12
                ]
            ],
            "date-time": "2023-12-12T00:29:07Z",
            "timestamp": 1702340947259
        },
        "reference-count": 0,
        "publisher": "Wiley",
        "issue": "S1",
        "license": [
            {
                "start": {
                    "date-parts": [
                        [
                            2020,
                            4,
                            18
                        ]
                    ],
                    "date-time": "2020-04-18T00:00:00Z",
                    "timestamp": 1587168000000
                },
                "content-version": "vor",
                "delay-in-days": 17,
                "URL": "http://onlinelibrary.wiley.com/termsAndConditions#vor"
            }
        ],
        "content-domain": {
            "domain": [
                "faseb.onlinelibrary.wiley.com"
            ],
            "crossmark-restriction": true
        },
        "short-container-title": [
            "The FASEB Journal"
        ],
        "published-print": {
            "date-parts": [
                [
                    2020,
                    4
                ]
            ]
        },
        "abstract": "<jats:sec><jats:title>Objective</jats:title><jats:p>To determine the effects of acute creatine monohydrate supplementation on arterial stiffness (AS) and skeletal muscle oxygen saturation (SmO2). There is a void in our knowledge on the impact of acute creatine monohydrate supplementation on AS in the major elastic arteries. In addition, there is a dearth of findings on the effects of creatine supplementation on SmO2 in the lower leg. Data have indicated that creatine supplementation can result in an increase in lower leg anterior compartment pressure at rest and post exercise. Although the increased pressures seen during these studies were not pathological, this and additional factors associated with creatine supplementation could possibly effect SmO2 during exercise and recovery.</jats:p></jats:sec><jats:sec><jats:title>Methods</jats:title><jats:p>20 male, physically active participants were randomized in a double\u2010blind fashion to placebo (PL) (n=10, 22.9\u00b13.1 yrs.) or creatine (CM) (n=10, 21.3\u00b11.8 yrs.) groups. Subjects received 0.3 g/kg/day creatine monohydrate or placebo in gelatin capsules for 7 days. Ultrasonography of the carotid artery, applanation tonometry, submaximal exercise tests (10 minute treadmill activity at 3.7 mph and 9% incline), SmO2, and lower leg pain (analog visual scale and pain test algometer) assessments were conducted at baseline and on day 7 of the study period.</jats:p></jats:sec><jats:sec><jats:title>Results</jats:title><jats:p>There were baseline differences in central systolic blood pressure (cSBP) (mean difference, 109; 95% confidence interval (CI) 105 to 113, vs. mean difference, 130; 95% CI 114 to 146, p &lt; 0.05) between the PLA and CM groups, respectively. Following the intervention, there were no significant differences between PL and CM in arterial stiffness indices between the groups. There was a significant group effect (P&lt;0.03) but no significant effect of supplementation (P&gt;0.05) on the % change in SmO2 during the exercise tests (CM: pre 66.49 \u00b1 30.54; post 59.61 \u00b1 23.87 vs. PL: pre 39.87 \u00b1 16.72; post 38.51 \u00b1 26.95 % change SmO2; M \u00b1 SD). Percent fat free mass (FFM) was significantly increased (mean, 68.5\u00b17.5%; 95% CI 62.1% to 72.9%, to mean 69.3\u00b17.5% 95% CI 62.9% to 73.6%, P&lt;0.05) in the CM group only. There were no other significant changes in anthropometric measurements.</jats:p></jats:sec><jats:sec><jats:title>Conclusions</jats:title><jats:p>Using a randomly controlled, double\u2010blind trial with validated measurements of AS and SmO2, acute creatine supplementation does not appear to impact vascular compliance or oxygen saturation in skeletal muscle in young, healthy males.</jats:p></jats:sec>",
        "DOI": "10.1096/fasebj.2020.34.s1.06192",
        "type": "journal-article",
        "created": {
            "date-parts": [
                [
                    2020,
                    4,
                    19
                ]
            ],
            "date-time": "2020-04-19T05:24:02Z",
            "timestamp": 1587273842000
        },
        "page": "1-1",
        "update-policy": "http://dx.doi.org/10.1002/crossmark_policy",
        "source": "Crossref",
        "is-referenced-by-count": 0,
        "title": [
            "Effect of Acute Creatine Supplementation on Arterial Stiffness and Muscle Oxygen Saturation"
        ],
        "prefix": "10.1096",
        "volume": "34",
        "author": [
            {
                "given": "Thomas K.",
                "family": "Pellinger",
                "sequence": "first",
                "affiliation": [
                    {
                        "name": "Salisbury University"
                    }
                ]
            },
            {
                "given": "Colin J.",
                "family": "Gimblet",
                "sequence": "additional",
                "affiliation": [
                    {
                        "name": "Salisbury University"
                    }
                ]
            },
            {
                "given": "Morgan M.",
                "family": "Vance",
                "sequence": "additional",
                "affiliation": [
                    {
                        "name": "Salisbury University"
                    }
                ]
            },
            {
                "given": "Meghan",
                "family": "Shepherd",
                "sequence": "additional",
                "affiliation": [
                    {
                        "name": "Salisbury University"
                    }
                ]
            },
            {
                "given": "Austin T.",
                "family": "Ortlip",
                "sequence": "additional",
                "affiliation": [
                    {
                        "name": "Salisbury University"
                    }
                ]
            },
            {
                "given": "Timothy B.",
                "family": "Staudmyer",
                "sequence": "additional",
                "affiliation": [
                    {
                        "name": "Salisbury University"
                    }
                ]
            },
            {
                "given": "John J.",
                "family": "Lamanca",
                "sequence": "additional",
                "affiliation": [
                    {
                        "name": "Salisbury University"
                    }
                ]
            },
            {
                "given": "Timothy J.",
                "family": "Werner",
                "sequence": "additional",
                "affiliation": [
                    {
                        "name": "Salisbury University"
                    }
                ]
            }
        ],
        "member": "311",
        "published-online": {
            "date-parts": [
                [
                    2020,
                    4,
                    18
                ]
            ]
        },
        "container-title": [
            "The FASEB Journal"
        ],
        "language": "en",
        "deposited": {
            "date-parts": [
                [
                    2023,
                    12,
                    11
                ]
            ],
            "date-time": "2023-12-11T11:23:52Z",
            "timestamp": 1702293832000
        },
        "score": 18.222166,
        "resource": {
            "primary": {
                "URL": "https://faseb.onlinelibrary.wiley.com/doi/10.1096/fasebj.2020.34.s1.06192"
            }
        },
        "issued": {
            "date-parts": [
                [
                    2020,
                    4
                ]
            ]
        },
        "references-count": 0,
        "journal-issue": {
            "issue": "S1",
            "published-print": {
                "date-parts": [
                    [
                        2020,
                        4
                    ]
                ]
            }
        },
        "alternative-id": [
            "10.1096/fasebj.2020.34.s1.06192"
        ],
        "URL": "http://dx.doi.org/10.1096/fasebj.2020.34.s1.06192",
        "archive": [
            "Portico"
        ],
        "ISSN": [
            "0892-6638",
            "1530-6860"
        ],
        "issn-type": [
            {
                "value": "0892-6638",
                "type": "print"
            },
            {
                "value": "1530-6860",
                "type": "electronic"
            }
        ],
        "published": {
            "date-parts": [
                [
                    2020,
                    4
                ]
            ]
        },
        "assertion": [
            {
                "value": "2020-04-18",
                "order": 2,
                "name": "published",
                "label": "Published",
                "group": {
                    "name": "publication_history",
                    "label": "Publication History"
                }
            }
        ]
    },

Walk through and break it down step by step. 