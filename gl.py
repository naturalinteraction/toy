import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import time
import select
import numpy
import xwiimote

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

vertices= (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

def DrawCube():
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

device = wait_for_balanceboard()
iface = xwiimote.iface(device)
iface.open(xwiimote.IFACE_BALANCE_BOARD)
pygame.init()
display = (1920,1080)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)  # |FULLSCREEN)
aspect_ratio = float(display[0]) / float(display[1])
gluPerspective(45, aspect_ratio, 0.1, 50.0)
glClearColor(0.3, 0.3, 0.3, 1.0)
i = 0
try:
    for m in measurements(iface):
        #print('topleft%.2f'      % (float(m[0]) / 100.0) + 
        #      ' topright%.2f'    % (float(m[1]) / 100.0) + 
        #      ' bottomleft%.2f'  % (float(m[2]) / 100.0) + 
        #      ' bottomright%.2f' % (float(m[3]) / 100.0))
        m = numpy.array(m) / 100.0
        if i > 60 * 60:
            quit()
        if i == 10:
            zero = m
        i = i + 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print('quit')
                quit()
        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if i > 11:
            press = m - zero
            # print(press)
            if numpy.sum(press) > 10.0:
                x = 4.0 * ((press[1] + press[3]) - (press[0] + press[2])) / (numpy.sum(press))
                y = 2.0 * ((press[0] + press[1]) - (press[2] + press[3])) / (numpy.sum(press))
                print(x,y)
                glPushMatrix()
                glTranslatef(x, y, -5)
                DrawCube()
                glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)
except:
    quit()
