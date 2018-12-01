from smbus2 import SMBus
import time
import requests

def refactor(l):
    if l > 128:
        return l - 255
    return l
def get_mode(x):
    if x < 4000:
        return 0
    elif x < 6000:
        return 1
    elif x < 8000:
        return 2
    else:
        return 3
    

bus = SMBus(1)
address = 0x4c

while 1:
    time.sleep(0.1)
    bus.write_i2c_block_data(address, 0,[0x15, 0x30, 0x00, 0x0C,])
    l = bus.read_i2c_block_data(address,0, 16)
    status = l[4] & 7
    
    data={}
    data['activity']=str(status)
    

    registers = [ 0x12, 0x20, 0x06, 0x01, 0x00]
    bus.write_i2c_block_data(address, 0,registers)
    l = bus.read_i2c_block_data(address, 0, 32)
    x = refactor(l[26]) **2 + refactor(l[28]) **2  + refactor(l[30]) **2
    data['jump']=str(get_mode(x))
    print(data,x)
    r = requests.post(
        url='https://mwmrdhsvyb.execute-api.us-east-2.amazonaws.com/default/4764activity',
        json=data)
#     print(str(r.text))