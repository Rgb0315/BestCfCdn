# git_sync.ps1
# 功能：调用并发安全同步程序，只更新 config.json 中本终端对应的节点。

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) {
    Write-Host "❌ 未找到 Python" -ForegroundColor Red
    exit 1
}

& $python.Source (Join-Path $PSScriptRoot "github_sync.py") --input (Join-Path $PSScriptRoot "ip.txt")
exit $LASTEXITCODE
