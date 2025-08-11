@echo off
setlocal
echo == Anbar Pro Local Installer (Windows) ==

where python >NUL 2>&1
if errorlevel 1 (
  echo Python is required (3.10+). Install from https://python.org
  exit /b 1
)

python -m venv .venv
call .venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

set ANBAR_SQLITE=1
set DJANGO_DEBUG=1

python manage.py migrate

set /p CREATEADMIN=Create admin user now? [Y/n]:
if /I "%CREATEADMIN%"=="n" goto SKIPADMIN
set /p ADMINUSER=Admin username [admin]:
if "%ADMINUSER%"=="" set ADMINUSER=admin
set /p ADMINEMAIL=Admin email [admin@example.com]:
if "%ADMINEMAIL%"=="" set ADMINEMAIL=admin@example.com
set /p ADMINPASS=Admin password:
set DJANGO_SUPERUSER_USERNAME=%ADMINUSER%
set DJANGO_SUPERUSER_EMAIL=%ADMINEMAIL%
set DJANGO_SUPERUSER_PASSWORD=%ADMINPASS%
python manage.py createsuperuser --noinput || echo (If user exists, ignoring error)
:SKIPADMIN

if exist anbar.xlsx (
  echo Found anbar.xlsx - importing base columns...
  python manage.py import_anbar_excel --path anbar.xlsx
) else (
  echo Place your anbar.xlsx in this folder to import data.
)

echo Starting server at http://127.0.0.1:8000  (Press Ctrl+C to stop)
python manage.py runserver 0.0.0.0:8000
endlocal
