# Claude Code Plugins Hub - Windows PowerShell Setup
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "Pornire instalare Claude Code Plugins Hub..." -ForegroundColor Cyan

if (Get-Command python -ErrorAction SilentlyContinue) {
    python install.py
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    py install.py
} else {
    Write-Host "[EROARE] Python nu a fost gasit in PATH!" -ForegroundColor Red
    Write-Host "Te rugam sa instalezi Python de la https://python.org si sa bifezi 'Add Python to PATH'." -ForegroundColor Yellow
    exit 1
}
