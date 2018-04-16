#!/usr/bin/env python

# sudo gpiod

import time

import pigpio 


pi = pigpio.pi()

pi.write(2, 0)  # turn on relay at startup
time.sleep(1)
pi.write(3, 0)  # turn on relay at startup
#time.sleep(1)
#pi.write(4, 0)  # turn on relay at startup
#time.sleep(1)
#pi.write(14, 0)  # turn on relay at startup
#time.sleep(1)

time.sleep(5)

pi.write(2, 1)  # turn off relay at any keypress
time.sleep(1)
pi.write(3, 1)  # turn off relay at any keypress
#time.sleep(1)
#pi.write(4, 1)  # turn off relay at any keypress
#time.sleep(1)
#pi.write(14, 1)  # turn off relay at any keypress

