#!/bin/sh
set -e

echo "Applying database migrations..."
python -m alembic upgrade head

echo "Starting server..."
exec python -m uvicorn app:app --host 0.0.0.0 --port 8000