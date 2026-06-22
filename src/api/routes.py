from fastapi import APIRouter
from src.api.models import QueryRequest
from src.core.assistant import Friday
from src.voice.tts import text_to_speech

router = APIRouter(prefix="/api/v1")

# Single shared instance (initialised once on startup)
_friday = Friday()


@router.post("/ask")
async def ask(req: QueryRequest) -> dict:
    result = await _friday.ask(req.query)

    audio_b64 = None
    if req.include_voice:
        audio_b64 = await text_to_speech(result["answer"])

    return {**result, "audio_b64": audio_b64}


@router.get("/news")
async def get_news(query: str = "", category: str = "") -> list[dict]:
    return await _friday.news.top_headlines(query, category)


@router.get("/trends")
async def get_trends(region: str = "US") -> list[dict]:
    return await _friday.trends.trending_topics(region)


@router.get("/health")
async def health() -> dict:
    return {"status": "online", "model": "claude-sonnet-4-6"}
