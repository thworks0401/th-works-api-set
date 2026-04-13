"""QRCode API — テキスト/URLからQRコード画像を生成"""
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Literal
import qrcode
import qrcode.image.pil
from io import BytesIO
from app.core.auth import verify_api_key

router = APIRouter()


class QRCodeRequest(BaseModel):
    data: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="QRコードにエンコードするテキストまたはURL",
        example="https://th-works.dev",
    )
    size: int = Field(10, ge=1, le=40, description="QRコードサイズ(box_size)。大きいほど高解像度")
    border: int = Field(4, ge=1, le=10, description="、マージン（ピクセル数）")
    error_correction: Literal["L", "M", "Q", "H"] = Field(
        "M",
        description="誤り訂正レベル: L=7%, M=15%, Q=25%, H=30%",
    )
    format: Literal["png", "jpeg"] = Field("png", description="出力画像形式")


EC_LEVELS = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}


@router.post("/qrcode", response_class=Response)
async def generate_qrcode(body: QRCodeRequest, _=Depends(verify_api_key)):
    """
    テキスト/URLからQRコード画像(PNG or JPEG)を生成して返す。
    Content-Type: image/png または image/jpeg でバイナリレスポンス。
    """
    qr = qrcode.QRCode(
        version=None,  # 自動
        error_correction=EC_LEVELS[body.error_correction],
        box_size=body.size,
        border=body.border,
    )
    qr.add_data(body.data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    fmt = body.format.upper()
    img.save(buf, format=fmt)
    buf.seek(0)

    media_type = f"image/{body.format}"
    return Response(content=buf.getvalue(), media_type=media_type)
