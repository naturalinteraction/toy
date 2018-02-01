import pygame
from pygame.locals import *
import sys
import time
import select
import numpy
import xwiimote
import glob

''''
pygame.transform.scale()
resize to new resolution
scale(Surface, (width, height), DestSurface = None) -> Surface


Make a copy of the image you want to show (to not change the original) and use following:
self.image = self.original_image.copy()
# this works on images with per pixel alpha too
alpha = 128
self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)


def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)


If you replace the screen.blit(happy, (100, 100)) with a call to blit_alpha(screen, happy, (100, 100), 128), you get the following:
'''''

def IsBoard(dev):
    time.sleep(2) # if we check the devtype to early it is reported as 'unknown' :(
    iface = xwiimote.iface(dev)
    return iface.get_devtype() == 'balanceboard'

def WaitForBoard():
    print("Waiting for board to connect...")
    mon = xwiimote.monitor(True, False)
    dev = None
    while True:
        print('waiting for board')
        mon.get_fd(True) # blocks
        connected = mon.poll()
        if connected == None:
            continue
        elif IsBoard(connected):
            print("Found board.")
            dev = connected
            break
        else:
            print("Waiting...")
    return dev

def GetMeasurementsFromBoard(iface, board_p):
    board_p.poll(16)  # with no argument, it blocks
    event = xwiimote.event()
    iface.dispatch(event)
    tl = event.get_abs(2)[0]
    tr = event.get_abs(0)[0]
    bl = event.get_abs(3)[0]
    br = event.get_abs(1)[0]
    return numpy.array((tl,tr,bl,br)) / 100.0

def InitBoard():
    iface = xwiimote.iface(WaitForBoard())
    iface.open(xwiimote.IFACE_BALANCE_BOARD)
    board_p = select.epoll.fromfd(iface.get_fd())
    return iface, board_p

use_board = False

iface = None
if use_board:
    iface, board_p = InitBoard()
pygame.init()
display = (1920, 1080)
screen = pygame.display.set_mode(display, DOUBLEBUF)  # |FULLSCREEN)
clock = pygame.time.Clock()
# print(pygame.font.get_fonts())
font = pygame.font.SysFont("ubuntu", 72)
text = font.render("Hello, World", True, (255, 255, 255))

sound_files = glob.glob('sounds/*.wav')
print(sound_files)
effects = []
for file in sound_files:
    effects.append(pygame.mixer.Sound(file))
sound_count = 0

image = pygame.image.load('images/glow.png')

i = 0

while True:
    if iface == None:
        m = numpy.array((0, 0, 0, 0))
    else:
        m = GetMeasurementsFromBoard(iface, board_p)
    if i == 10:
        zero = m
    i = i + 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print('quit')
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            print(sound_count)
            effect = effects[sound_count]
            effect.play()
            sound_count = sound_count + 1
    screen.fill((100, 100, 100))
    if i > 11:
        press = m - zero
        # print(press)
        if numpy.sum(press) > 10.0:
            x = 4.0 * ((press[1] + press[3]) - (press[0] + press[2])) / (numpy.sum(press))
            y = 2.0 * ((press[0] + press[1]) - (press[2] + press[3])) / (numpy.sum(press))
            screen.blit(image, (int(x * 500 + 900), int(- y * 500 + 500)))
            print(x, y)
    screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    pygame.display.flip()
    # pygame.time.wait(10)
    clock.tick(60)

