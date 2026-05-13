#!/bin/bash
# Railway startup — runs all 3 services in one dyno
set -e

echo "[start] Launching Legacy Bank on :8001"
python -m uvicorn services.legacy_bank:app --host 0.0.0.0 --port 8001 &

echo "[start] Launching Modern Bank on :8002"
python -m uvicorn services.modern_bank:app --host 0.0.0.0 --port 8002 &

# Give banks 3s to come up before dashboard tries to connect
sleep 3

echo "[start] Launching Dashboard on :${PORT:-8501}"
streamlit run dashboard.py \
  --server.port "${PORT:-8501}" \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.gatherUsageStats false
