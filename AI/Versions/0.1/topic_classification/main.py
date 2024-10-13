from chains.top_chain import process_top_classification_chain_map
import json
import os
from utils import Taxonomy

file_name = input("Please Enter the file name: ")
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
abstracts_file = os.path.join(data_dir, file_name)
with open(abstracts_file, "r") as f:
    titleAbstracts = json.load(f)

taxonomy = Taxonomy()
subset = {}
for i, (title, abstract) in enumerate(titleAbstracts.items()):
    if i < 10:
        subset[title] = abstract

process_top_classification_chain_map(subset, taxonomy)