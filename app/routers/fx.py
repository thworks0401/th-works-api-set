"""FX API — 為替レート取得（無料公開API使用）"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from app.core.auth import verify_api_key
import httpx
from datetime import datetime

router = APIRouter()

# サポート通貨一覧
SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "KRW"]
BASE_URL = "https://open.er-api.com/v6/latest"


class FxRatesResponse(BaseModel):
    base: str
    rates: dict[str, float]
    fetched_at: str


@router.get("/fx/rates", response_model=FxRatesResponse)
async def get_fx_rates(
    base: str = Query("JPY", description="基準通貨コード（例: JPY, USD）"),
    targets: list[str] = Query(
        default=SUPPORTED_CURRENCIES,
        description="取得する通貨コード一覧",
    ),
    _=Depends(verify_api_key),
):
    """
    指定基準通貨から各通貨への為替レートを取得する。
    無料公開API (open.er-api.com) を使用。
    """
    base = base.upper()
    if base not in SUPPORTED_CURRENCIES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported base currency: {base}. Supported: {SUPPORTED_CURRENCIES}",
        )
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{BASE_URL}/{base}")
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"為替レート取得エラー: {e}")

    all_rates = data.get("rates", {})
    # 指定通貨のみフィルタ
    filtered = {
        k: v for k, v in all_rates.items()
        if k in [t.upper() for t in targets]
    }
    return FxRatesResponse(
        base=base,
        rates=filtered,
        fetched_at=datetime.utcnow().isoformat(),
    )


@router.get("/fx/convert")
async def convert_currency(
    amount: float = Query(..., gt=0, description="変換金額"),
    from_: str = Query(..., alias="from", description="変換元通貨"),
    to: str = Query(..., description="変換先通貨"),
    _=Depends(verify_api_key),
):
    """指定通貨間で金額を変換する"""
    from_ = from_.upper()
    to = to.upper()
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{BASE_URL}/{from_}")
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    rate = data["rates"].get(to)
    if rate is None:
        raise HTTPException(status_code=400, detail=f"Unsupported target currency: {to}")

    converted = round(amount * rate, 6)
    return {
        "from": from_,
        "to": to,
        "amount": amount,
        "converted": converted,
        "rate": rate,
        "fetched_at": datetime.utcnow().isoformat(),
    }
