# THWorks REST API Set - Test Script
# Usage: uvicorn起動後、別ターミナルで .\test_api.ps1

$BASE = "http://localhost:8000"
$KEY  = "dev-insecure-key"
$H    = @{ "X-API-Key" = $KEY; "Content-Type" = "application/json" }

Write-Host ""
Write-Host "===== Health Check =====" -ForegroundColor Cyan
$r = Invoke-RestMethod -Uri "$BASE/" -Method GET
$r | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "===== TODO: Create =====" -ForegroundColor Cyan
$body = '{"title": "Test Task 1", "description": "check operation"}'
$r = Invoke-RestMethod -Uri "$BASE/api/v1/todos" -Method POST -Headers $H -Body $body
$r | ConvertTo-Json -Depth 5
$todoId = $r.id

Write-Host ""
Write-Host "===== TODO: List =====" -ForegroundColor Cyan
$r = Invoke-RestMethod -Uri "$BASE/api/v1/todos" -Method GET -Headers $H
$r | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "===== TODO: Update (done=true) =====" -ForegroundColor Cyan
$body = '{"done": true}'
$r = Invoke-RestMethod -Uri "$BASE/api/v1/todos/$todoId" -Method PUT -Headers $H -Body $body
$r | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "===== Markdown -> HTML =====" -ForegroundColor Cyan
$body = '{"markdown_text": "# Hello\n\nThis is **bold** text.", "extensions": ["tables", "fenced_code"]}'
$r = Invoke-RestMethod -Uri "$BASE/api/v1/convert/md2html" -Method POST -Headers $H -Body $body
$r | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "===== FX Rates (JPY base) =====" -ForegroundColor Cyan
$r = Invoke-RestMethod -Uri "$BASE/api/v1/fx/rates?base=JPY&targets=USD&targets=EUR&targets=GBP" -Method GET -Headers $H
$r | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "===== FX Convert: 10000 JPY -> USD =====" -ForegroundColor Cyan
$r = Invoke-RestMethod -Uri "$BASE/api/v1/fx/convert?amount=10000&from=JPY&to=USD" -Method GET -Headers $H
$r | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "===== QR Code -> qrcode_output.png =====" -ForegroundColor Cyan
$body = '{"data": "https://th-works.dev", "size": 10, "error_correction": "M", "format": "png"}'
$resp = Invoke-WebRequest -Uri "$BASE/api/v1/qrcode" -Method POST -Headers @{ "X-API-Key" = $KEY; "Content-Type" = "application/json" } -Body $body
[System.IO.File]::WriteAllBytes("$PWD\qrcode_output.png", $resp.Content)
Write-Host "Saved: qrcode_output.png"
Start-Process "$PWD\qrcode_output.png"

Write-Host ""
Write-Host "All tests done." -ForegroundColor Green
