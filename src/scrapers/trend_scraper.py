"""
Trend detector — Google Trends via pytrends (runs in a thread to avoid blocking).
"""
from __future__ import annotations
import asyncio
from src.utils.logger import logger


class TrendScraper:
    async def trending_topics(self, region: str = "US") -> list[dict]:
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._fetch_trending, region)
        except Exception as e:
            logger.warning(f"Trend fetch error: {e}")
            return []

    async def keyword_interest(self, keyword: str, timeframe: str = "now 1-d") -> dict:
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._keyword_interest, keyword, timeframe)
        except Exception as e:
            logger.warning(f"Keyword interest error: {e}")
            return {}

    def _fetch_trending(self, region: str) -> list[dict]:
        try:
            from pytrends.request import TrendReq
            pt = TrendReq(hl="en-US", tz=360, timeout=(5, 10))
            df = pt.trending_searches(pn=region.lower())
            return [{"topic": str(row[0])} for _, row in df.head(10).iterrows()]
        except Exception as e:
            logger.warning(f"pytrends trending error: {e}")
            return []

    def _keyword_interest(self, keyword: str, timeframe: str) -> dict:
        try:
            from pytrends.request import TrendReq
            pt = TrendReq(hl="en-US", tz=360, timeout=(5, 10))
            pt.build_payload([keyword], timeframe=timeframe)
            df = pt.interest_over_time()
            if df.empty:
                return {}
            return {"keyword": keyword, "interest": df[keyword].tolist()}
        except Exception as e:
            logger.warning(f"pytrends keyword error: {e}")
            return {}
