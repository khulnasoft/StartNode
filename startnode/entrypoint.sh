#!/bin/bash

# Run Alembic migrations
alembic -c startnode/alembic.ini upgrade heads

# Start the app
exec uvicorn startnode.app:app --host 0.0.0.0 --port 8001 --reload