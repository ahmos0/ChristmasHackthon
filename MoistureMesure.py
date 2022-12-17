# -*- coding:utf-8 -*-
import time
import spidev
import requests

import os

from dotenv import load_dotenv
load_dotenv()

# 発行されたトークンID
ACCESS_TOKEN =os.environ['ACCESS_TOKEN']
STR_NOTICE_MESSAGE = 'お湯張りができました'


Vref = 3.334 

spi = spidev.SpiDev()

spi.open(0, 0) 
spi.max_speed_hz = 100000  


def readAdc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 200])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def convertVolts(data, vref):
    mois = (data * vref) / float(1023)
    return mois

def fnc_line_notify():
    line_notify_api  =  "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {'message': f'{STR_NOTICE_MESSAGE}'}
    requests.post(line_notify_api, headers=headers, data=data)
    return


if __name__ == '__main__':
    try:
        while True:
            data = readAdc(channel=0)
            mois = convertVolts(data, Vref)
            print("CH0 mois: {:.2f}".format(mois))
            if mois < 1.8:
                fnc_line_notify()
                break
            time.sleep(2)

    except KeyboardInterrupt:
        spi.close()