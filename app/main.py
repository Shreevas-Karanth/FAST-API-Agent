from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import ollama

from app.agent import run_agent, MODEL


app = FastAPI(
    title="Local AI Agent API",
    description="A task assistant powered by Ollama",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="Question or instruction for the agent"
    )


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {
        "message": "Local AI Agent API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    try:
        ollama.show(MODEL)
        return {
            "status": "UP",
            "ollama": "CONNECTED",
            "model": MODEL
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Ollama is unavailable or the model is not installed"
        )


@app.post("/agent/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = run_agent(request.message)
        return ChatResponse(answer=answer)

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="The AI agent could not complete the request"
        )