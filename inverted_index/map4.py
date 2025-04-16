#!/usr/bin/env python3
"""Map 4: sort using docid."""
import sys

entries = []

for line in sys.stdin:
    line = line.strip()
    docid, rest = line.split("\t", 1)
    entries.append((docid, rest))

entries.sort(key=lambda x: x[0])

for docid, rest in entries:
    print(f"{docid}\t{rest}")
