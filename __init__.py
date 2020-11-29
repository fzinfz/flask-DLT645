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
       
@app.route('/')
@app.route('/meters/')
def read():

    devices = Meters(meter_list_str)
    result = devices.read_meters(chn, level=1)
    
    for k,v in result.items():
        v['Addr'] = k, ''
        v['Tag'] = devices.df.loc[k]['Tag']
    
    now = datetime.now(tz).strftime("%Y-%m-%d %X")
    
    return render_template('meters.html', 
                           meters=result.values(), 
                           now=now
                          )
