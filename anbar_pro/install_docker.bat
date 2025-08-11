@echo off
setlocal
echo == Anbar Pro Docker Installer ==

where docker >NUL 2>&1
if errorlevel 1 (
  echo Docker is required. Install Docker Desktop.
  exit /b 1
)

docker compose up --build -d
docker compose exec web python manage.py migrate

set /p CREATEADMIN=Create admin user now? [Y/n]:
if /I "%CREATEADMIN%"=="n" goto SKIPADMIN
set /p ADMINUSER=Admin username [admin]:
if "%ADMINUSER%"=="" set ADMINUSER=admin
set /p ADMINEMAIL=Admin email [admin@example.com]:
if "%ADMINEMAIL%"=="" set ADMINEMAIL=admin@example.com
set /p ADMINPASS=Admin password:
docker compose exec -e DJANGO_SUPERUSER_USERNAME=%ADMINUSER% -e DJANGO_SUPERUSER_EMAIL=%ADMINEMAIL% -e DJANGO_SUPERUSER_PASSWORD=%ADMINPASS% web python manage.py createsuperuser --noinput || echo (If user exists, ignore)
:SKIPADMIN

if exist anbar.xlsx (
  docker compose cp anbar.xlsx web:/app/anbar.xlsx
  docker compose exec web python manage.py import_anbar_excel --path /app/anbar.xlsx
)

echo Open http://localhost:8000/admin and http://localhost:8000/reports
endlocal
