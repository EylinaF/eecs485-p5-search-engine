"""Initialization for the search model."""
import sqlite3
import threading
import heapq
import requests
from flask import current_app


def get_results(query, weight):
    """Initialize for get results."""
    api_urls = current_app.config["SEARCH_INDEX_SEGMENT_API_URLS"]
    db_path = "var/search.sqlite3"

    results = []
    threads = []
    lock = threading.Lock()

    def fetch_from_api(url):
        try:
            response = requests.get(url, params={"q": query, "w": weight})
            response.raise_for_status()
            data = response.json()["hits"]
            with lock:
                results.extend(data)
        except Exception as e:
            print(f"ERROR fetching from {url}: {e}")

    # Launch threads
    for url in api_urls:
        t = threading.Thread(target=fetch_from_api, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Merge and sort results
    doc_scores = {}
    for item in results:
        docid = item["docid"]
        score = item["score"]
        if docid not in doc_scores or score > doc_scores[docid]:
            doc_scores[docid] = score

    # Get top 10 docids sorted by score
    top_results = heapq.nlargest(10, doc_scores.items(), key=lambda x: x[1])

    # Load metadata from database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    output = []
    for docid, score in top_results:
        cur.execute(
            "SELECT title, summary, url FROM documents WHERE docid=?",
            (docid,)
        )
        row = cur.fetchone()
        if row:
            title, summary, url = row
            if not summary:
                summary = "No summary available"
            output.append({
                "docid": docid,
                "score": score,
                "title": title,
                "summary": summary,
                "url": url
            })
    conn.close()

    return output
