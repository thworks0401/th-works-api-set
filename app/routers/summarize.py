"""Summarize API — テキスト要約（Ollama ローカル利用）"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from app.core.auth import verify_api_key
from app.core.config import settings
import httpx

router = APIRouter()


class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=50,
        max_length=10_000,
        description="要約するテキスト（最低50文字）",
    )
    max_length: int = Field(
        200,
        ge=50,
        le=500,
        description="要約の最大文字数",
    )


class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    model_used: str


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(body: SummarizeRequest, _=Depends(verify_api_key)):
    """
    Ollamaローカルモデルでテキストを要約する。
    Ollamaが起動していない場合は503を返す。
    """
    prompt = (
        f"以下のテキストを日本語で{body.max_length}文字以内に要約してください。"
        f"要点のみを簡潔にまとめてください:\n\n{body.text}"
    )
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            summary = data.get("response", "").strip()
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Ollamaに接続できません。起動してから再度お試しください: {settings.OLLAMA_BASE_URL}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return SummarizeResponse(
        summary=summary,
        original_length=len(body.text),
        summary_length=len(summary),
        model_used=settings.OLLAMA_MODEL,
    )
