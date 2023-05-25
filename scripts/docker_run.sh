#!/bin/bash

set -e

alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 1 --log-level info
