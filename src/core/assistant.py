"""
Friday core orchestrator — fans out to scrapers, synthesizes with Claude.
"""
from __future__ import annotations
import asyncio
import anthropic
from src.core.config import config
from src.scrapers.news_scraper import NewsScraper
from src.scrapers.trend_scraper import TrendScraper
from src.utils.logger import logger

_SYSTEM = (
    "You are F.R.I.D.A.Y. (Female Replacement Intelligent Digital Assistant Youth), "
    "Tony Stark's AI. You are precise, fast, and data-driven. "
    "When live news or trend context is supplied, use it to ground your answer. "
    "Be concise — under 120 words unless depth is genuinely needed. "
    "No filler, no fluff. Speak with quiet confidence."
)


class Friday:
    def __init__(self) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
        self.news    = NewsScraper()
        self.trends  = TrendScraper()

    async def ask(self, query: str) -> dict:
        logger.info(f"Query received: {query!r}")

        # Fan out concurrently
        news_res, trend_res = await asyncio.gather(
            self.news.search(query),
            self.trends.trending_topics(),
            return_exceptions=True,
        )
        articles = news_res  if isinstance(news_res,  list) else []
        trending = trend_res if isinstance(trend_res, list) else []

        context = _build_context(articles, trending)
        answer  = await self._synthesize(query, context)

        sources = [
            {
                "title":        a.get("title", ""),
                "url":          a.get("url", ""),
                "snippet":      a.get("description", ""),
                "published_at": a.get("publishedAt"),
            }
            for a in articles[:5]
        ]
        trend_labels = [
            t.get("topic", str(t)) if isinstance(t, dict) else str(t)
            for t in trending[:8]
        ]

        return {"answer": answer, "sources": sources, "trending": trend_labels}

    async def _synthesize(self, query: str, context: str) -> str:
        content = f"{context}\n\nQuery: {query}" if context else query
        msg = await self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=_SYSTEM,
            messages=[{"role": "user", "content": content}],
        )
        return msg.content[0].text


def _build_context(articles: list, trending: list) -> str:
    parts: list[str] = []
    if articles:
        parts.append("=== LIVE NEWS ===")
        for a in articles[:6]:
            title = a.get("title", "")
            desc  = a.get("description", "")
            parts.append(f"• {title}: {desc}"[:200])
    if trending:
        parts.append("\n=== TRENDING NOW ===")
        parts.append(", ".join(
            t.get("topic", str(t)) if isinstance(t, dict) else str(t)
            for t in trending[:10]
        ))
    return "\n".join(parts)
