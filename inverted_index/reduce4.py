#!/usr/bin/env python3
"""Reduce 4: Normalize tf-idf for docs, emit final inverted index format."""
import sys
import math

current_docid = None
entries = {}

for line in sys.stdin:
    docid, rest = line.rstrip("\n").split("\t", 1)

    if current_docid is not None and docid != current_docid:
        norm = math.sqrt(sum(val[2] ** 2 for val in entries.values()))
        for term in sorted(entries.keys()):
            idf_val, tf_val, tfidf_val = entries[term]
            print(f"{term} {idf_val} {current_docid} {tf_val} {norm}")
        entries = {}

    term, idf, tf, tfidf = rest.split()
    entries[term] = (float(idf), int(tf), float(tfidf))
    current_docid = docid

# Final doc
if current_docid is not None:
    norm = math.sqrt(sum(val[2] ** 2 for val in entries.values()))
    for term in sorted(entries.keys()):
        idf_val, tf_val, tfidf_val = entries[term]
        print(f"{term} {idf_val} {current_docid} {tf_val} {norm}")
