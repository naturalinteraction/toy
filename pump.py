#!/usr/bin/env python

# sudo gpiod

import os
import time
import pigpio
from web import *

pump_log = 'Started.<br>'
UpdateWeb(pump_log)

StartWebServer()
pi = pigpio.pi()

while True:
    localtime = time.localtime(time.time())
    if localtime.tm_hour >= 9 and localtime.tm_hour < 21:
        pi.write(2, 0)  # lamps
    else:
        pi.write(2, 1)  # lamps
    if localtime.tm_sec < 30 and localtime.tm_min % 15 == 0 and (localtime.tm_hour >= 0 or localtime.tm_hour == 0):  # day and night
        message = str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec) + ' pump on'
        print(message)
        pump_log = pump_log + message + '<br>'
        UpdateWeb(pump_log)
        pi.write(3, 0)
        time.sleep(40)
        print(str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec) + ' pump off')
        pi.write(3, 1)
    else:
        print(str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec) + ' nop')
    if localtime.tm_min == 0 and localtime.tm_sec < 30:
        message = os.popen("./mif.sh").read().strip()
        print(message)
        pump_log = pump_log + message + '<br>'
    for i in range(30):
        WebServerIterate()
        time.sleep(1)  # seconds
