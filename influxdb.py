from __init__ import *

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

print(f'{influxdb_url}, bucket={influxdb_bucket}, org={influxdb_org}')
influxdb_client_obj = InfluxDBClient(url=influxdb_url, token=influxdb_token)
    
write_api = influxdb_client_obj.write_api(write_options=SYNCHRONOUS)

chn.open()

def push():
    sequence = []
    for d in devices.devices:
        addr = d[0] 
        m = Meter(chn, addr_convert(addr), level=1, verbose=0)
        meter_data = m.read_meter()
        s = f"度数,tag={devices.df.loc[addr]['Tag']} 当前={meter_data['电能-组合有功总-当前'][0]}"
        print(s)
        sequence.append(s)

    write_api.write(influxdb_bucket, influxdb_org, sequence)

if __name__ == '__main__':
    push()