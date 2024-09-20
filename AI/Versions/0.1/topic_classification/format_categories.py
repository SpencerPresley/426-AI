import pandas as pd
import json
import os


print(taxonomy_df.columns)
for column in taxonomy_df.columns:
    # remove prefacing / trailing whitespace
    taxonomy_df[column] = taxonomy_df[column].str.strip()

print(taxonomy_df.columns)