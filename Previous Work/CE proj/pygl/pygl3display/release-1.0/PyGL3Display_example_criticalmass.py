"""
PyGL3Display
(C) David Griffin (2010-present)
"Habilain" is a pseudonym used by David Griffin in a number of places.

A high performance Pygame OpenGL library, capable of handling 1000s of sprites

Requirements: Python, Pygame, PyOpenGL, Open GL 2.0 graphics hardware

Licensed under GPLv2 or GPLv3. You should have received a copy of both of these
licenses in the files GPLv2.txt and GPLv3.txt. If not these licenses can be
found at http://www.gnu.org/licenses/gpl-2.0.html (GPLv2) and
http://www.gnu.org/licenses/gpl-3.0.html (GPLv3). By using this file you agree
to be bound by at least one of these licenses.

Other licenses, including commercial/proprietary licenses, can be arranged by 
contacting me via e-mail at habilain@gmail.com. If you do not have in physical 
writing an alternative license agreement from me, you must use one of the 
licenses specified above when releasing work which makes use of this library.

PyGL3Display_example_criticalmass.py

This file provides a sample game, based on the Critical Mass game by Alex
Haefner (website: alexhaefner.com). Note that this game isn't programmed that
well at all, or at least from a Game Engine design point of view.
In particular, from you should really use seperate logic and render clocks,
which isn't done here! This is only an example of how to use PyGL3Display
in it's higher performance mode.
"""

import PyGL3Display
from PyGL3Display.PyGL3Display_2dSprites import *
import random
import pygame
import os.path
from math import sqrt

class Ball(object): 
    def __init__(self, level):
        self.x = random.randint(0, level.x)
        self.y = random.randint(0, level.y)
        self.vecx, self.vecy = (random.randint(-level.maxspd, level.maxspd), random.randint(-level.maxspd, level.maxspd))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 128)
        self.sprite = GL3Sprite(image=level.ballImg, color=self.color, position=(self.x, self.y), scale=0.2)
        self.radius = 10
        self.scale = 0.2
        self.exploding = False
        self.explosion = 0
        
    def tick(self, level):
        if self.exploding is False:
            # Update the position
            self.x += self.vecx
            self.y += self.vecy
            
            if self.x < 0:
                self.x = -self.x
                self.vecx = -self.vecx
            elif self.x > level.x:
                self.x = level.x - (self.x - level.x)
                self.vecx = -self.vecx
            if self.y < 0:
                self.y = -self.y
                self.vecy = -self.vecy
            elif self.y > level.y:
                self.y = level.y - (self.y - level.y)
                self.vecy = -self.vecy    
            
            self.sprite.setPosition((self.x, self.y))
        
            # Check to see if we should be exploding
            for exploder in level.exploders:
                dx = abs(self.x - exploder.x)
                dy = abs(self.y - exploder.y)
                if dx < exploder.radius and dy < exploder.radius:
                    dist = sqrt((dx * dx) + (dy * dy))
                    if dist < exploder.radius:
                        # we explode
                        self.exploding = exploder.exploding + 1
                        self.sprite.setImage(level.bangImg)
        else:
            if self.explosion < 10:
                self.radius *= 1.1
                self.scale *= 1.1
                self.sprite.setScale(self.scale)
            if self.explosion > 100:
                self.radius /= 1.1
                self.scale /= 1.1
                self.sprite.setScale(self.scale)
            if self.radius < 2:
                self.sprite.setVisibility(False)
                self.exploding = False
            self.explosion += 1

class Bang(Ball):
    def __init__(self, level, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.vecx, self.vecy = 0, 0
        self.color = (255,255,255,255)
        self.sprite = GL3Sprite(image=level.bangImg, color=self.color, position=(self.x, self.y), scale=0.2)
        self.radius = 10
        self.scale = 0.2
        self.exploding = 0
        self.explosion = 0
        
       
class Level(object):
    def __init__(self, number, size):
        self.x, self.y = size
        self.maxspd = int(number * 0.4 + 1)
        self.balls = int((number * number) * 0.6 + (2 * number))
        self.required = (number * 0.8) * 0.8 * self.balls
        self.ballSize = max(10 - (number / 5), 1)
        self.ballImg = GL3Load('ball.png')
        self.bangImg = GL3Load('bang.png')
        self.balls = [Ball(self) for x in xrange(self.balls)]
        self.exploders = []
        self.bangPlaced = False
        self.finished = False
        
    def placeBang(self, pos):
        if not self.bangPlaced:
            self.bangPlaced = True
            self.exploders.append(Bang(self, pos))
        
    def tick(self):
        for ball in self.balls:
            ball.tick(self)
            if ball.exploding is not False:
                self.balls.remove(ball)
                self.exploders.append(ball)
        for exploder in self.exploders:
            exploder.tick(self)
            if exploder.exploding is False:
                self.exploders.remove(exploder)
        if self.bangPlaced and len(self.exploders) == 0:
            self.finished = True

def main():
    pygame.init()
    PyGL3Display.GL3Common.initEnvironment((400, 400))
    x = Level(15, (400,400))
    clock = pygame.time.Clock()
    going = True
    while going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONUP:
                x.placeBang(event.pos)
        x.tick()
        if x.finished:
            going = False
        PyGL3Display.GL3Common.doTasks()

if __name__ == '__main__':
    main()
    
