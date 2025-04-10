"""Map 0."""
import sys


for line in sys.stdin:
    if "<!DOCTYPE html>" in line:
        print("{count}\t1")
