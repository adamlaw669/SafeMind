#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize Database (Run migrations)
# This creates the tables in the hosted Postgres DB automatically
python -c "from app.db.base import Base, engine; Base.metadata.create_all(bind=engine)"