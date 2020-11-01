if [ ! -f lib/forked/dlt645.py ]; then
    mkdir -p lib/forked
    wget https://raw.githubusercontent.com/glx-technologies/meter-dlt645/master/dlt645.py -P lib/forked
fi

# export FLASK_ENV=development
export FLASK_APP=__init__.py
flask run --host=0.0.0.0 --port=5050 --no-reload

