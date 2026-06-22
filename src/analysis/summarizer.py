"""LLM-powered summarizer — condenses scraped content into concise briefs."""
from __future__ import annotations


class Summarizer:
    async def summarize(self, text: str, max_words: int = 150) -> str:
        raise NotImplementedError

    async def summarize_many(self, texts: list[str]) -> list[str]:
        raise NotImplementedError
