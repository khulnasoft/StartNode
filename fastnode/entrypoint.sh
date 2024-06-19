#!/bin/bash

# Run Alembic migrations
alembic -c fastnode/alembic.ini upgrade heads

# Fast the app
exec uvicorn fastnode.app:app --host 0.0.0.0 --port 8001 --reload