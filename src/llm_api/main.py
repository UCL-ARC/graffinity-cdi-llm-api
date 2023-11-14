"""Entry point and main file for FastAPI app."""

from importlib import metadata

import uvicorn
from fastapi import FastAPI
from loguru import logger

from llm_api.routers import model_calling

logger.info("API starting")

description = """
Calls a large language model (LLM) with a preconstructed prompt
augmented by user search input. The LLM response is returned as JSON
with the most relevant entities from the search input extracted.
"""

app = FastAPI(
    title="LLM Search Entity Extraction API",
    description=description,
    version=metadata.version("llm-api"),
)

app.include_router(model_calling.router)


@app.get("/ping")
async def ping() -> dict[str, str]:
    """
    Provide a basic API route for testing purposes.

    Returns
    -------
        dict[str, str]: Dictionary containing response
    """
    return {"ping": "pong"}


if __name__ == "__main__":
    uvicorn.run(
        "llm_api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
