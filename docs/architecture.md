# Friday — Architecture

## Overview

```
User Query
    │
    ▼
[Friday Core Orchestrator]
    │
    ├──► [Web Scraper]      ──► raw HTML/text
    ├──► [News Scraper]     ──► articles
    └──► [Trend Scraper]    ──► trending signals
              │
              ▼
    [Analysis Layer]
    ├──► NLP Processor      ──► entities, keywords
    ├──► Summarizer         ──► condensed text
    └──► Trend Analyzer     ──► ranked topics
              │
              ▼
    [LLM Synthesis]         ──► final answer + sources
              │
              ▼
    [REST API / WebSocket]  ──► client
```

## Key Design Decisions

- **Async-first**: all I/O is async via `asyncio` + `httpx`
- **Playwright** for JS-heavy pages; `trafilatura` for fast static extraction
- **Redis** for caching scraped content (TTL configurable)
- **FastAPI** for the API layer with automatic OpenAPI docs
- **Anthropic Claude** as the synthesis LLM

## Data Flow

1. Query arrives at `POST /api/v1/ask`
2. Orchestrator fans out scrape + news + trend jobs concurrently
3. Results are chunked and summarized per source
4. Final LLM call synthesizes a grounded answer with citations
5. Response streamed back to client
