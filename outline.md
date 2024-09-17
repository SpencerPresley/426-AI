Note: The taxonomy referenced in this document can be found [here](https://github.com/SpencerPresley/426-Taxonomy-Generator/blob/5146f00796c1dc870436712944ceda5e616c7a7c/GetCategoryHierarchy/data/taxonomyJson/taxonomy_hierarchy.json).

# AI Framework Outline

## Overview

This framework leverages AI to categorize research papers into a hierarchical taxonomy. The taxonomy is structured as a tree, where each node represents a category, and child nodes represent subcategories.

Each research paper will be assigned to a node in the tree, with the node's value corresponding to the paper's category. The AI will traverse the tree, analyzing the paper's content to make decisions at each branching point, selecting the most appropriate path.

The taxonomy hierarchy is structured as follows:

- **Top Level**: Area of Research
- **Second Level**: Broad Category
- **Third Level**: Major Category
- **Fourth Level**: Detailed Category

Each paper is assigned to a single Area of Research but can belong to one or more Broad, Major, and Detailed categories.

### Example:

**Paper**: "Attention is All You Need"  
- **Area of Research**: Sciences  
- **Broad Category**: Computer Science  
- **Major Category**: Deep Learning  
- **Detailed Category**: Transformers  

We will be using various LLMs and techniqes to achieve this. A brief list and description of a few niche techniques we will be using can be found here: [Techniques](techniques.md) while the main summary of the entire AI system including most important details and our plans on handling challenges during implementation can be found here: [AI System Overview](system.md).


