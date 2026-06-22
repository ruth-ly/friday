"""Cross-source trend analysis — clusters and ranks signals."""
from __future__ import annotations


class TrendAnalyzer:
    def rank_topics(self, signals: list[dict]) -> list[dict]:
        raise NotImplementedError

    def cluster_stories(self, articles: list[dict]) -> list[list[dict]]:
        raise NotImplementedError
