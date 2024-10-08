# AI System Overview
## Summary of the Classification Problem

We are building a system to classify research papers into a **hierarchical set of predefined categories**, starting from the **broadest level of Area of Study** and narrowing down to **Broad, Major, and Detailed categories**. The classification process must handle both **single-category assignments** (in the case of Area of Study) and **multi-category assignments** (where papers may fall under multiple Broad, Major, or Detailed categories). 

To achieve this, we will be utilizing two primary models:
1. **Google Gemini Pro 1.5** for **extracting entities and key passages** from papers, thanks to its impressive 2 million token context window, which can handle large and complex research papers.
2. **OpenAI's GPT-4o** for more intensive **reasoning steps** and final classification, which will be fine-tuned on a custom dataset.

### Challenges

1. **Handling Complex Content at Different Classification Levels**: Research papers can be long and dense, with multiple areas of focus. Extracting relevant content from large texts for the different classification levels (Area, Broad, Major, Detailed) is challenging.

2. **Balancing Manual and Automated Classification**: We will manually categorize around 20 papers, building a dataset that shows **why** specific categories were selected. This dataset will be used as a foundation for generating a **larger pseudo-dataset** using Google Gemini. From this, we aim to fine-tune GPT-4o as the final classifier.

3. **Creating a Multi-Step Categorization**: The hierarchical classification needs to first assign papers to **one Area of Study**, followed by selecting the appropriate **Broad, Major, and Detailed categories**. Papers may belong to one Area of Study but can have multiple Broad, Major, or Detailed categories, increasing the complexity of classification.

4. **Ensuring Consistency Across Models**: With two models—Google Gemini for content extraction and GPT-4o for classification—maintaining consistency in data interpretation and ensuring smooth handoff between tasks will be crucial.

### Approach to Success

1. **Entity and Passage Extraction with Google Gemini Pro**: The 2 million token context window allows for the extraction of **entities and key passages** from the papers, which will provide the groundwork for identifying relevant categories at each level. This model will handle the **data preprocessing** step by extracting content that GPT-4o will use to make the final classification decisions.

2. **Manual Categorization and Dataset Generation**: We will manually categorize **20 papers**, creating a **ground truth dataset** that contains the categories each paper falls into and detailed reasoning behind the selection of these categories. This reasoning will cite specific parts of the **abstract and other sections** of the papers to provide clear justifications for each category assignment.

3. **Pseudo-Dataset Generation with Google Gemini**: Using the manually categorized dataset, Google Gemini will generate a larger **pseudo-dataset** by expanding on the reasoning and extracting additional content from similar papers. This will ensure the dataset is rich enough for effective fine-tuning of GPT-4o.

4. **Fine-Tuning GPT-4o**: The final classifier will be a **fine-tuned version of GPT-4o**, trained on the pseudo-dataset generated by Google Gemini. This fine-tuned model will perform the hierarchical classification, starting with the **Area of Study** and working its way down to the more specific categories (Broad, Major, and Detailed).

---

# Techniques

## Longer Definition Embedding

The **Longer Definition Embedding** approach involves enriching the embeddings of each category by providing **detailed descriptions**. These definitions will serve as a more accurate reference point for the embeddings that GPT-4o generates when comparing paper content to categories. Instead of using brief labels like "Biophysics" or "Machine Learning," we will generate more detailed descriptions, which provide specific context and scope.

### Benefits
- **Custom Definitions**: By defining each category according to our exact understanding, we can avoid any potential misinterpretations by the model and ensure that each category reflects its intended scope.
- **Enhanced Comparability**: These longer descriptions will result in richer embeddings, making it easier to compare the detailed paper content against a broader, more accurate category embedding.

### Challenges
- **Construction of Definitions**: Crafting detailed, precise descriptions for each category is time-consuming but essential for accurate embedding comparisons.

---

## Combining and Weighing Embeddings

