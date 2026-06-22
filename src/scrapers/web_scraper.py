from __future__ import annotations
import asyncio
import httpx
import trafilatura
from src.utils.logger import logger

_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; FridayBot/1.0; +https://friday.ai)"}


class WebScraper:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            timeout=12.0,
            headers=_HEADERS,
            follow_redirects=True,
        )

    async def fetch(self, url: str) -> str:
        try:
            r = await self._client.get(url)
            r.raise_for_status()
            text = trafilatura.extract(
                r.text,
                include_comments=False,
                include_tables=False,
                no_fallback=False,
            )
            return text or ""
        except Exception as e:
            logger.warning(f"Web fetch failed [{url}]: {e}")
            return ""

    async def fetch_many(self, urls: list[str]) -> list[str]:
        return list(await asyncio.gather(*(self.fetch(u) for u in urls)))

    async def __aenter__(self): return self
    async def __aexit__(self, *_): await self._client.aclose()
