from fastapi import APIRouter
from src.api.models import QueryRequest, QueryResponse

router = APIRouter(prefix="/api/v1")


@router.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest) -> QueryResponse:
    raise NotImplementedError


@router.get("/news")
async def get_news(query: str = "", category: str = "") -> list[dict]:
    raise NotImplementedError


@router.get("/trends")
async def get_trends(region: str = "US") -> list[dict]:
    raise NotImplementedError
