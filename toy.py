#!/usr/bin/env python
import pygame
from pygame.locals import *
import sys
import time
import select
import numpy
import xwiimote
import glob
from postures import *

''''
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
Replace the screen.blit(happy, (100, 100)) with a call to blit_alpha(screen, happy, (100, 100), 128)
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

def UpdatePoseText(last_pose_change, posture):
    pose_text = []
    for n,p in enumerate(posture):
        color = 155 + 100 * (last_pose_change == n)
        pose_text.append(font.render(p[1] + '   ' + p[3], True, (color, color, color)))
    if len(posture) == 2:
        pose_text.append(font.render('', True, (255, 255, 255)))
    return pose_text

USE_BOARD    = False
CHANGE_SOUND = 1
POSE_TIME    = 1

iface = None
if USE_BOARD:
    iface, board_p = InitBoard()

# pygame init
pygame.init()
display = (1920, 1080)
screen = pygame.display.set_mode(display, DOUBLEBUF)  # |FULLSCREEN)
clock = pygame.time.Clock()

# fonts
# print(pygame.font.get_fonts())
font = pygame.font.SysFont("ubuntu", 72)

# sounds
sound_files = glob.glob('sounds/*.wav')
print(sound_files)
effects = []
for file in sound_files:
    effects.append(pygame.mixer.Sound(file))
sound_count = 0

# images
image = pygame.image.load('images/glow.png')

pose_count = -1  # number of poses
frames = 0
before = time.time()
pose_time = time.time()
change_sound_played = False
while True:
    if (time.time() - pose_time) > POSE_TIME - 0.4:
        if not change_sound_played:
            effects[CHANGE_SOUND].play()
            change_sound_played = True
    if (time.time() - pose_time) > POSE_TIME:
        pose_count = pose_count + 1
        if pose_count < 3:
            if pose_count == 0:
                previous_posture = GenerateNewPosture(None)
            pose_text = UpdatePoseText(pose_count, previous_posture)
        else:
            last_pose_change,previous_posture = ChangeSomething(previous_posture)
            pose_text = UpdatePoseText(last_pose_change, previous_posture)
        pose_time = time.time()
        change_sound_played = False
    if iface == None:
        m = numpy.array((0, 0, 0, 0))
    else:
        m = GetMeasurementsFromBoard(iface, board_p)
    if frames == 10:
        zero = m
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print('quit')
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            print('quit')
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            print(sound_count)
            effect = effects[sound_count]
            effect.play()
            sound_count = sound_count + 1
    screen.fill((100, 100, 100))
    if frames > 11:
        press = m - zero
        # print(press)
        if numpy.sum(press) > 10.0:
            x = 4.0 * ((press[1] + press[3]) - (press[0] + press[2])) / (numpy.sum(press))
            y = 2.0 * ((press[0] + press[1]) - (press[2] + press[3])) / (numpy.sum(press))
            screen.blit(image, (int(x * 500 + 900), int(- y * 500 + 500)))
            # print(x, y)

    if pose_count > -1:
        for n,text in enumerate(pose_text):
            screen.blit(text, (1920 // 2 - text.get_width() // 2, 200 + 100 * n - text.get_height() // 2))

    pygame.display.flip()
    # pygame.time.wait(15)  # milliseconds
    # time.sleep(1.0 / 90.0)  # seconds
    clock.tick(60)  # fps
    frames = frames + 1
    if frames % 60 == 0:
        print('fps %.1f' % (float(frames) / (time.time() - before)))
