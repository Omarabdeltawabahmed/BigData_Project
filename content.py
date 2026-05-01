import requests
from bs4 import BeautifulSoup
import os
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

if not os.path.exists("docs"):
    os.makedirs("docs")

with open("links.txt", "r", encoding="utf-8") as f:
    links = f.readlines()

doc_map = {}

for i, link in enumerate(links):
    link = link.strip()

    try:
        res = requests.get(link, headers=headers, timeout=10)

        if res.status_code != 200:
            continue

        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()

        filename = f"doc{i}.txt"

        with open(f"docs/{filename}", "w", encoding="utf-8") as file:
            file.write(text)

        doc_map[filename] = link

        print(f"Saved: {filename}")

        time.sleep(1)

    except Exception as e:
        print(f"Error in {link}")
        continue

with open("doc_map.json", "w", encoding="utf-8") as f:
    json.dump(doc_map, f, indent=4)

print("Scraping Finished ")
