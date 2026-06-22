"""Entry point — starts the Friday API server."""
import uvicorn
from fastapi import FastAPI
from src.api.routes import router
from src.core.config import config

app = FastAPI(title="Friday", version="0.1.0")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT, reload=True)
