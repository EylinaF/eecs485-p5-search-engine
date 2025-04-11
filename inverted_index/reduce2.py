"""Reduce 2: sort the term"""
import sys

current_term = None
entries = []

for line in sys.stdin:
    key, tf = line.strip().split("\t")
    doc_id, term = key.split()
    tf = int(tf)

    if term != current_term and current_term is not None:
        for doc_id, tf in sorted(entries, key=lambda x: x[0]):
            print(f"{current_term}\t{doc_id} {tf}")
        entries = []

    entries.append((doc_id, tf))
    current_term = term

if current_term is not None:
    for doc_id, tf in sorted(entries, key=lambda x: x[0]):
        print(f"{current_term}\t{doc_id} {tf}")
