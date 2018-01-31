import pygame
from pygame.locals import *
import sys
import time
import select
import numpy
import xwiimote
import glob

def dev_is_balanceboard(dev):
    time.sleep(2) # if we check the devtype to early it is reported as 'unknown' :(
    iface = xwiimote.iface(dev)
    return iface.get_devtype() == 'balanceboard'

def wait_for_balanceboard():
    print("Waiting for balanceboard to connect...")
    mon = xwiimote.monitor(True, False)
    dev = None
    while True:
        mon.get_fd(True) # blocks
        connected = mon.poll()
        if connected == None:
            continue
        elif dev_is_balanceboard(connected):
            print("Found balanceboard:", connected)
            dev = connected
            break
        else:
            # print("Found non-balanceboard device:", connected)
            # print("Waiting..")
            pass
    return dev

def measurements(iface):
    p = select.epoll.fromfd(iface.get_fd())
    while True:
        p.poll()  # blocks
        event = xwiimote.event()
        iface.dispatch(event)
        tl = event.get_abs(2)[0]
        tr = event.get_abs(0)[0]
        bl = event.get_abs(3)[0]
        br = event.get_abs(1)[0]
        yield (tl,tr,bl,br)

device = wait_for_balanceboard()
iface = xwiimote.iface(device)
iface.open(xwiimote.IFACE_BALANCE_BOARD)
pygame.init()
display = (1920, 1080)
screen = pygame.display.set_mode(display, DOUBLEBUF)  # |FULLSCREEN)
clock = pygame.time.Clock()
aspect_ratio = float(display[0]) / float(display[1])
i = 0
done = False
font = pygame.font.SysFont("Arial", 72)
text = font.render("Hello, World", True, (255, 255, 255))
sound_files = glob.glob('sounds/*.wav')
print(sound_files)
effects = []
for file in sound_files:
    effects.append(pygame.mixer.Sound(file))
count = 0
image = pygame.image.load('images/glow.png')
try:
    for m in measurements(iface):
        #print('topleft%.2f'      % (float(m[0]) / 100.0) + 
        #      ' topright%.2f'    % (float(m[1]) / 100.0) + 
        #      ' bottomleft%.2f'  % (float(m[2]) / 100.0) + 
        #      ' bottomright%.2f' % (float(m[3]) / 100.0))
        m = numpy.array(m) / 100.0
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
                print(count)
                effect = effects[count]
                effect.play()
                count = count + 1
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
except:
    quit()
