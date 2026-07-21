#!/usr/bin/env python3
# Query the 度数/当前 series and print the per-point difference (delta).
#
# Reads connection settings from conf/conf.py (via the project root __init__.py,
# which prefers conf/conf_my.py when present).
#
# Usage:
#   uv run scripts/influxdb2/query_diff.py # [--start=-1h] [--stop=now()]
#   uv run scripts/influxdb2/query_diff.py --start=-7d --stop=-1h

import argparse
import importlib.util
import os, sys

# Load the shared lib.py from this same directory under a private module name
# to avoid clobbering the project's top-level `lib` package (which __init__.py
# imports via `from lib.forked import *`).
_COMMON_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib.py')
_spec = importlib.util.spec_from_file_location('_influx_common', _COMMON_PATH)
_common = importlib.util.module_from_spec(_spec)
sys.modules['_influx_common'] = _common
_spec.loader.exec_module(_common)

from _influx_common import (influxdb_url, influxdb_bucket, influxdb_org,
                            influxdb_token, make_client, print_connection)


def query_diff(start='-1h', stop='now()'):
    print_connection()

    flux = f'''
from(bucket: "{influxdb_bucket}")
  |> range(start: {start}, stop: {stop})
  |> filter(fn: (r) => r["_measurement"] == "度数")
  |> filter(fn: (r) => r["_field"] == "当前")
  |> difference()
'''
    print(f'query:\n{flux}')

    client = make_client()
    query_api = client.query_api()
    tables = query_api.query(org=influxdb_org, query=flux)

    for table in tables:
        for record in table.records:
            print(f"time={record.get_time()}, tag={record.values.get('tag')}, diff={record.get_value()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query 度数/当前 difference from InfluxDB')
    parser.add_argument('--start', default='-1h',
                        help='range start, e.g. -1h, -7d, 2024-01-01T00:00:00Z (default: -1h)')
    parser.add_argument('--stop', default='now()',
                        help='range stop, e.g. now(), -1h, 2024-01-02T00:00:00Z (default: now())')
    args = parser.parse_args()

    query_diff(start=args.start, stop=args.stop)
