#!/bin/sh

SERVICE_ID=$1

chmod +x /app/src/main.py
sync

# install function requirements
cd /model
pip install -r requirements.txt

cd /app/src
exec python3 /app/src/main.py