This technique will be used to create a **comprehensive representation** of each paper by combining embeddings from multiple elements—**entities, keywords, key passages**—extracted by Google Gemini. Each component will be **weighed differently** based on its relevance to the classification task.

For instance, **entities** that capture key topics or concepts will likely have more influence on the classification, while **keywords and key passages** may serve as secondary sources of information that support the main classification.

### Benefits
- **Weighted Relevance**: By adjusting the weights of different content features, we ensure that the most important content (such as key entities) has more influence on the classification, while less important elements contribute in a supportive role.
- **Holistic View**: This method allows the system to take multiple factors into account, creating a more comprehensive and accurate picture of the paper’s focus.

### Challenges
- **Weighting Tuning**: Determining the appropriate weights for entities, keywords, and passages will require careful calibration to ensure the most relevant features have the strongest influence.

---

## Multi-Step Evaluation

The classification process will follow a **multi-step evaluation** approach, where each step in the hierarchy (Area of Study, Broad, Major, Detailed categories) is addressed separately. This method allows for the breakdown of the paper into individual aspects (entities, keywords, passages), which are evaluated against their respective category levels.

### Steps:
1. **Area of Study Classification**: The first task is to classify the paper into one **Area of Study**. Since each paper can belong to only one area, this step helps narrow down the classification process early.
   
2. **Broad Category Classification**: Once the Area is determined, the paper will be classified into one or more **Broad categories**. These categories capture the general subfields under the Area of Study.

3. **Major Category Classification**: After determining the Broad categories, the paper will be classified into one or more **Major categories**, further refining its classification into more specific research domains.

4. **Detailed Category Classification**: Finally, within the Major categories, the system will identify one or more **Detailed categories**. These represent the most specific focus areas of the paper.

### Benefits
- **Granular Control**: Evaluating each level separately ensures that the classification process is detailed and logical, with each level building on the previous one.
- **Flexibility**: Papers can have multiple categories at the Broad, Major, and Detailed levels, ensuring the system is flexible enough to handle multi-disciplinary papers.

### Challenges
- **Complex Orchestration**: The multi-step approach adds complexity, as each layer needs to feed into the next accurately and consistently.

---

# Manual Dataset Generation and Pseudo-Dataset Expansion

### Manual Categorization

We will manually categorize **around 20 papers**, selecting the appropriate categories for each and providing detailed explanations for why each category was chosen. This dataset will serve as a **ground truth** for training the model, with specific sections from the **abstract and other parts of the paper** cited to justify each category decision.

### Pseudo-Dataset Generation

Using the manually generated dataset, we will use **Google Gemini Pro 1.5** to generate a **pseudo-dataset** by expanding the reasoning and applying it to a broader set of papers. This larger dataset will provide a robust foundation for **fine-tuning GPT-4o**, enabling it to make accurate classification decisions based on the reasoning embedded in the pseudo-dataset.

### Benefits
- **Ground Truth Dataset**: The manually categorized papers serve as a high-quality reference for understanding why certain categories were selected, improving the model's ability to learn reasoning patterns.
- **Larger Dataset for Fine-Tuning**: Using Gemini to generate a larger pseudo-dataset ensures that the fine-tuning process for GPT-4o has enough diverse training data to generalize well to new papers.

---

### Summary Conclusion

By combining **Google Gemini Pro 1.5** for entity and passage extraction with **fine-tuned GPT-4o** for reasoning-based classification, and incorporating **manually categorized data** as a foundation, we can create a robust and flexible classification system. The multi-step approach to hierarchical classification, combined with longer category definitions and a carefully weighted evaluation of the paper’s components, ensures high accuracy and consistency across a wide range of papers.

---

# Embeddings and Comparisons in the Classification System

In this section, we’ll delve deeper into how **embeddings** play a crucial role in the comparison process and outline the specific roles that each part of the chain system will take on. This expands on the concept of using multiple steps and embedding-based techniques to enhance the accuracy and robustness of the classification system.

### Embedding Comparisons and Reliability

