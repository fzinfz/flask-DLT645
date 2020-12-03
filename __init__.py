from flask import Flask
from flask import render_template

app = Flask(__name__)

from datetime import datetime
import pytz
tz = pytz.timezone('Asia/Shanghai')

from .lib.forked import *
from .lib.read import *

if 'METER_ENV' in os.environ and os.environ['METER_ENV'] == 'prod':
    from .lib.conf_prod import *
    print("** lib/conf_prod loaded **")
else:
    from .lib.conf import *
    print("** lib/conf loaded **")

addr_convert = lambda addr: [ int(s,16) for s in re.findall('..', addr) ]

from flask import Response

def iter_meters():
    devices = Meters(meter_list_str)
    for d in devices.devices:
        addr = d[0] 
        m = Meter(chn, addr_convert(addr), level=1, verbose=0)
        yield devices.df.loc[addr]['Tag'], m.read_meter()

# Folowing: https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/#streaming-from-templates
# but not working on iPad

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

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
