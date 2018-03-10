#!/usr/bin/env python

# sudo gpiod

import time

import pigpio 


pi = pigpio.pi()

pi.write(2, 1)
