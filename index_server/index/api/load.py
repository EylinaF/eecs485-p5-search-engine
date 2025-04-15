from pathlib import Path

INVERTED_INDEX = {}
PAGERANK = {}
STOPWORDS = set()

def load_index(index_path):
    stopwords_path = Path(__file__).parent.parent / "stopwords.txt"
    with open(stopwords_path, "r") as f:
        for line in f:
            STOPWORDS.add(line.strip())

    pagerank_path = Path(__file__).parent.parent / "pagerank.out"
    with open(pagerank_path, "r") as f:
        for line in f:
            docid, score = line.strip().split(",")
            PAGERANK[int(docid)] = float(score)
    
    with open(index_path, "r") as f:
        for line in f:
            tokens = line.strip().split()
            if len(tokens) < 2:
                continue
            term = tokens[0]
            idf = float(tokens[1])
            postings = {}
            for i in range(2, len(tokens), 3):
                docid = int(tokens[i])
                tf = int(tokens[i + 1])
                norm = float(tokens[i + 2])
                postings.append((docid, tf, norm))
            
            INVERTED_INDEX[term] = {
                "idf": idf,
                "postings": postings
            }



