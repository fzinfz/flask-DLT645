from __init__ import *

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

print(f'{influxdb_url}, bucket={influxdb_bucket}, org={influxdb_org}')
influxdb_client_obj = InfluxDBClient(url=influxdb_url, token=influxdb_token)
    
write_api = influxdb_client_obj.write_api(write_options=SYNCHRONOUS)

chn.open()

def push():
    sequence = []
    for device in devices.devices:
        address_str = device[0] 
        meter = Meter(chn, convert_address(address_str), level=1, verbose=0)
        meter_data = meter.read_meter()
        line = f"度数,tag={devices.df.loc[address_str]['Tag']} 当前={meter_data['电能-组合有功总-当前'][0]}"
        print(line)
        sequence.append(line)

    write_api.write(influxdb_bucket, influxdb_org, sequence)

if __name__ == '__main__':
    push()
