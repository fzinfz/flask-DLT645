from flask import Flask
from flask import render_template

app = Flask(__name__)

from datetime import datetime
import pytz
tz = pytz.timezone('Asia/Shanghai')

from .lib.forked import *
from .lib.read import *
from .lib.conf import *

chn=dlt645.Channel(port_id = serial_port, tmo_cnt = timeout_count, wait_for_read = wait_for_read)

@app.route('/')
@app.route('/meters/')
def read():
    
    meters = get_meter_list(meter_list_str)
    result = read_meters(chn, meters, level=1)
    
    for k,v in result.items():
        v['Addr'] = k, ''
        v['Tag'] = get_meter_tag_by_id(k, meters)
    
    now = datetime.now(tz).strftime("%Y-%m-%d %X")
    
    return render_template('meters.html', 
                           meters=result.values(), 
                           now=now
                          )
