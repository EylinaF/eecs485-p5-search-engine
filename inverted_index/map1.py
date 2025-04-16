#!/usr/bin/env python3
"""Map 1."""

import sys
import re
import bs4


def main():
    """Initialize main for map1."""
    with open("stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = set(line.strip() for line in f)

    html = ""
    for line in sys.stdin:
        # Assume well-formed HTML docs:
        # - Starts with <!DOCTYPE html>
        # - End with </html>
        # - Contains a trailing newline
        if "<!DOCTYPE html>" in line:
            html = line
        else:
            html += line

        if "</html>" not in line:
            continue

        soup = bs4.BeautifulSoup(html, "html.parser")
        doc_id = soup.find(
            "meta", attrs={"eecs485_docid": True}
        ).get("eecs485_docid")

        element = soup.find("html")
        content = element.get_text(separator=" ", strip=True).replace("\n", "")

        content = re.sub(r"[^a-zA-Z0-9 ]+", "", content)
        content = content.casefold()
        terms = [term for term in content.split() if term not in stopwords]

        print(f"{doc_id}\t{' '.join(terms)}")


if __name__ == "__main__":
    main()
