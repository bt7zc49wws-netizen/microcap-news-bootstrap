#!/usr/bin/env sh
set -eu

python /app/scripts/free_provider_smoke.py
curl -s http://localhost:8000/api/v1/status
