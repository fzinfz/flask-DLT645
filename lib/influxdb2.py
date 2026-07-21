import sys, os
import importlib.util

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/..')
sys.path.insert(0, ROOT_DIR)

# Load the project root __init__.py explicitly by file path, so it doesn't
# accidentally resolve to lib/__init__.py (lib is itself a package).
_init_path = os.path.join(ROOT_DIR, '__init__.py')
_spec = importlib.util.spec_from_file_location('proj_root', _init_path)
proj = importlib.util.module_from_spec(_spec)
sys.modules['proj_root'] = proj
_spec.loader.exec_module(proj)
from proj_root import *

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

def pull(range_start='-30m'):
    query_api = influxdb_client_obj.query_api()
    flux = f'''
from(bucket: "{influxdb_bucket}")
  |> range(start: {range_start})
  |> filter(fn: (r) => r._field == "当前")
'''
    print(f'query: {flux}')
    tables = query_api.query(org=influxdb_org, query=flux)
    for table in tables:
        for record in table.records:
            print(f"time={record.get_time()}, tag={record.values.get('tag')}, value={record.get_value()}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Push/pull meter data to/from InfluxDB')
    parser.add_argument('--push', action='store_true', help='read meters and push data to influxdb')
    parser.add_argument('--pull', action='store_true', help='query remote influxdb and print fetched data')
    parser.add_argument('--range_start', default='-30m', help='query range start (default: -30m)')
    args = parser.parse_args()

    if args.pull:
        if sys.stdin.isatty() and not any(a.startswith('--range_start=') for a in sys.argv):
            r = input(f'range_start (default {args.range_start}): ').strip()
            if r:
                args.range_start = r
        pull(range_start=args.range_start)
    elif args.push:
        push()
    else:
        parser.print_help()
