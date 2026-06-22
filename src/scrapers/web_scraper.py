"""General-purpose web scraper with JS rendering support via Playwright."""
from __future__ import annotations


class WebScraper:
    async def fetch(self, url: str) -> str:
        """Fetch and extract clean text from a URL."""
        raise NotImplementedError

    async def fetch_many(self, urls: list[str]) -> list[str]:
        raise NotImplementedError
