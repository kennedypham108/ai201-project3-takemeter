#!/usr/bin/env python3
"""
Collect public r/nba comments from LeBron-related threads and save them for manual labeling.

Run:
    python3 collect_reddit_data.py

Output:
    unlabeled_lebron_comments.csv

Important:
- Review every row yourself.
- Add exactly one of these labels:
  Evidence-Based Analysis
  Reasoned Opinion
  Hot Take or Reaction
"""

import csv
import html
import time
from typing import Dict, List, Set

import requests

USER_AGENT = "ai201-project3-dataset-collector/1.0 (educational use)"
HEADERS = {"User-Agent": USER_AGENT}

SEARCH_TERMS = [
    "LeBron retirement",
    "LeBron Lakers contract",
    "LeBron trade",
    "LeBron Luka",
    "LeBron Cleveland",
    "LeBron Warriors",
    "LeBron longevity",
    "LeBron GOAT",
    "LeBron Jordan",
    "LeBron salary",
    "LeBron defense",
    "LeBron playoffs",
    "LeBron legacy",
    "LeBron Bronny",
]

TARGET_COUNT = 220
MIN_LENGTH = 20
MAX_LENGTH = 1200


def get_json(url: str, params: Dict | None = None) -> Dict:
    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def search_threads(term: str, limit: int = 25) -> List[str]:
    data = get_json(
        "https://www.reddit.com/r/nba/search.json",
        {
            "q": term,
            "restrict_sr": "on",
            "sort": "relevance",
            "t": "all",
            "limit": limit,
            "raw_json": 1,
        },
    )

    permalinks = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        permalink = post.get("permalink")
        if permalink:
            permalinks.append(permalink)
    return permalinks


def flatten_comments(children: List[Dict], source_url: str, rows: List[Dict], seen: Set[str]) -> None:
    for child in children:
        if child.get("kind") != "t1":
            continue

        data = child.get("data", {})
        body = html.unescape(data.get("body", "")).strip()
        comment_id = data.get("id", "")

        if (
            body
            and body not in {"[deleted]", "[removed]"}
            and MIN_LENGTH <= len(body) <= MAX_LENGTH
            and comment_id not in seen
        ):
            seen.add(comment_id)
            rows.append(
                {
                    "text": " ".join(body.split()),
                    "label": "",
                    "source_url": source_url + comment_id + "/",
                    "notes": "",
                }
            )

        replies = data.get("replies")
        if isinstance(replies, dict):
            nested = replies.get("data", {}).get("children", [])
            flatten_comments(nested, source_url, rows, seen)


def collect_comments(permalink: str, rows: List[Dict], seen: Set[str]) -> None:
    url = f"https://www.reddit.com{permalink}.json"
    data = get_json(url, {"limit": 500, "depth": 8, "raw_json": 1})

    if not isinstance(data, list) or len(data) < 2:
        return

    source_url = f"https://www.reddit.com{permalink}"
    children = data[1].get("data", {}).get("children", [])
    flatten_comments(children, source_url, rows, seen)


def main() -> None:
    rows: List[Dict] = []
    seen: Set[str] = set()
    visited_threads: Set[str] = set()

    for term in SEARCH_TERMS:
        print(f"Searching: {term}")
        try:
            threads = search_threads(term)
        except requests.RequestException as exc:
            print(f"Search failed for {term}: {exc}")
            continue

        for permalink in threads:
            if permalink in visited_threads:
                continue
            visited_threads.add(permalink)

            try:
                collect_comments(permalink, rows, seen)
                print(f"Collected {len(rows)} comments")
            except requests.RequestException as exc:
                print(f"Thread failed: {exc}")

            if len(rows) >= TARGET_COUNT:
                break

            time.sleep(1)

        if len(rows) >= TARGET_COUNT:
            break

    rows = rows[:TARGET_COUNT]

    output = "unlabeled_lebron_comments.csv"
    with open(output, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["text", "label", "source_url", "notes"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} rows to {output}")
    if len(rows) < 200:
        print("Fewer than 200 comments were collected. Run again later or add comments manually.")


if __name__ == "__main__":
    main()
