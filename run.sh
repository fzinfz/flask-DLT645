if [ ! -f lib/forked/dlt645.py ]; then
    mkdir -p lib/forked
    wget https://raw.githubusercontent.com/glx-technologies/meter-dlt645/master/dlt645.py -P lib/forked
fi

[ -n "$1" ] && export METER_ENV=$1 || export METER_ENV=prod # 'dev' or 'prod'

[ -z "$FLASK_ENV" ] && export FLASK_ENV=development
[ -z "$FLASK_DLT645_PORT" ] && export FLASK_DLT645_PORT=5000

export FLASK_APP=__init__.py
flask run --host=0.0.0.0 --port=$FLASK_DLT645_PORT --no-reload

