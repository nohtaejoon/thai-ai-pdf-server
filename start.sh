#!/bin/sh
echo "Starting server on port: $PORT"
exec gunicorn main:app --bind "0.0.0.0:$PORT" --workers 2 --timeout 120
