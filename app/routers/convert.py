"""Convert API — Markdown→HTML変換"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
import markdown
from app.core.auth import verify_api_key

router = APIRouter()


class MdConvertRequest(BaseModel):
    markdown_text: str = Field(
        ...,
        min_length=1,
        max_length=50_000,
        description="変換するMarkdownテキスト",
        example="# Hello\n\nThis is **bold** text.",
    )
    extensions: list[str] = Field(
        default=["tables", "fenced_code", "toc"],
        description="使用するMarkdown拡張機能",
    )


class MdConvertResponse(BaseModel):
    html: str
    char_count_input: int
    char_count_output: int


@router.post("/convert/md2html", response_model=MdConvertResponse)
async def md_to_html(body: MdConvertRequest, _=Depends(verify_api_key)):
    """
    MarkdownテキストをHTMLに変換する。
    tables, fenced_code, tocなどの拡張も指定可能。
    """
    html = markdown.markdown(body.markdown_text, extensions=body.extensions)
    return MdConvertResponse(
        html=html,
        char_count_input=len(body.markdown_text),
        char_count_output=len(html),
    )
