"""Reduce 0."""
import sys
import itertools


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def reduce_one_group(group):
    """Reduce one group."""
    total_count = 0
    for line in group:
        count = line.partition("\t")[2]
        total_count += int(count)
    print(f"{total_count}")


if __name__ == "__main__":
    main()
