#!/usr/bin/env bash
set -e
echo "== Anbar Pro Local Installer (Linux/macOS) =="

# Ensure Python
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 is required. Please install Python 3.10+."
  exit 1
fi

# Create venv
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install deps
pip install --upgrade pip
pip install -r requirements.txt

# Use SQLite
export ANBAR_SQLITE=1
export DJANGO_DEBUG=1

# Migrate and create superuser
python manage.py migrate

read -p "Create admin user now? [Y/n] " yn
yn=${yn:-Y}
if [[ "$yn" =~ ^[Yy]$ ]]; then
  read -p "Admin username [admin]: " u; u=${u:-admin}
  read -p "Admin email [admin@example.com]: " e; e=${e:-admin@example.com}
  read -s -p "Admin password: " p; echo
  export DJANGO_SUPERUSER_USERNAME="$u"
  export DJANGO_SUPERUSER_EMAIL="$e"
  export DJANGO_SUPERUSER_PASSWORD="$p"
  python manage.py createsuperuser --noinput || true
fi

# Optional Excel import
if [ -f "./anbar.xlsx" ]; then
  echo "Found anbar.xlsx – importing base columns..."
  python manage.py import_anbar_excel --path ./anbar.xlsx
else
  echo "Place your anbar.xlsx next to this script to import data."
fi

echo "Starting server at http://127.0.0.1:8000 ... (Ctrl+C to stop)"
python manage.py runserver 0.0.0.0:8000
