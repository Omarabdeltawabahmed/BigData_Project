import os
import json
import re
from collections import defaultdict

index = defaultdict(dict)

for file in os.listdir("docs"):
    with open(f"docs/{file}", "r", encoding="utf-8") as f:
        text = f.read().lower()
        words = re.findall(r'\b\w+\b', text)

        for word in words:
            if file not in index[word]:
                index[word][file] = 0
            index[word][file] += 1

with open("index.json", "w", encoding="utf-8") as f:
    json.dump(index, f)

print("Index Created ")