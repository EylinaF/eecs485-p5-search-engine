"""Search result retrieval logic for the search server."""

import sqlite3
import threading
import heapq
import requests
from flask import current_app


def get_results(query, weight):
    """Fetch top 10 results."""
    api_urls = current_app.config["SEARCH_INDEX_SEGMENT_API_URLS"]
    raw_results = fetch_all_segments(api_urls, query, weight)
    top_docids = get_top_docids(raw_results, top_k=10)
    return get_metadata(top_docids)


def fetch_all_segments(api_urls, query, weight):
    """Fetch results concurrently from all index segment servers."""
    results = []
    threads = []
    lock = threading.Lock()

    def fetch(url):
        try:
            response = requests.get(
                url, params={"q": query, "w": weight}, timeout=5
            )
            response.raise_for_status()
            hits = response.json().get("hits", [])
            with lock:
                results.extend(hits)
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch from {url}: {e}")

    for url in api_urls:
        t = threading.Thread(target=fetch, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results


def get_top_docids(results, top_k=10):
    """Select top_k results, keeping highest score for each docid."""
    doc_scores = {}
    for item in results:
        docid = item["docid"]
        score = item["score"]
        if docid not in doc_scores or score > doc_scores[docid]:
            doc_scores[docid] = score
    return heapq.nlargest(top_k, doc_scores.items(), key=lambda x: x[1])


def get_metadata(docid_score_pairs):
    """Retrieve title, summary, and url from SQLite database."""
    db_path = "var/search.sqlite3"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    output = []
    for docid, score in docid_score_pairs:
        cur.execute(
            "SELECT title, summary, url FROM documents WHERE docid = ?",
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
