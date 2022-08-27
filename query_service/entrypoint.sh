#!/usr/bin/env bash

# Running ingestion
python ingest.py &

# FastAPI
uvicorn query:app --host 0.0.0.0 --port 8002
