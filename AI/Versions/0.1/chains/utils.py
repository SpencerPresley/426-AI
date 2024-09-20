import json
import os

def json_print_to_file(name, data):
    outputs_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
    methods_dir_path = os.path.join(outputs_dir_path, "method_extraction")
    sentence_analysis_dir_path = os.path.join(outputs_dir_path, "sentence_analysis")
    summary_dir_path = os.path.join(outputs_dir_path, "summary")
    
    output_dir = None
    if name.startswith("method_json_output"):
        output_dir = methods_dir_path
    elif name.startswith("abstract_chain_output"):
        output_dir = sentence_analysis_dir_path
    elif name.startswith("summary_chain_output"):
        output_dir = summary_dir_path
    else:
        raise ValueError(f"Invalid 'name' argument. Expected 'method_json_output', 'abstract_chain_output', or 'summary_chain_output'. Got:\n{name}")

    with open(os.path.join(output_dir, f"{name}.json"), "w") as f:
        json.dump(data, f, indent=4)