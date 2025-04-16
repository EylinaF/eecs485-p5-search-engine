"""Initialization for the search."""
from flask import Flask
from search import config
from search.views import bp as views_bp

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(views_bp)
