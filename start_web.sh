. ./setup.sh

[ -z "$FLASK_DLT645_PORT" ] && export FLASK_DLT645_PORT=5000

export PYTHONUNBUFFERED=1

export FLASK_APP=web.py
flask run --host=0.0.0.0 --port=$FLASK_DLT645_PORT --no-reload
