"""Trend detector — Google Trends, Reddit rising, and search signals."""
from __future__ import annotations


class TrendScraper:
    async def trending_topics(self, region: str = "US") -> list[dict]:
        raise NotImplementedError

    async def keyword_interest(self, keyword: str, timeframe: str = "now 1-d") -> dict:
        raise NotImplementedError
