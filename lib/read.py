import sys, re, os
import pprint
import pandas as pd
from collections import ChainMap

#                        （DI3~0, 整数位数，小数位数， 单位）
properties_list = [
    {
        '电能-组合有功总-当前':       ('00 00 00 00', 6, 2, 'kWh'),
    },
    {
        '功率-瞬时总有功':      ('02 03 00 00', 2, 4, 'kW'),  
    },
    {    
        '电能-组合有功总-上结算日':       ('00 00 00 01', 6, 2, 'kWh'),

        'A相电压':             ('02 01 01 00', 3, 1, 'V'),    
        'A相电流':             ('02 02 01 00', 3, 3, 'A'),    

        '功率-一分钟有功总平均': ('02 80 00 03', 2, 4, 'kW'),
        '功率因数-总':           ('02 06 00 00', 1, 3, ''), 
    },
    {        
        '内部电池电压':          ('02 80 00 08', 2, 2, 'V'),    

        '日期':                 ('04 00 01 01', 6, 2, '年月日.星期'),  
        '时间':                 ('04 00 01 02', 4, 2, 'hhmm.ss'),      
    },
    {
        'B相电压':             ('02 01 02 00', 3, 1, 'V'),    
        'C相电压':             ('02 01 03 00', 3, 1, 'V'),    

        'B相电流':             ('02 02 02 00', 3, 3, 'A'), 
        'C相电流':             ('02 02 03 00', 3, 3, 'A'), 

        '功率-瞬时A相有功':       ('02 03 01 00', 2, 4, 'kW'),    
        '功率-瞬时B相有功':       ('02 03 02 00', 2, 4, 'kW'),    
        '功率-瞬时C相有功':       ('02 03 03 00', 2, 4, 'kW'),      

        '功率-瞬时总视在':       ('02 05 00 00', 2, 4, 'kVA'),    

        '零线电流':             ('02 80 00 01', 3, 3, 'A'),  
        '频率':                 ('02 80 00 02', 2, 2, 'Hz'),  

        '表内温度':             ('02 80 00 07', 3, 1, '°C'),    
        '内部电池工作时间':       ('02 80 00 0A', 8, 0, '分'), 

        '表号':                 ('04 00 04 02', 12, 0, '#'),  
        '通信地址':             ('04 00 04 01', 12, 0, '#'),  

        '每月第1结算日':         ('04 00 0B 01', 2, 2, '日.时'),  
        '每月第2结算日':         ('04 00 0B 02', 2, 2, '日.时'),  
        '每月第3结算日':         ('04 00 0B 03', 2, 2, '日.时'),  

        '型号':                 ('04 00 04 0B', 20, 0, ''),  

        '状态字1':              ('04 00 05 01', 4, 0, 'int'),    
        '状态字2':              ('04 00 05 02', 4, 0, 'int'),    
        '状态字3':              ('04 00 05 03', 4, 0, 'int'),    
        '状态字4':              ('04 00 05 04', 4, 0, 'int'),    
        '状态字5':              ('04 00 05 05', 4, 0, 'int'),    
        '状态字6':              ('04 00 05 06', 4, 0, 'int'),    
        '状态字7':              ('04 00 05 07', 4, 0, 'int'),    
    }
]


class Meter:
    def __init__(self, chn, addr, level=1, verbose=0):
        self.chn = chn
        self.addr = addr
        self.properties = dict(ChainMap(*properties_list[:level]))
        self.verbose = verbose
        

    def get_data(self, item):

        d = self.properties[item]   
        cmd = [ int(x, 16) for x in d[0].split(' ')[::-1] ]
        self.chn.encode(self.addr, 0x11, cmd)
        self.chn.xchg_data(self.verbose)        
        payload = self.chn.rx_payload

        len_whole, len_decimal = d[1], d[2]
        len_payload = int( (len_whole + len_decimal) / 2 )

        hex_str = ''.join([ "%02x" % x  for x in payload[::-1][:len_payload] ])
        try:
            value = int(hex_str) / pow(10, len_decimal)
        except ValueError:
            value = hex_str

        unit = d[3]
        return value, unit


    def read_meter(self):
        
        D = self.properties
        result = {}

        for item in D:
            result[item] = self.get_data(item)

        if len(D) == 1: return result

        for k, v in D.items():
            unit = v[3]
            if unit == 'kW':
                result[k] = "{:,.2f}".format( result[k][0] * 1000 ) , 'W'           
            if unit == '#':
                result[k] = "{0:0>12d}".format(int(result[k][0])), ''   
            if unit == '分':            
                result[k] = "{:,.2f}".format( result[k][0] / (60*24) / 365 ), '年'

        try:
            
            result['功率-A相'] = "{:,.2f}".format( result['A相电压'][0] * result['A相电流'][0] ) , 'W'
            result['电能:本周期'] = "{:,.2f}".format( result['电能-组合有功总-当前'][0] - result['电能-组合有功总-上结算日'][0] ) , 'kWh'
        
            result['日期时间'] = str(result['日期'][0] + 20000000).split('.')[0] + ' ' + \
                 ':'.join( re.findall('..', "{0:0>6d}".format(int(result['时间'][0]*100))) ), ''
            del result['日期']
            del result['时间']
        except:
            pass

        return result


class Meters:
    
    def __init__(self, meter_list_str):        
        _s = meter_list_str # defined in conf.py
        self.devices = [ re.findall('[^ ]+', line)[:2] 
                        for line in _s.strip().splitlines() if not line.startswith('#') ]
        self.df = pd.DataFrame(self.devices, columns =['Addr','Tag']).set_index('Addr')
    
    def read_meters(self, chn, level=2, verbose=0):
        meters = self.devices
        chn.open()
        print(chn.ser)
        # print('read_meters()', chn.ser.isOpen())

        result = {}
        for meter in meters:    
            print('\n', '='* 5, meter, '='* 5)
            addr_human = meter[0]    
            addr = [ int(s,16) for s in re.findall('..', addr_human) ]
            m = Meter(chn, addr, level, verbose)
            rs = m.read_meter()
            pprint.pprint(rs)
            result[addr_human] = rs

        chn.close()    
        return result
