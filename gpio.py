#!/usr/bin/env python

# http://abyz.me.uk/rpi/pigpio/
# sudo gpiod

import time
import curses
import atexit

import pigpio 

GPIOS=32

MODES=["INPUT", "OUTPUT", "ALT5", "ALT4", "ALT0", "ALT1", "ALT2", "ALT3"]

def cleanup():
   curses.nocbreak()
   curses.echo()
   curses.endwin()
   pi.stop()

pi = pigpio.pi()

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

atexit.register(cleanup)

cb = []

for g in range(GPIOS):
   cb.append(pi.callback(g, pigpio.EITHER_EDGE))

# disable gpio 28 as the PCM clock is swamping the system

cb[28].cancel()

stdscr.nodelay(1)

stdscr.addstr(0, 23, "Status of gpios 0-31", curses.A_REVERSE)

# pi.set_pull_up_down(17, pigpio.PUD_OFF)
time.sleep(1)
pi.write(2, 0)  # turn on relay at startup
time.sleep(1)
pi.write(3, 0)  # turn on relay at startup
time.sleep(1)
pi.write(4, 0)  # turn on relay at startup
time.sleep(1)
pi.write(14, 0)  # turn on relay at startup
time.sleep(1)

while True:

   for g in range(GPIOS):
      tally = cb[g].tally()
      mode = pi.get_mode(g)

      col = (g / 11) * 25
      row = (g % 11) + 2

      stdscr.addstr(row, col, "{:2}".format(g), curses.A_BOLD)

      stdscr.addstr(
         "={} {:>6}: {:<10}".format(pi.read(g), MODES[mode], tally))

   stdscr.refresh()

   time.sleep(0.1)

   c = stdscr.getch()

   if c != curses.ERR:
      pi.write(2, 1)  # turn off relay at any keypress
      time.sleep(1)
      pi.write(3, 1)  # turn off relay at any keypress
      time.sleep(1)
      pi.write(4, 1)  # turn off relay at any keypress
      time.sleep(1)
      pi.write(14, 1)  # turn off relay at any keypress
      break
