#!/usr/bin/env python

# sudo gpiod

import time

import pigpio 

pi = pigpio.pi()

while True:
    localtime = time.localtime(time.time())
    if localtime.tm_sec < 30 and localtime.tm_min % 15 and (localtime.tm_hour >= 8 or localtime.tm_hour == 0):
        print(str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec) + ' pump on')
        pi.write(2, 0)
    else:
        print(str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec) + ' pump off')
        pi.write(2, 1)
    time.sleep(10)  # seconds
