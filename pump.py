#!/usr/bin/env python

# sudo gpiod

import os
import time
import pigpio 
from web import *

StartWebServer()
pi = pigpio.pi()

while True:
    WebServerIterate()
    WebServerIterate()
    localtime = time.localtime(time.time())
    if localtime.tm_sec < 30 and localtime.tm_min % 15 == 0 and (localtime.tm_hour >= 8 or localtime.tm_hour == 0):
        print(str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec) + ' pump on')
        pi.write(2, 0)
        time.sleep(30)
        print(str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec) + ' pump off')
        pi.write(2, 1)
    else:
        print(str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec) + ' nop')
    if localtime.tm_min == 0 and localtime.tm_sec < 30:
        print(os.popen("./mif.sh").read().strip())
    time.sleep(30)  # seconds
