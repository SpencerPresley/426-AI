import json

with open('ALL_ABSTRACTS.json', 'r') as f:
    data = json.load(f)

num_abstracts = len(data['abstracts'])
print(f"Number of abstracts: {num_abstracts}")
