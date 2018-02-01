#!/usr/bin/env python
import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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

pygame.init()
display = (1920,1080)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)  # |FULLSCREEN)
aspect_ratio = float(display[0]) / float(display[1])
gluPerspective(45, aspect_ratio, 0.1, 50.0)
glClearColor(0.3, 0.3, 0.3, 1.0)
glTranslatef(0, 0, -5)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print('quit')
            quit()
    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glTranslatef(0, 0, -1)
    DrawCube()
    glPopMatrix()
    pygame.display.flip()
    pygame.time.wait(10)
