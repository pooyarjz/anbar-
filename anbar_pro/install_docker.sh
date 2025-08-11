#!/usr/bin/env bash
set -e
echo "== Anbar Pro Docker Installer =="

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required. Install Docker Desktop or docker engine."
  exit 1
fi
if ! command -v docker compose >/dev/null 2>&1; then
  echo "Docker Compose plugin is required."
  exit 1
fi

docker compose up --build -d
docker compose exec web python manage.py migrate

read -p "Create admin user now? [Y/n] " yn
yn=${yn:-Y}
if [[ "$yn" =~ ^[Yy]$ ]]; then
  read -p "Admin username [admin]: " u; u=${u:-admin}
  read -p "Admin email [admin@example.com]: " e; e=${e:-admin@example.com}
  read -s -p "Admin password: " p; echo
  docker compose exec -e DJANGO_SUPERUSER_USERNAME="$u" -e DJANGO_SUPERUSER_EMAIL="$e" -e DJANGO_SUPERUSER_PASSWORD="$p" web python manage.py createsuperuser --noinput || true
fi

if [ -f "./anbar.xlsx" ]; then
  docker compose cp ./anbar.xlsx web:/app/anbar.xlsx
  docker compose exec web python manage.py import_anbar_excel --path /app/anbar.xlsx
fi

echo "Open http://localhost:8000/admin to login, and http://localhost:8000/reports for reports."
