import datetime
from typing import List

import feedparser
import requests


FEEDS = [
    ("BBC", "http://feeds.bbci.co.uk/news/rss.xml"),
    ("Reuters", "http://feeds.reuters.com/reuters/topNews"),
    ("Hacker News", "https://news.ycombinator.com/rss"),
    ("TechCrunch", "http://feeds.feedburner.com/TechCrunch/"),
]


def _is_recent(entry_date: datetime.datetime) -> bool:
    now = datetime.datetime.now(datetime.timezone.utc)
    return now - entry_date < datetime.timedelta(days=1)


def _parse_entry(entry: dict) -> dict:
    title = entry.get("title", "").strip()
    link = entry.get("link", "").strip()
    description = entry.get("summary", entry.get("description", "")).strip()
    published = entry.get("published_parsed")

    if published:
        entry_date = datetime.datetime(*published[:6], tzinfo=datetime.timezone.utc)
    else:
        entry_date = datetime.datetime.now(datetime.timezone.utc)

    return {
        "title": title,
        "link": link,
        "description": description,
        "published": entry_date,
    }


def fetch_news(limit: int = 8) -> List[dict]:
    articles = []
    seen_links = set()

    for name, url in FEEDS:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
        except Exception:
            continue

        for entry in feed.entries:
            article = _parse_entry(entry)
            if article["link"] in seen_links:
                continue

            if article["title"] and _is_recent(article["published"]):
                articles.append(article)
                seen_links.add(article["link"])

            if len(articles) >= limit:
                break

        if len(articles) >= limit:
            break

    return articles[:limit]
