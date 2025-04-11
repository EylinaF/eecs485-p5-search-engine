#!/usr/bin/env python3
"""Map 5: Assign terms to segments based on doc_id % 3."""
import sys

for line in sys.stdin:
    term, idf, doc_id, tf, norm = line.strip().split()
    segment = int(doc_id) % 3
    print(f"{segment}\t{term} {idf} {doc_id} {tf} {norm}")