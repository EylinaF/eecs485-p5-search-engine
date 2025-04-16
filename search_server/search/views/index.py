"""Initialization for the index page for search."""
from flask import Blueprint, request, render_template
from search.model import get_results

bp = Blueprint("views", __name__)


@bp.route("/", methods=["GET"])
def index():
    """Initialize for the index function."""
    query = request.args.get("q", "")
    weight = float(request.args.get("w", 0.5))

    results = []
    if query.strip():
        results = get_results(query, weight)

    return render_template("index.html", q=query, w=weight, results=results)
