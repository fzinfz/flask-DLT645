#!/usr/bin/env python3
# Shared helpers for the influxdb2 scripts under scripts/influxdb2/.
#
# Loads the project root __init__.py (which prefers conf/conf_my.py when
# present) so that influxdb_url / influxdb_token / influxdb_org /
# influxdb_bucket are available, and exposes a convenience to build a client.

import sys, os
import importlib.util
import re
from datetime import datetime, timezone, timedelta

# Project root = parent of scripts/.. -> scripts/influxdb2/query_diff
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../..')
sys.path.insert(0, ROOT_DIR)

# Load the project root __init__.py explicitly by file path, so it doesn't
# accidentally resolve to lib/__init__.py (lib is itself a package).
_init_path = os.path.join(ROOT_DIR, '__init__.py')
_spec = importlib.util.spec_from_file_location('proj_root', _init_path)
proj = importlib.util.module_from_spec(_spec)
sys.modules['proj_root'] = proj
_spec.loader.exec_module(proj)
from proj_root import *

from influxdb_client import InfluxDBClient


def make_client():
    """Return an InfluxDBClient built from the project configuration."""
    return InfluxDBClient(url=influxdb_url, token=influxdb_token)


def print_connection():
    print(f'influxdb_url={influxdb_url}, bucket={influxdb_bucket}, org={influxdb_org}')


# Units understood by the relative-time helper below.
_DURATION_UNITS = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800}


def to_rfc3339(value):
    """Convert a time spec into an RFC3339Nano string for the delete API.

    The delete API requires absolute RFC3339 timestamps (e.g.
    2009-01-02T23:00:00Z); it does NOT accept Flux relative times like -1h
    or now(). This helper accepts:
      - 'now()' / 'now'        -> current UTC time
      - '-1h', '-30m', '-7d', '-1w' -> now minus the duration
      - a literal RFC3339 string   -> returned unchanged

    Returns an RFC3339 string (no fractional seconds needed by the API).
    """
    if value is None:
        return value
    value = str(value).strip()
    if value in ('now()', 'now'):
        dt = datetime.now(timezone.utc)
    elif value.startswith('-'):
        m = re.fullmatch(r'-(\d+)([smhdw])', value)
        if not m:
            # Not a recognised relative spec; assume it is already RFC3339.
            return value
        amount = int(m.group(1))
        unit = m.group(2)
        dt = datetime.now(timezone.utc) - timedelta(seconds=amount * _DURATION_UNITS[unit])
    else:
        # Literal RFC3339 (or any other value) passed through unchanged.
        return value
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
