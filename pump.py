#!/usr/bin/env python

# sudo gpiod

import time

import pigpio 


pi = pigpio.pi()

#on 
####pi.write(2, 0)


#### offf 
##pi.write(2, 1)

while True:
    localtime = time.localtime(time.time())
    if localtime.tm_min == 00 and localtime.tm_hour > 8 and localtime.tm_hour < 21:
        print('zero minutes')
    else:
        print('non zero minutes')
    # if localtime.tm_hour == 10:
    time.sleep(5)  # seconds
