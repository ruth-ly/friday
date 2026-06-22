"""News aggregator — pulls headlines from NewsAPI, RSS feeds, and The Guardian."""
from __future__ import annotations


class NewsScraper:
    async def top_headlines(self, query: str = "", category: str = "") -> list[dict]:
        raise NotImplementedError

    async def search(self, query: str, days_back: int = 1) -> list[dict]:
        raise NotImplementedError
