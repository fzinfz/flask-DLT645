# 1-Addr(非表号)  2-Tag  3..-可选自定义列\

meter_list_str = '''
010128318569 表1
001522454104 表2
# 000080853040 表3
'''

from forked import dlt645
chn=dlt645.Channel(port_id = '/dev/ttyUSB1', tmo_cnt = 10, wait_for_read = 0.5)
