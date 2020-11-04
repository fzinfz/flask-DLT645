from flask import Flask
from flask import render_template

app = Flask(__name__)

from datetime import datetime
import pytz
tz = pytz.timezone('Asia/Shanghai')

from .lib.forked import *
from .lib.read import *

@app.route('/')
@app.route('/meters/')
def read():
    result = read_meters(chn, meters)
    
    for k,v in result.items():
        v['Addr'] = k, ''
        v['Tag'] = get_meter_tag_by_id(k)
    
    now = datetime.now(tz).strftime("%Y-%m-%d %X")
    
    return render_template('meters.html', 
                           meters=result.values(), 
                           now=now
                          )
