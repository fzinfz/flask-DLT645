import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from lib.forked import *
from lib.read import *
from lib.conf import *

devices = Meters(meter_list_str)
    
addr_convert = lambda addr: [ int(s,16) for s in re.findall('..', addr) ]

def iter_meters():
    for d in devices.devices:
        addr = d[0] 
        m = Meter(chn, addr_convert(addr), level=1, verbose=0)
        yield devices.df.loc[addr]['Tag'], m.read_meter()
