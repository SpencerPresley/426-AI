import os
import json

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
abstracts_file = os.path.join(data_dir, "ALL_ABSTRACTS.json")
with open(abstracts_file, "r") as f:
    abstracts = json.load(f)["abstracts"]
    

def print_give_abstract(i: int):
    print(f"Abstract {i}:\n {abstracts[i]}\n")
    input("Press Enter to continue...")


print_give_abstract(196)
