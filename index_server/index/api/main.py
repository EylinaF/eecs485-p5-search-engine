"""Initialization for the API main page."""

import re
import math
from pathlib import Path
from flask import request, jsonify
from index import app

INVERTED_INDEX = {}
PAGERANK = {}
STOPWORDS = set()


def load_index(index_path):
    """Load stopwords, PageRank scores, and inverted index."""
    stopwords_path = Path(__file__).parent.parent / "stopwords.txt"
    with open(stopwords_path, "r", encoding="utf-8") as f:
        for line in f:
            STOPWORDS.add(line.strip())

    pagerank_path = Path(__file__).parent.parent / "pagerank.out"
    with open(pagerank_path, "r", encoding="utf-8") as f:
        for line in f:
            docid, score = line.strip().split(",")
            PAGERANK[int(docid)] = float(score)

    with open(index_path, "r", encoding="utf-8") as f:
        for line in f:
            tokens = line.strip().split()
            if len(tokens) < 2:
                continue
            term = tokens[0]
            idf = float(tokens[1])
            postings = {}
            for i in range(2, len(tokens), 3):
                docid = int(tokens[i])
                tf = int(tokens[i + 1])
                norm = float(tokens[i + 2])
                postings[docid] = {"tf": tf, "norm": norm}

            INVERTED_INDEX[term] = {
                "idf": idf,
                "postings": postings
            }


@app.route("/api/v1/")
def list_services():
    """List available API services."""
    return jsonify({
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    })


@app.route("/api/v1/hits/")
def get_hits():
    """Return matching documents and scores for a query."""
    query_string = request.args.get("q", "")
    pagerank_weight = float(request.args.get("w", 0.5))
    query_string = re.sub(r"[^a-zA-Z0-9 ]+", "", query_string)

    tokens = query_string.casefold().split()
    query_terms = [t for t in tokens if t not in STOPWORDS]

    if any(t not in INVERTED_INDEX for t in query_terms):
        return jsonify({"hits": []})

    # --- Query vector ---
    query_tf = {}
    for term in query_terms:
        query_tf[term] = query_tf.get(term, 0) + 1

    query_vec = {}
    for term in query_terms:
        idf = INVERTED_INDEX[term]["idf"]
        query_vec[term] = query_tf[term] * idf

    query_norm = math.sqrt(sum(w ** 2 for w in query_vec.values())) or 1.0
    for term in query_vec:
        query_vec[term] /= query_norm

    # --- Document scoring ---
    doc_scores = {}
    candidate_docs = None
    for term in query_vec:
        postings = INVERTED_INDEX[term]["postings"]
        doc_ids = set(postings)
        candidate_docs = doc_ids if candidate_docs is None else candidate_docs & doc_ids

    if not candidate_docs:
        return jsonify({"hits": []})

    for docid in candidate_docs:
        cos_sim = 0.0
        for term, query_weight in query_vec.items():
            posting = INVERTED_INDEX[term]["postings"][docid]
            tf_idf = posting["tf"] * INVERTED_INDEX[term]["idf"] / posting["norm"]
            cos_sim += query_weight * tf_idf

        pagerank = PAGERANK.get(docid, 0.0)
        score = pagerank_weight * pagerank + (1 - pagerank_weight) * cos_sim
        doc_scores[docid] = score

    hits = [{"docid": docid, "score": score} for docid, score in doc_scores.items()]
    hits.sort(key=lambda x: x["score"], reverse=True)

    return jsonify({"hits": hits})
