"""This is just a little script for summarizing these big JSON files."""

import json
import os

from textprobability.data.langdata import DefaultLangData

DATA_DIR = "./textprobability/data"

for filename in os.listdir(DATA_DIR):
    if not filename.endswith(".json"):
        continue
    path = os.path.join(DATA_DIR, filename)
    with open(path) as f:
        full_data = DefaultLangData.from_serializable(json.loads(f.read()))
    os.renames(path, os.path.join(DATA_DIR, "full", filename))
    with open(path, "w") as f:
        f.write(json.dumps(full_data.summarize(min_n=5).to_serializable()))
