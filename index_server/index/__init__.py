# ...
import index.api  # noqa: E402  pylint: disable=wrong-import-position
from flask import Flask
import os
from pathlib import Path

app = Flask(__name__)


INDEX_DIR = Path(__file__).parent/"inverted_index"
app.config["INDEX_PATH"] = os.getenv(
    "INDEX_PATH",  # Environment variable name
    INDEX_DIR/"inverted_index_1.txt"  # Default value
)

# Load inverted index, stopwords, and pagerank into memory
index.api.load_index(app.config["INDEX_PATH"])