#!/bin/sh
ACTUAL_PORT="${PORT:-8080}"
echo "=== Starting Thai AI Server ==="
echo "PORT env: $PORT"
echo "Using port: $ACTUAL_PORT"
exec gunicorn main:app --bind "0.0.0.0:${ACTUAL_PORT}" --workers 1 --timeout 120 --log-level debug
