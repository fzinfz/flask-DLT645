if [ ! -f lib/forked/dlt645.py ]; then
    mkdir -p lib/forked
    wget https://raw.githubusercontent.com/glx-technologies/meter-dlt645/master/dlt645.py -P lib/forked
fi

export FLASK_ENV=development
export FLASK_APP=__init__.py

[ -z "$FLASK_DLT645_PORT" ] && export FLASK_DLT645_PORT=5000
flask run --host=0.0.0.0 --port=$FLASK_DLT645_PORT --no-reload

