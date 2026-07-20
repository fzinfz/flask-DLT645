import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from lib.forked import *
from lib.read import *

try:
    from conf.conf_my import *
    print("** conf/conf_my loaded **")
except ImportError:
    from conf.conf import *
    print("** conf/conf loaded **")

devices = Meters(meter_list_str)
    
def convert_address(address_str):
    return [ int(byte_str, 16) for byte_str in re.findall('..', address_str) ]

def iter_meters(level=1):
    for device in devices.devices:
        address_str = device[0] 
        meter = Meter(chn, convert_address(address_str), level=level, verbose=0)
        yield devices.df.loc[address_str]['Tag'], meter.read_meter()
