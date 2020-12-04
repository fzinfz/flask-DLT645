import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from lib.forked import *
from lib.read import *

if 'METER_ENV' in os.environ and os.environ['METER_ENV'] == 'prod':
    from lib.conf_prod import *
    print("** lib/conf_prod loaded **")
else:
    from lib.conf import *
    print("** lib/conf loaded **")

try:
    from lib.conf_my import *
    print("** lib/conf_my loaded **")
except:
    pass

devices = Meters(meter_list_str)
    
addr_convert = lambda addr: [ int(s,16) for s in re.findall('..', addr) ]

def iter_meters():
    for d in devices.devices:
        addr = d[0] 
        m = Meter(chn, addr_convert(addr), level=1, verbose=0)
        yield devices.df.loc[addr]['Tag'], m.read_meter()
