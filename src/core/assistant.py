"""
Friday — core orchestrator.
Receives a user query, fans out to scrapers/analysis, returns a synthesized answer.
"""
from __future__ import annotations


class Friday:
    def __init__(self) -> None:
        pass

    async def ask(self, query: str) -> dict:
        """Entry point for a natural-language query."""
        raise NotImplementedError
