# Friday — AI Intelligence Assistant

> *"Good morning. I am Friday, your personal AI assistant."*

Friday is an AI assistant inspired by Tony Stark's F.R.I.D.A.Y. — built to scan the web, aggregate live news, detect emerging trends, and surface exactly what you need in seconds.

---

## What Friday Does

- **Real-time web intelligence** — scrapes and analyzes web pages on demand
- **News aggregation** — pulls from multiple news sources and clusters related stories
- **Trend detection** — monitors social signals and search trends across the web
- **AI summarization** — condenses large amounts of information into actionable briefs
- **Query answering** — accepts natural language queries and returns synthesized answers with sources

---

## Project Structure

```
friday/
├── src/
│   ├── core/          # Assistant brain — orchestration & config
│   ├── scrapers/      # Web, news, and trend scrapers
│   ├── analysis/      # NLP, summarization, trend analysis
│   ├── api/           # REST API layer
│   └── utils/         # Logging, helpers
├── tests/             # Unit and integration tests
├── data/
│   ├── cache/         # Cached responses (gitignored)
│   └── logs/          # Runtime logs (gitignored)
├── docs/              # Architecture and design docs
└── scripts/           # Setup and utility scripts
```

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/friday.git
cd friday

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run Friday
python scripts/run.py
```

---

## Requirements

- Python 3.11+
- API keys: see `.env.example`

---

## Roadmap

- [ ] Web scraper with JS rendering support
- [ ] Multi-source news aggregator
- [ ] Trend detection engine (Google Trends, Reddit, X)
- [ ] LLM-powered summarization and Q&A
- [ ] REST API with WebSocket streaming
- [ ] Voice interface
- [ ] Dashboard UI

---

## License

MIT
