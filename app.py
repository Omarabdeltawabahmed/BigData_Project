import os
import json
import re
from flask import Flask, request, render_template
from collections import defaultdict

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(BASE_DIR, "docs")  

INDEX_PATH = os.path.join(BASE_DIR, "index.json")
MAP_PATH = os.path.join(BASE_DIR, "doc_map.json")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index = json.load(f)

with open(MAP_PATH, "r", encoding="utf-8") as f:
    doc_map = json.load(f)

@app.route("/", methods=["GET", "POST"])
def search():
    results = []
    query_string = ""

    if request.method == "POST":
        query_string = request.form.get("query", "").lower()
        query_words = re.findall(r'\b\w+\b', query_string)

        scores = defaultdict(int)

        for word in query_words:
            if word in index:
                for doc_id, count in index[word].items():
                    scores[doc_id] += count

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        for doc_id, score in sorted_docs:
            url = doc_map.get(doc_id)
            if url:
                results.append({
                    "url": url,
                    "score": score,
                    "id": doc_id
                })

    return render_template("index.html", results=results, query=query_string)


@app.route("/view/<doc_id>")
def view_file(doc_id):
    doc_id = doc_id.strip()  

    query = request.args.get("q", "")

    file_path = os.path.join(CORPUS_DIR, doc_id)

    print("Trying:", file_path) 

    if not os.path.exists(file_path):
        return f" الملف {doc_id} غير موجود في {CORPUS_DIR}", 404

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return render_template("view.html", content=content, query=query, doc_id=doc_id)


if __name__ == "__main__":
    app.run(debug=True)
