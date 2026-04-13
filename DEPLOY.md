# Render 無料枠へのデプロイ手順

## 1. Renderで新規 Web Service 作成

1. https://dashboard.render.com → **New → Web Service**
2. GitHubリポジトリ連携: `thworks0401/th-works-api-set`
3. 設定値:

   | 項目 | 値 |
   |------|-----|
   | Name | th-works-api-set |
   | Runtime | Python 3 |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | Instance Type | Free |

4. **Environment Variables** に追加:

   | Key | Value |
   |-----|-------|
   | `API_KEY` | 任意のランダム文字列 |
   | `APP_ENV` | `production` |

5. **Deploy** ボタンを押す

## 2. ngrokでローカル公開（Render代替）

```powershell
# uvicorn起動後、別ターミナルで
ngrok http 8000
# 表示された https://xxxx.ngrok.io が公開URL
```

## 3. 動作確認

```powershell
# Render URLからテスト
$BASE = "https://th-works-api-set.onrender.com"
$H = @{ "X-API-Key" = "設定したAPI_KEY" }
Invoke-RestMethod -Uri "$BASE/" -Method GET
Invoke-RestMethod -Uri "$BASE/docs" -Method GET
```

## 注意事項

- Render無料枠は**15分アイドルでスリープ**する。テスト時は最初の1リクエストに30秒程度かかる場合あり。
- `テキスト要約API`はOllamaローカル依存のため、Renderデプロイ中は503を返す。その他4本は完全動作する。
- 要約APIを公開したい場合は、Ollama Cloudデプロイ or OpenAI代替に切り替える必要あり。
