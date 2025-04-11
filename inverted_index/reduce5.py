#!/usr/bin/env python3
"""Reduce 5: Format final inverted index, sorted by term and then docid."""
import sys
from collections import defaultdict

current_term = None
idf = None
postings = {}

for line in sys.stdin:
    key, value = line.strip().split("\t")
    term, idf_str, docid, tf, norm = value.split()
    tf = int(tf)

    if current_term and term != current_term:
        output = [current_term, idf]
        for docid in sorted(postings.keys()):
            tf_val, norm_val = postings[docid]
            output.extend([docid, str(tf_val), norm_val])
        print(" ".join(output))
        postings = {}

    current_term = term
    idf = idf_str
    postings[docid] = (tf, norm)

# Emit last term
if current_term:
    output = [current_term, idf]
    for docid in sorted(postings.keys()):
        tf_val, norm_val = postings[docid]
        output.extend([docid, str(tf_val), norm_val])
    print(" ".join(output))
