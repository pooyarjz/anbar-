
Write-Host "=== Anbar Pro: Diagnose & Fix ==="

$ErrorActionPreference = "Continue"
$root = (Get-Item "$PSScriptRoot\..\..").FullName
Set-Location $root

function Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Err($msg)  { Write-Host "[ERR ] $msg" -ForegroundColor Red }

Info "Current folder: $root"
Info "PowerShell: $($PSVersionTable.PSVersion)"
Info "ExecutionPolicy (CurrentUser): $(Get-ExecutionPolicy -Scope CurrentUser)"
Info "Checking Python..."
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) {
  Warn "Python not found. Trying winget install..."
  $win = (Get-Command winget -ErrorAction SilentlyContinue)
  if ($win) {
    winget install --id Python.Python.3.11 -e --source winget --accept-package-agreements --accept-source-agreements
  } else {
    Err "winget not available. Install Python 3.11+ manually from python.org"
    exit 1
  }
}

Info "Creating/activating venv..."
if (!(Test-Path ".\.venv")) { python -m venv .venv }
. .\.venv\Scripts\Activate.ps1

Info "Upgrading pip & installing requirements..."
python -m pip install --upgrade pip
pip install -r requirements.txt

Info "Django check & migrate..."
$env:ANBAR_SQLITE = "1"
$env:DJANGO_DEBUG = "1"
python manage.py check
python manage.py migrate

Info "Checking port 8000..."
$busy = netstat -ano | Select-String ":8000" | Select-String "LISTENING"
if ($busy) {
  Warn "Port 8000 is busy. Trying to stop the process..."
  $pid = ($busy -split "\s+")[-1]
  try { Stop-Process -Id $pid -Force; Info "Stopped PID $pid" } catch { Warn "Could not stop PID $pid: $_" }
}

Info "Starting server (waitress)..."
if (!(Test-Path ".\logs")) { New-Item -ItemType Directory -Path ".\logs" | Out-Null }
python -m waitress --host=127.0.0.1 --port=8000 anbar_pro.wsgi:application *> .\logs\server_console.log
