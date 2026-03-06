# tests/test_news.py
from unittest.mock import patch, MagicMock
from tools.news import get_news


def test_get_news_returns_headlines():
    mock_entry = MagicMock()
    mock_entry.title = "AI Makes Breakthrough"
    mock_entry.link = "https://example.com/article"

    mock_feed = MagicMock()
    mock_feed.entries = [mock_entry]

    with patch("tools.news.feedparser.parse", return_value=mock_feed):
        result = get_news()

    assert "AI Makes Breakthrough" in result
    assert "https://example.com/article" in result
    assert isinstance(result, str)


def test_get_news_deduplicates_titles():
    mock_entry = MagicMock()
    mock_entry.title = "Duplicate Title"
    mock_entry.link = "https://example.com/1"

    mock_feed = MagicMock()
    mock_feed.entries = [mock_entry, mock_entry]  # same entry twice

    with patch("tools.news.feedparser.parse", return_value=mock_feed):
        result = get_news()

    assert result.count("Duplicate Title") == 1


def test_get_news_returns_fallback_when_no_entries():
    mock_feed = MagicMock()
    mock_feed.entries = []

    with patch("tools.news.feedparser.parse", return_value=mock_feed):
        result = get_news()

    assert result == "뉴스를 가져올 수 없습니다."
