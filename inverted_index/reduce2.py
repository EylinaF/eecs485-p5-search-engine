#!/usr/bin/env python3
"""Reduce 2: sort the term."""
import sys
from itertools import groupby


def keyfunc(line):
    """Initialize key function."""
    return line.split("\t")[0]


def main():
    """Initialize for reduce 2 worker."""
    for term, group in groupby(sys.stdin, key=keyfunc):
        postings = []
        for line in group:
            _, value = line.strip().split("\t")
            doc_id, tf = value.split()
            postings.append((doc_id, int(tf)))
        for doc_id, tf in sorted(postings, key=lambda x: x[0]):
            print(f"{term}\t{doc_id} {tf}")


if __name__ == "__main__":
    main()
