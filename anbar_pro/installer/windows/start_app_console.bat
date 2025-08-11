
@echo off
setlocal ENABLEDELAYEDEXPANSION
echo === Anbar Pro: Console Starter (Verbose) ===

cd /d %~dp0\..\..

echo [1/8] Checking Python...
where python >NUL 2>&1
if errorlevel 1 (
  echo ERROR: Python not found. Please install Python 3.11+ from https://python.org or run post_install.ps1
  pause
  exit /b 1
)

echo [2/8] Creating venv if missing...
if not exist .venv (
  python -m venv .venv
  if errorlevel 1 (
    echo ERROR: Failed to create virtualenv.
    pause
    exit /b 1
  )
)

echo [3/8] Activating venv...
call .venv\Scripts\activate

echo [4/8] Pip upgrade & install requirements...
python -m pip --version
python -m pip install --upgrade pip
if errorlevel 1 echo WARNING: pip upgrade failed (continuing)
pip install -r requirements.txt
if errorlevel 1 (
  echo ERROR: Failed to install requirements.
  pause
  exit /b 1
)

echo [5/8] Django checks & migrate...
set ANBAR_SQLITE=1
set DJANGO_DEBUG=1
python manage.py check
if errorlevel 1 (
  echo ERROR: Django check failed.
  pause
  exit /b 1
)
python manage.py migrate
if errorlevel 1 (
  echo ERROR: migrate failed.
  pause
  exit /b 1
)

echo [6/8] Port check (8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
  echo Port 8000 is in use by PID %%a
  echo Try closing the app using that port or run stop_app.bat
  pause
  exit /b 1
)

echo [7/8] Starting server with waitress on http://127.0.0.1:8000 ...
if not exist logs mkdir logs
python -m waitress --host=127.0.0.1 --port=8000 anbar_pro.wsgi:application 1>>logs\server.out.log 2>>logs\server.err.log
if errorlevel 1 (
  echo ERROR: waitress failed to start.
  echo See logs\server.err.log for details.
  pause
  exit /b 1
)

echo [8/8] Running. Press Ctrl+C to stop.
endlocal
