# THWorks REST API セット — 動作確認用PowerShellスクリプト
# 使い方: .venvを有効化しuvicorn起動後、別ターミナルで .\test_api.ps1

$BASE = "http://localhost:8000"
$KEY  = "dev-insecure-key"  # .envのAPI_KEYと合わせる
$H    = @{ "X-API-Key" = $KEY; "Content-Type" = "application/json" }

function Show-Result($title, $resp) {
    Write-Host ""`n===== $title =====" -ForegroundColor Cyan
    Write-Host ($resp | ConvertTo-Json -Depth 5)
}

# 1. ヘルスチェック
$r = Invoke-RestMethod -Uri "$BASE/" -Method GET
Show-Result "Health Check" $r

# 2. TODO 作成
$body = @{ title = "テストタスク1"; description = "動作確認用" } | ConvertTo-Json
$r = Invoke-RestMethod -Uri "$BASE/api/v1/todos" -Method POST -Headers $H -Body $body
Show-Result "TODO Create" $r
$todoId = $r.id

# 3. TODO 一覧
$r = Invoke-RestMethod -Uri "$BASE/api/v1/todos" -Method GET -Headers $H
Show-Result "TODO List" $r

# 4. TODO 更新
$body = @{ done = $true } | ConvertTo-Json
$r = Invoke-RestMethod -Uri "$BASE/api/v1/todos/$todoId" -Method PUT -Headers $H -Body $body
Show-Result "TODO Update (done=true)" $r

# 5. Markdown -> HTML
$body = @{ markdown_text = "# Hello\n\nThis is **bold** and `code`."; extensions = @("fenced_code", "tables") } | ConvertTo-Json
$r = Invoke-RestMethod -Uri "$BASE/api/v1/convert/md2html" -Method POST -Headers $H -Body $body
Show-Result "Markdown -> HTML" $r

# 6. 為替レート
$r = Invoke-RestMethod -Uri "$BASE/api/v1/fx/rates?base=JPY&targets=USD&targets=EUR" -Method GET -Headers $H
Show-Result "FX Rates (JPY base)" $r

# 7. 為替変換
$r = Invoke-RestMethod -Uri "$BASE/api/v1/fx/convert?amount=10000&from=JPY&to=USD" -Method GET -Headers $H
Show-Result "FX Convert 10000 JPY -> USD" $r

# 8. QRコード生成 (画像ファイル保存)
$body = @{ data = "https://th-works.dev"; size = 10; error_correction = "M"; format = "png" } | ConvertTo-Json
$bytes = Invoke-WebRequest -Uri "$BASE/api/v1/qrcode" -Method POST `
    -Headers @{ "X-API-Key" = $KEY; "Content-Type" = "application/json" } `
    -Body $body
[System.IO.File]::WriteAllBytes("$PWD\qrcode_output.png", $bytes.Content)
Write-Host ""`n===== QR Code =====" -ForegroundColor Cyan
Write-Host "山力: qrcode_output.png (ブラウザで開く)"
Start-Process "$PWD\qrcode_output.png"

Write-Host ""`n✅ 全テスト完了" -ForegroundColor Green
