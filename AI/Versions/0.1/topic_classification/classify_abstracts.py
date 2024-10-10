from utils import Taxonomy
from abstract import abstracts
from chains import process_top_classification_chain
import os
import json

print(len(abstracts))
input("Press Enter to continue...")

taxonomy = Taxonomy()
method_json_outputs = []
abstract_chain_outputs = []
abstract_summary_outputs = []

process_top_classification_chain(abstracts, taxonomy)
