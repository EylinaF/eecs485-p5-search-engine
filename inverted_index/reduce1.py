#!/usr/bin/env python3
"""Reduce 1."""
import sys
import itertools

def main():
    """Group by doc_id and emit merged content."""
    for doc_id, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(doc_id, group)

def keyfunc(line):
    """Extract the doc_id (key) from a tab-delimited line."""
    return line.partition("\t")[0]

def reduce_one_group(doc_id, group):
    """Combine lines for a single doc_id and output cleaned content."""
    terms = []
    for line in group:
        _, _, content = line.partition("\t")
        terms.append(content.strip())
    merged_terms = " ".join(terms)
    print(f"{doc_id}\t{merged_terms}")

if __name__ == "__main__":
    main()