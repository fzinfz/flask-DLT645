from . import *

from flask import Flask, Response, render_template
app = Flask(__name__)

# Following: https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/#streaming-from-templates
# but streaming not working on iPad

def stream_template(template_name, **context):
    app.update_template_context(context)
    template = app.jinja_env.get_template(template_name)
    response = template.stream(context)
    response.enable_buffering(5)
    return response

from datetime import datetime
import pytz
timezone = pytz.timezone('Asia/Shanghai')

def read_meters(level):
    chn.open()
    meters = iter_meters(level=level)
    current_time = datetime.now(timezone).strftime("%Y-%m-%d %X")
    return meters, current_time

@app.route('/')
def index():
    current_time = datetime.now(timezone).strftime("%Y-%m-%d %X")
    return render_template('index.html', now=current_time)

@app.route('/meters/')
def meters():
    meters_data, current_time = read_meters(level=1)
    return Response(stream_template('meters.html', 
                           meters=meters_data, 
                           now=current_time
                          ))

@app.route('/power/')
def power():
    meters_data, current_time = read_meters(level=2)
    return Response(stream_template('power.html', 
                           meters=meters_data, 
                           now=current_time
                          ))
