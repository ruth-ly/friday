"""
News aggregator — NewsAPI primary, RSS fallback.
"""
from __future__ import annotations
from datetime import datetime, timedelta
import httpx
import feedparser
from src.core.config import config
from src.utils.logger import logger

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://techcrunch.com/feed/",
    "https://feeds.reuters.com/reuters/technologyNews",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
]


class NewsScraper:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=10.0, follow_redirects=True)

    async def top_headlines(self, query: str = "", category: str = "") -> list[dict]:
        if config.NEWS_API_KEY:
            return await self._newsapi(
                endpoint="top-headlines",
                params={"q": query, "category": category, "language": "en", "pageSize": 10},
            )
        return await self._rss()

    async def search(self, query: str, days_back: int = 1) -> list[dict]:
        if not query.strip():
            return await self.top_headlines()
        if config.NEWS_API_KEY:
            from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            return await self._newsapi(
                endpoint="everything",
                params={
                    "q": query,
                    "from": from_date,
                    "sortBy": "relevancy",
                    "language": "en",
                    "pageSize": 10,
                },
            )
        return await self._rss()

    async def _newsapi(self, endpoint: str, params: dict) -> list[dict]:
        params = {k: v for k, v in params.items() if v}
        params["apiKey"] = config.NEWS_API_KEY
        try:
            r = await self._client.get(f"https://newsapi.org/v2/{endpoint}", params=params)
            r.raise_for_status()
            return r.json().get("articles", [])
        except Exception as e:
            logger.warning(f"NewsAPI error: {e}")
            return await self._rss()

    async def _rss(self) -> list[dict]:
        articles: list[dict] = []
        for url in RSS_FEEDS:
            try:
                r = await self._client.get(url)
                feed = feedparser.parse(r.text)
                for entry in feed.entries[:4]:
                    articles.append({
                        "title":       entry.get("title", ""),
                        "url":         entry.get("link", ""),
                        "description": entry.get("summary", ""),
                        "publishedAt": entry.get("published", ""),
                        "source":      {"name": feed.feed.get("title", url)},
                    })
            except Exception as e:
                logger.warning(f"RSS error [{url}]: {e}")
        return articles