When working with embeddings of varying content sizes—such as comparing the rich content of a research paper to shorter category labels—the system needs to carefully balance the comparison. Here’s how the three main embedding techniques work together:

#### 1. **Longer Definition Embeddings for Categories**
We use detailed descriptions for categories, resulting in **richer embeddings**. These definitions help resolve the issue of comparing the content-rich embeddings of papers with short, abstract category labels. By giving the category embeddings a broader context, the system is less likely to rely on oversimplified comparisons and can instead match against more meaningful semantic representations.

#### 2. **Combining and Weighing Embeddings for Paper Content**
The content of the paper—**entities, keywords, key passages**—is combined into a **weighted vector**. By assigning weights to each component (e.g., giving more weight to key entities), we ensure that the classification decision emphasizes the most relevant aspects of the paper. This method ensures that the model gives priority to critical content like technical concepts or methodologies while still accounting for supporting details such as keywords or contextual passages.

The goal is to avoid overcomplicating comparisons by using a direct, balanced approach where each component is given the weight it deserves based on its relevance.

#### 3. **Multi-Step Evaluation**
The system evaluates individual parts of the paper—entities, keywords, passages—and compares them separately to the **category embeddings**. This granular breakdown ensures that mismatches in one aspect don’t affect the entire classification. After the individual comparisons, the results are combined to reach the final decision.

### Addressing Content Length Disparity in Comparisons

When comparing embeddings from papers (rich in content) with shorter category descriptions, there’s a risk that the paper’s detail will overwhelm the comparison. Here’s how this issue is mitigated:

1. **Detailed Category Definitions**: By expanding category labels into longer descriptions, the system can make more balanced comparisons with the content-heavy embeddings of the paper. These expanded definitions ensure that even nuanced content from the paper can align with the appropriate category context.
  
2. **Summarization as a Backup**: Although summarizing the paper is risky due to the potential loss of key information, it could serve as a **secondary step** to simplify the comparison if necessary. Summarization should focus on core research contributions to maintain classification accuracy.

3. **Stepwise Embedding Weighing**: Rather than embedding the entire content at once, the system weighs each feature (entities, keywords, passages) individually, ensuring that relevant aspects are highlighted in the comparison.

---

# Chain System Outline: Roles and Responsibilities

The chain system operates in a structured manner, breaking down the classification process into smaller tasks that each layer is responsible for. Here’s the detailed outline of what each part of the chain is responsible for:

### Step 1: **Entity and Passage Extraction with Google Gemini Pro 1.5**

**Role**: Extract key entities and passages from research papers.
- **Reason**: Google Gemini’s 2 million token context window allows for the extraction of detailed and comprehensive content from the paper without overlooking any key information.
- **Output**: The extracted entities (core concepts, methodologies) and passages (relevant sections of the paper such as the abstract, introduction, and conclusions) will be passed to the next step in the chain for classification.

### Step 2: **Combining and Weighing Extracted Embeddings**
  
**Role**: Take the output from Gemini (entities, keywords, and key passages) and generate a combined embedding, where each feature is weighted based on its importance to the classification process.
- **Entities**: Given more weight, as they directly reflect the paper’s core concepts.
- **Keywords**: Provide supporting context and are given moderate weight.
- **Passages**: Help to confirm and reinforce the classification, ensuring that the entities and keywords align with the broader context.

### Step 3: **Longer Definition Embedding Generation**

**Role**: Generate the embedding for the **longer definitions of each category**.
- **Reason**: Ensures that category embeddings are detailed enough to match the complexity of the paper content.
- **Output**: Rich, context-heavy category embeddings will be passed to the next step for comparison with the paper’s combined embeddings.

### Step 4: **Multi-Step Evaluation of Categories**

