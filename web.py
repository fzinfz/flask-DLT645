from . import *

from flask import Flask
app = Flask(__name__)

# Folowing: https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/#streaming-from-templates
# but not working on iPad

from flask import Response
def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

from datetime import datetime
import pytz
tz = pytz.timezone('Asia/Shanghai')

from flask import Response

@app.route('/')
@app.route('/meters/')
def read():

    chn.open()
    meters = iter_meters()
    
    now = datetime.now(tz).strftime("%Y-%m-%d %X")
    
    return Response(stream_template('meters.html', 
                           meters=meters, 
                           now=now
                          ))
