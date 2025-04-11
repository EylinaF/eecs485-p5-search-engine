#!/usr/bin/env python3
"""Reduce 3: Group by term, compute IDF, and emit final inverted index lines."""
import sys
import math
from collections import defaultdict

with open("total_document_count.txt", "r") as f:
    total_docs = int(f.read().strip())

current_term = None
postings = {}

for line in sys.stdin:
    term, value = line.strip().split("\t")
    doc_id, tf= value.split()
    tf = int(tf)


    if term != current_term and current_term is not None:
        n_k = len(postings)
        idf = math.log10(total_docs / n_k)

        for d in sorted(postings.keys()):
            tf_val = postings[d]
            tfidf = tf_val * idf
            print(f"{d}\t{current_term} {idf} {tf_val} {tfidf}")
        postings = {}
            
    postings[doc_id] = tf
    current_term = term


# Final term
if current_term:
    n_k = len(postings)
    idf = math.log10(total_docs / n_k)
    for doc_id in sorted(postings.keys()):
        tf_val = postings[doc_id]
        tfidf = tf_val * idf
        print(f"{doc_id}\t{current_term} {idf} {tf_val} {tfidf}")