**Role**: Compare the paper’s content (extracted entities, keywords, passages) to the **predefined category embeddings** at each level of the hierarchy (Area, Broad, Major, Detailed).
- **Step-by-Step Evaluation**:
   1. **Area of Study Classification**: Compare the combined embeddings of the paper to the detailed category definitions of each Area of Study.
   2. **Broad Category Classification**: Once the Area is determined, compare the paper to the Broad categories within that Area.
   3. **Major Category Classification**: Narrow the paper’s classification by comparing its content to the Major categories within the selected Broad category.
   4. **Detailed Category Classification**: Finally, assign the paper to one or more Detailed categories within the selected Major categories.

### Step 5: **Final Reasoning with Fine-Tuned GPT-4o**

**Role**: Fine-tuned GPT-4o performs the **reasoning-based classification** using the pseudo-dataset generated from manual categorization. After all individual components have been processed and classified, GPT-4o verifies and refines the final output.
- **Reason**: To ensure that the classifier can reason effectively across multiple hierarchical levels and handle edge cases where classification is less clear.
- **Output**: Final hierarchical classification (Area, Broad, Major, Detailed).

---

### Chain System Summary Conclusion

By utilizing **multi-step evaluations**, **combined and weighted embeddings**, and **longer category definitions**, this system creates a robust framework for hierarchical classification. Each component of the chain has a clear role, ensuring that the content extracted from papers is accurately compared with detailed category embeddings, leading to reliable and precise classifications.

- **Multi-step evaluation** ensures that mismatches in one layer don’t propagate through the system.
- **Combined and weighted embeddings** allow for nuanced and detailed comparisons that emphasize key elements without losing important context.
- **Longer category definitions** provide richer comparison points, minimizing misclassifications due to the abstract nature of category labels.

Additionally we may expiriment with Quantizing embeddings to see if this caputres more of the core semantic meaning of the paper while eliminating technical minutia present in methodologies. See [Experimenting with Quantized Document Embeddings](quantizing_docs.md) for more information.

# Overall Summary

After considering the various techniques, methodologies, and potential optimizations for the research paper classification system, the final system will integrate several advanced strategies to ensure robust and efficient performance.

### 1. **Longer Definition Embedding and Custom Category Comparisons**
The use of **longer definition embeddings** ensures that category definitions align with our precise understanding of each category. This technique allows us to create richer embeddings that match the complexity of the research papers, reducing the risk of misclassifications due to overly abstract category labels. This method will be particularly useful when aligning the system with the **hierarchical category structure**.

### 2. **Combining and Weighing Embeddings for Paper Content**
By **combining and weighing embeddings** for different aspects of the paper (entities, keywords, key passages), the system can balance multiple sources of information to arrive at a more nuanced and accurate classification. The weighted approach ensures that **critical content** is emphasized while still considering supporting details. This method allows for a more **comprehensive evaluation** of the paper, leading to better classification accuracy.

### 3. **Multi-Step Evaluation for Hierarchical Classification**
The classification system uses a **multi-step evaluation** approach to break down the classification process into distinct levels: **Area of Study**, **Broad categories**, **Major categories**, and **Detailed categories**. Each level is addressed separately, ensuring that the system can handle papers with multiple classifications at the lower levels while keeping the higher levels distinct.

### 4. [**Quantization as an Experiment for Efficiency**](quantizing_docs.md)
The potential use of **quantized embeddings** offers an interesting experiment in terms of **simplifying content** and improving classification speed. By reducing the precision of the embeddings, we hypothesize that less relevant details may be filtered out, allowing the system to focus on the broader message of the paper. While this could provide gains in computational efficiency and high-level classification accuracy, we must balance this against the potential loss of precision in more detailed categories.

# Final Thoughts:
By combining these techniques—custom category embeddings, multi-step evaluation, weighted content analysis, and potential [quantization](quantizing_docs.md)—the classification system is designed to be both **accurate** and **efficient**. It will prioritize control over category definitions, handle the complexity of research papers, and allow for flexible optimization (like quantization) where appropriate. This multi-layered approach ensures that the system can adapt to various research domains and provide reliable, high-quality classifications across different levels of detail.
