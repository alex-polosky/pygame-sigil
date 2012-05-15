import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

WIDTH = 800
HEIGHT = 600
CLOCK = pygame.time.Clock()
FPS = 0

pygame.init()

def pygameTest():
    global FPS, CLOCK
    display = pygame.display.set_mode((WIDTH, HEIGHT))

    while True:
        pygame.display.set_caption("FPS: "+str(FPS))
        CLOCK.tick()
        FPS = CLOCK.get_fps()
        pygame.display.flip()

def openGLTest():
    global FPS, CLOCK
    pygame.display.set_mode((WIDTH,HEIGHT), pygame.OPENGL|pygame.DOUBLEBUF)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluOrtho2D(0, WIDTH, 0, HEIGHT)
    gluOrtho2D(0, WIDTH, HEIGHT, 0)
    glMatrixMode(GL_MODELVIEW)

    glColor4f(1.0,1.0,1.0,1.0)

    done = False
    while not done:
        glBegin(GL_TRIANGLES)
        glVertex2f(10, 400)
        glVertex2f(400, 400)
        glVertex2f(400, 200)
        glEnd()

        pygame.display.set_caption("FPS: "+str(int(FPS)))
        CLOCK.tick()
        FPS = CLOCK.get_fps()
        pygame.display.flip()

#pygameTest()
openGLTest()
