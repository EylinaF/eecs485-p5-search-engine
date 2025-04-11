"""Reduce 3: Group by term, compute IDF, and emit final inverted index lines."""
import sys
import math
from collections import defaultdict

with open("total_document_count.txt", "r") as f:
    total_docs = int(f.read().strip())

current_term = None
postings = []

for line in sys.stdin:
    term, value = line.strip().split("\t")
    doc_id, tf = value.split()
    tf = int(tf)

    if term != current_term and current_term is not None:
        n_k = len(postings)
        idf = math.log10(total_docs / n_k)

        postings.sort(key=lambda x: x[0])
        output_parts = [f"{current_term} {idf}"]
        for doc_id, tf in postings:
            output_parts.append(f"{doc_id} {tf}")
        print(f"{int(postings[0][0]) % 3}\t{' '.join(output_parts)}")

        postings = []

    postings.append((doc_id, tf))
    current_term = term

# Final term
if current_term is not None:
    n_k = len(postings)
    idf = math.log10(total_docs / n_k)
    postings.sort(key=lambda x: x[0])
    output_parts = [f"{current_term} {idf}"]
    for doc_id, tf in postings:
        output_parts.append(f"{doc_id} {tf}")
    print(f"{int(postings[0][0]) % 3}\t{' '.join(output_parts)}")