#!/usr/bin/env python3
"""Reduce 5: Format final inverted index, sorted by term and then docid."""

import sys


def main():
    """Intialize reduce 5."""
    current_term = None
    idf = None
    postings = {}

    for line in sys.stdin:
        _, value = line.strip().split("\t")
        term, idf_str, docid, tf, norm = value.split()
        tf = int(tf)

        if current_term and term != current_term:
            output = [current_term, idf]
            for d in sorted(postings):
                tf_val, norm_val = postings[d]
                output.extend([d, str(tf_val), norm_val])
            print(" ".join(output))
            postings = {}

        current_term = term
        idf = idf_str
        postings[docid] = (tf, norm)

    if current_term:
        output = [current_term, idf]
        for docid in sorted(postings):
            tf_val, norm_val = postings[docid]
            output.extend([docid, str(tf_val), norm_val])
        print(" ".join(output))


if __name__ == "__main__":
    main()
