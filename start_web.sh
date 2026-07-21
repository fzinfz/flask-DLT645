#!/usr/bin/env bash
. ./setup.sh

# 仅当端口是合法整数时才使用，否则回退（防御脏环境变量）
if ! [[ "${FLASK_DLT645_PORT:-}" =~ ^[0-9]+$ ]]; then
  FLASK_DLT645_PORT=5000
fi
export FLASK_DLT645_PORT

export PYTHONUNBUFFERED=1

export FLASK_APP=web.py
export PATH="/root/.local/bin/:$PATH"
uv run flask run --host=0.0.0.0 --port=$FLASK_DLT645_PORT --no-reload
