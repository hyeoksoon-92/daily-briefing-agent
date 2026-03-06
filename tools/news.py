# tools/news.py
import feedparser

RSS_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch",
    "https://hnrss.org/frontpage",
    "https://www.reddit.com/r/programming/.rss",
]


def get_news(limit: int = 10) -> str:
    entries = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        entries.extend(feed.entries[:5])

    seen = set()
    lines = []
    for entry in entries:
        title = getattr(entry, "title", "").strip()
        link = getattr(entry, "link", "")
        if title and title not in seen:
            seen.add(title)
            lines.append(f"- {title}\n  {link}")
        if len(lines) >= limit:
            break

    return "\n".join(lines) if lines else "뉴스를 가져올 수 없습니다."
