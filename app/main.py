"""THWorks REST API セット — メインエントリ"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import todos, convert, summarize, fx, qrcode
from app.core.config import settings

app = FastAPI(
    title="THWorks REST API セット",
    description="""
## THWorks ポートフォリオ — REST API セット

5本のREST APIを一括公開。実務起用の設計パターンを包括。

### 認証
`X-API-Key` ヘッダーに API Key を付けてリクエスト。

```
X-API-Key: your-secret-api-key-here
```
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(todos.router, prefix="/api/v1", tags=["TODO"])
app.include_router(convert.router, prefix="/api/v1", tags=["Convert"])
app.include_router(summarize.router, prefix="/api/v1", tags=["Summarize"])
app.include_router(fx.router, prefix="/api/v1", tags=["FX"])
app.include_router(qrcode.router, prefix="/api/v1", tags=["QRCode"])


@app.get("/", tags=["Health"])
async def root():
    """APIセットのルート。ヘルスチェック用。"""
    return {
        "service": "THWorks REST API セット",
        "version": "0.1.0",
        "status": "ok",
        "docs": "/docs",
        "endpoints": [
            "/api/v1/todos",
            "/api/v1/convert/md2html",
            "/api/v1/summarize",
            "/api/v1/fx/rates",
            "/api/v1/qrcode",
        ],
    }
