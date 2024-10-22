import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.paper_metadata_model import abstracts

print(abstracts)
input("Press Enter to continue...")
# abstracts = []

# with open("../data/ALL_ABSTRACTS.json", "r") as f:
#     raw_abstracts = json.load(f)["abstracts"]

# for abstract in raw_abstracts:
#     if abstract == "" or abstract == None:
#         continue
#     abstracts.append(abstract)
