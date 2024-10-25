import json
import pandas as pd
from abstract import abstracts

# Load the classification_results JSON data
with open('outputs/classification_results.json', 'r') as f:
    classification_results = json.load(f)

# Load the raw_classification_outputs JSON data
with open('outputs/raw_classification_outputs.json', 'r') as f:
    raw_classification_outputs = json.load(f)

# Open a file to log the output
with open('logs.txt', 'w') as log_file:
    # Initialize a list to hold data rows for the DataFrame
    data_rows = []

    # Iterate over each abstract in the classification_results
    for abstract_key, categories in classification_results.items():
        print(f"\n\nProcessing abstract: {abstract_key}", file=log_file)
        index = int(abstract_key.split('_')[1])
        abstract_text = abstracts[index]
        
        # Find the corresponding raw data for this abstract
        raw_data = raw_classification_outputs[index]
        print(f"\n\nRaw data: {raw_data}", file=log_file)

        # Iterate over each category in the classification_results
        def traverse_categories(cat_dict, parent_categories):
            for cat_name, sub_cats in cat_dict.items():
                current_categories = parent_categories + [cat_name]
                full_category = ', '.join(current_categories)
                print(f"\n\nTraversing category: {cat_name}", file=log_file)
                
                # Match the abstract and category in raw_classification_outputs
                category_reasoning = ''
                category_confidence = ''
                for classification in raw_data.get('classifications', []):
                    if abstract_text == classification.get('abstract') and cat_name in classification.get('categories', []):
                        category_reasoning = classification.get('reasoning', '')
                        category_confidence = classification.get('confidence_score', '')
                        break

                # Prepare the data row
                data_row = {
                    'Abstract Key': abstract_key,
                    'Abstract': abstract_text,
                    'Category': cat_name,
                    'Parent Categories': ', '.join(parent_categories),
                    'Reasoning': category_reasoning,
                    'Confidence Score': category_confidence,
                    'Reflection': raw_data.get('reflection', ''),
                    'Feedback': '; '.join([fb.get('feedback', '') for fb in raw_data.get('feedback', [])])
                }
                print(f"\n\nData row: {data_row}", file=log_file)
                data_rows.append(data_row)
                
                if isinstance(sub_cats, dict):
                    # Recurse with the subcategories
                    traverse_categories(sub_cats, current_categories)
        
        # Start traversing from the top-level categories
        traverse_categories(categories, [])

# Create a pandas DataFrame from the collected data
df = pd.DataFrame(data_rows)

# Export the DataFrame to a CSV file
df.to_excel('classification_output.xlsx', index=False)