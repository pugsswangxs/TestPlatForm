#!/bin/sh
set -e

echo "==> Entering project directory"
cd "/app/${PROJECT_NAME}"

echo "==> Checking for manage.py"
if [ ! -f manage.py ]; then
  echo "❌ manage.py not found in $(pwd)"
  exit 1
fi

echo "==> Running makemigrations"
python3 manage.py makemigrations

echo "==> Running migrate"
python3 manage.py migrate

echo "==> Starting supervisor"
exec supervisord -c supervisor.conf
