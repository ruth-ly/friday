"""NLP utilities — entity extraction, keyword detection, sentiment."""
from __future__ import annotations


class NLPProcessor:
    def extract_keywords(self, text: str) -> list[str]:
        raise NotImplementedError

    def extract_entities(self, text: str) -> dict:
        raise NotImplementedError

    def sentiment(self, text: str) -> str:
        raise NotImplementedError
