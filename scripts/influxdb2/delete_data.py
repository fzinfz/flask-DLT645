#!/usr/bin/env python3
# Delete all test data (every measurement / field / tag) in the given range.
#
# Reads connection settings from conf/conf.py (via the project root __init__.py,
# which prefers conf/conf_my.py when present).
#
# Usage:
#   uv run scripts/influxdb2/delete_data.py # --start=-1h --stop=now()
#   uv run scripts/influxdb2/delete_data.py --start=2024-01-01T00:00:00Z --stop=2024-01-02T00:00:00Z

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
                            make_client, print_connection, to_rfc3339)


def delete_data(start='-1h', stop='now()'):
    print_connection()

    # The delete API requires absolute RFC3339 timestamps; convert relative
    # specs like -1h / now() into concrete times.
    start_rfc = to_rfc3339(start)
    stop_rfc = to_rfc3339(stop)

    # predicate is empty -> matches every point in the range (all measurements,
    # fields and tags). With InfluxDB 2.x the stop bound is exclusive.
    predicate = ''

    print(f'delete start={start_rfc}, stop={stop_rfc}, predicate={predicate!r}')

    client = make_client()
    delete_api = client.delete_api()
    delete_api.delete(start=start_rfc, stop=stop_rfc, predicate=predicate,
                      bucket=influxdb_bucket, org=influxdb_org)
    print('done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete all test data from InfluxDB in the given range')
    parser.add_argument('--start', default='-1h',
                        help='range start, e.g. -1h, -7d, 2024-01-01T00:00:00Z (default: -1h)')
    parser.add_argument('--stop', default='now()',
                        help='range stop, e.g. now(), -1h, 2024-01-02T00:00:00Z (default: now())')
    args = parser.parse_args()

    delete_data(start=args.start, stop=args.stop)
