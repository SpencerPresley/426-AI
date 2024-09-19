import json

def json_print_to_file(name, data):
    with open(f"{name}.json", "w") as f:
        json.dump(data, f, indent=4)