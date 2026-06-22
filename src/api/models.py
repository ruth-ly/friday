from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    max_sources: int = 10
    include_trends: bool = True


class Source(BaseModel):
    title: str
    url: str
    snippet: str
    published_at: str | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
    trending: list[str] = []
