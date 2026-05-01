import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

visited = set()
to_visit = ["https://en.wikipedia.org/wiki/Main_Page"]
all_links_set = set() 
all_links_list = []
base_url = "https://en.wikipedia.org"

while to_visit and len(all_links_list) < 1000:
    url = to_visit.pop(0)

    if url in visited:
        continue

    visited.add(url)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            continue
            
        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            if len(all_links_list) >= 1000:
                break
                
            href = link.get("href")
            full_url = urljoin(base_url, href)
            
            if full_url.startswith("https://en.wikipedia.org/wiki/") and full_url not in visited and full_url not in all_links_set:
                all_links_set.add(full_url)
                all_links_list.append(full_url)
                to_visit.append(full_url)

    except Exception as e:
        continue

print(f"Total Unique Links Collected: {len(all_links_list)}")

with open("links.txt", "w", encoding="utf-8") as f:
    for link in all_links_list:
        f.write(link + "\n")