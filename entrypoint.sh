#!/bin/bash

alembic upgrade head

exec uvicorn api.core.main:app --host 0.0.0.0 --port 8000
