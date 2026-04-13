# THWorks REST API セット

FastAPI + Python 3.11 で作る5本の REST API ポートフォリオ。

## API 一覧

| # | API名 | 概要 | エンドポイント |
|---|-------|------|---------------|
| 1 | **TODO CRUD API** | タスク管理の基本CRUD | `/api/v1/todos` |
| 2 | **Markdown→HTML変換 API** | MarkdownテキストをHTMLに変換 | `/api/v1/convert/md2html` |
| 3 | **テキスト要約 API** | 長文テキストを要約（ローカルOllama利用） | `/api/v1/summarize` |
| 4 | **為替レート取得 API** | 主要通貨の為替レート取得 | `/api/v1/fx/rates` |
| 5 | **QRコード生成 API** | テキスト/URLからQRコード画像を生成 | `/api/v1/qrcode` |

## 技術スタック

- **フレームワーク**: FastAPI 0.115+
- **Python**: 3.11
- **バリデーション**: Pydantic v2
- **ドキュメント**: Swagger UI (自動生成) → `/docs`
- **デプロイ**: Render 無料枠 or ローカル + ngrok
- **認証**: API Key 認証 (ヘッダー: `X-API-Key`)

## セットアップ

```powershell
# リポジトリクローン
git clone https://github.com/thworks0401/th-works-api-set.git
cd th-works-api-set

# venv作成・有効化
python -m venv .venv
.venv\Scripts\Activate.ps1

# 依存インストール
pip install -r requirements.txt

# 起動
uvicorn app.main:app --reload --port 8000
```

## ドキュメント

起動後、以下でSwagger UIを確認:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## ライセンス

MIT
