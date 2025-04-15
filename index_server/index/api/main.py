from index import app
from pathlib import Path
from flask import Flask, request, jsonify
import math
import re


INVERTED_INDEX = {}
PAGERANK = {}
STOPWORDS = set()

def load_index(index_path):
    stopwords_path = Path(__file__).parent.parent / "stopwords.txt"
    with open(stopwords_path, "r") as f:
        for line in f:
            STOPWORDS.add(line.strip())

    pagerank_path = Path(__file__).parent.parent / "pagerank.out"
    with open(pagerank_path, "r") as f:
        for line in f:
            docid, score = line.strip().split(",")
            PAGERANK[int(docid)] = float(score)
    
    with open(index_path, "r") as f:
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
    return jsonify({
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    })

@app.route("/api/v1/hits/")
def get_hits():
    query_string = request.args.get("q", "")
    query_string = re.sub(r"[^a-zA-Z0-9 ]+", "", query_string)
    pagerank_weight = float(request.args.get("w", 0.5))

    # --- Clean query --- 
    tokens = query_string.lower().split()
    query_terms = [t for t in tokens if t not in STOPWORDS]
    if any(t not in INVERTED_INDEX for t in query_terms):
        return jsonify({"hits": []})
    
    # --- Build query vector ---
    # query frequency
    query_tf = {}
    for term in query_terms:
        query_tf[term] = query_tf.get(term, 0) + 1
    
    query_vec = {}
    for term in query_terms:
        idf = INVERTED_INDEX[term]["idf"]
        query_vec[term] = query_tf[term] * idf

    query_norm = math.sqrt(sum(weight**2 for weight in query_vec.values()))
    if query_norm == 0:
        query_norm = 1.0
    
    for term in query_vec:
        query_vec[term] /= query_norm

    # --- Build document vector ---
    # Gather candidate document
    doc_scores = {}
    candidate_docs = None
    for term in query_vec:
        postings = INVERTED_INDEX[term]["postings"]
        docs_with_term = set(postings.keys())

        if candidate_docs is None:
            candidate_docs = docs_with_term
        else:
            candidate_docs &= docs_with_term
    
    if not candidate_docs:
        return jsonify({"hits":[]})

    for docid in candidate_docs:
        cosSim = 0
        for term in query_vec:
            tf = INVERTED_INDEX[term]["postings"][docid]["tf"]
            norm = INVERTED_INDEX[term]["postings"][docid]["norm"]
            idf = INVERTED_INDEX[term]["idf"]

            cosSim += query_vec[term] * (tf * idf / norm)
        
        pagerank = PAGERANK.get(docid, 0.0)
        score = pagerank_weight * pagerank + (1 - pagerank_weight) * cosSim

        doc_scores[docid] = score
    
    hits = [{"docid": docid, "score": doc_scores[docid]} for docid in doc_scores]
    hits.sort(key=lambda x:x["score"], reverse=True)

    return jsonify({"hits": hits})


    
