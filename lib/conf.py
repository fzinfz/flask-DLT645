# 1-Addr(非表号)  2-Tag  3..-可选自定义列\

meter_list_str = '''
010128318569 表1
# 001522454104 表2
000080853040 表3
'''

from forked import dlt645
chn=dlt645.Channel(port_id = '/dev/ttyUSB0', tmo_cnt = 10, wait_for_read = 0.5)

# [可选] influxdb (OSS V2.0 tested)

influxdb_url="http://192.168.1.72:8086"
influxdb_token = ""
influxdb_org = ""
influxdb_bucket = ""
