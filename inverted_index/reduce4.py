#!/usr/bin/env python3
"""Reduce 4: Normalize tf-idf for docs, emit final inverted index format."""

import sys
import math


def main():
    """Initialize main for reduce 4."""
    current_doc_id = None
    entries = {}

    for line in sys.stdin:
        docid, rest = line.rstrip("\n").split("\t", 1)

        if current_doc_id is not None and docid != current_doc_id:
            norm = math.sqrt(sum(val[2] ** 2 for val in entries.values()))
            for term in sorted(entries.keys()):
                idf_val, tf_val, _ = entries[term]
                print(f"{term} {idf_val} {current_doc_id} {tf_val} {norm}")
            entries = {}

        term, idf, tf, tfidf = rest.split()
        entries[term] = (float(idf), int(tf), float(tfidf))
        current_doc_id = docid

    if current_doc_id is not None:
        norm = math.sqrt(sum(val[2] ** 2 for val in entries.values()))
        for term in sorted(entries.keys()):
            idf_val, tf_val, _ = entries[term]
            print(f"{term} {idf_val} {current_doc_id} {tf_val} {norm}")


if __name__ == "__main__":
    main()
