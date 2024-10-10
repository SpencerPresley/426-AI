import json
abstracts = []

with open("data/ALL_ABSTRACTS.json", "r") as f:
    raw_abstracts = json.load(f)["abstracts"]

for abstract in raw_abstracts:
    if abstract == "" or abstract == None:
        continue
    abstracts.append(abstract)