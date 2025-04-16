#!/usr/bin/env python3
"""Map 2: Calculate the term frequency."""

import sys
from collections import defaultdict

for line in sys.stdin:
    doc_id, _, content = line.partition("\t")
    terms = content.strip().split()

    tf_counts = defaultdict(int)
    for term in terms:
        tf_counts[term] += 1

    for term, tf in tf_counts.items():
        print(f"{term}\t{doc_id} {tf}")
