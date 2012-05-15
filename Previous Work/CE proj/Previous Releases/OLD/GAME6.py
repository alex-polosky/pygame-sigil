#! /usr/bin/env python
import os
import pygame
import random

import CameraEngine

#f = open('log.GAME5.py.txt', 'a')
import sys
f = sys.stdout

os.environ["SDL_VIDEO_CENTERED"] = "1"

WIDTH = 800
HEIGHT = 600

BOUND_X_NEG = WIDTH - (WIDTH/2)
BOUND_X_POS = 50000 + BOUND_X_NEG
BOUND_Y_NEG = 10
BOUND_Y_POS = HEIGHT + BOUND_Y_NEG

CAM_BOUND_X_NEG = 0
CAM_BOUND_X_POS = BOUND_X_POS - WIDTH
CAM_BOUND_Y_NEG = 0
CAM_BOUND_Y_POS = 0

SQUARE_NUM = 5000
SQUARE_SIZE = 16
CHAR_SIZE = 16
LINE_THICK = 0

SPEED_X_CAM = 20 /4
SPEED_Y_CAM = 20 /4
SPEED_X_CAM_NORM = 0

SPEED_X_REG = 0
SPEED_X = 20 / 4 + 1
SPEED_Y = 20 / 4 + 1

WALL_BORDER = 5
WALL_BORDER_RIGHT = WALL_BORDER + CHAR_SIZE

GRID = 20

class Contain(CameraEngine.sprite.CamTree):
    pass

class Sprite(CameraEngine.sprite.CamSprite):
    
    pass      
    

class Fly(Sprite):
    """This is the flying object that can be controlled by the user"""

    X_DIR = 0
    Y_DIR = 0
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        # Take into account all changes in direction
        #self.posInWorld.x += SPEED_X_REG
        self.posInWorld.x += self.X_DIR
        self.posInWorld.y += self.Y_DIR

        # Reset the DIR speeds
        self.X_DIR = 0
        self.Y_DIR = 0
        
    def camUpdate(self):
        self.rect.x = self.posInWorld.x - self.camera.x
        self.rect.y = self.posInWorld.y - self.camera.y
        
        if (self.rect.x <= WALL_BORDER):
            self.posInWorld.x = self.camera.x + WALL_BORDER
            self.rect.x = self.posInWorld.x - self.camera.x
        if (self.rect.x >= WIDTH - WALL_BORDER_RIGHT):
            self.posInWorld.x = self.camera.right - WALL_BORDER_RIGHT
            self.rect.x = self.posInWorld.x - self.camera.x
        
        if (self.rect.y <= WALL_BORDER):
            self.posInWorld.y = self.camera.y + WALL_BORDER
            self.rect.y = self.posInWorld.y - self.camera.y
        if (self.rect.y >= HEIGHT - WALL_BORDER_RIGHT):
            self.posInWorld.y = self.camera.bottom - WALL_BORDER_RIGHT
            self.rect.y = self.posInWorld.y - self.camera.y

class Loop(CameraEngine.loops.Loop):
    
    def preLoop(self, Camera):
        colors = [
        (255, 255, 255), # WHITE
        (255, 255, 0),   # YELLOW
        (255, 0, 255),   # PURPLE
        (0, 255, 255),   # CYAN
        (0, 255, 0),     # GREEN
        #(255, 0, 0),     # RED
        (0, 0, 255)      # BLUE
        ]
        
        # These two are containers for sprites
        # First one is ALL sprites
        # second one is only for drawing
        self.C = Contain()
        self.todraw = Contain()
        
        for i in range(SQUARE_NUM):
            x = random.randint(BOUND_X_NEG, BOUND_X_POS)
            y = random.randint(-BOUND_Y_NEG, BOUND_Y_POS)
            w = SQUARE_SIZE
            h = SQUARE_SIZE
            color = random.choice(colors)
            self.C.add(Sprite(Camera, pygame.rect.Rect(x, y, w, h), color))
            
        self.character = Fly(Camera, pygame.rect.Rect(0, HEIGHT/2, CHAR_SIZE, CHAR_SIZE), (255, 0, 0))
        self.C.add(self.character)
    
        # This is the background
        self.background = CameraEngine.tools.gridBackground(800, 600, 20)
        self.screen.blit(self.background, (0, 0, 800, 600))
        pygame.display.flip()
    
    def preIter(self):
        self.setCaption('WSAD Moves!\tFPS: %d' %(self.clock.get_fps()))

    def clearSprites(self):
        self.todraw.clear(self.screen, self.background)
        self.todraw.empty()
        
    def updateSprites(self, sprites, camera):
        sprites.update()
        camera.update()
        sprites.camUpdate()
        
    def keyGet(self, camera):
        # Get keys pressed
        key = pygame.key.get_pressed()
        
        # Change any location for keys
        if key[pygame.K_w]:
            self.character.Y_DIR -= SPEED_Y
        if key[pygame.K_s]:
            self.character.Y_DIR += SPEED_Y
        if key[pygame.K_a]:
            self.character.X_DIR -= SPEED_X
        if key[pygame.K_d]:
            self.character.X_DIR += SPEED_X
            
        if key[pygame.K_LEFT]:
            camera.MOVE_X = -1
        if key[pygame.K_RIGHT]:
            camera.MOVE_X = 1
        if key[pygame.K_UP]:
            camera.MOVE_Y = -1
        if key[pygame.K_DOWN]:
            camera.MOVE_Y = 1
            
    def postIter(self):
        if (self._debug):
            self._debug = 0
            while 1:
                try:
                    exec(raw_input(">> "))
                except KeyboardInterrupt:
                    break
                except:
                    print("Error")
        
    def mainLoop(self, framecap, camera):
        self.preLoop(camera)
        
        self.running = 1
        while self.running:
            self.preIter()
            
            self.clockTick(framecap)
            
            self.clearSprites()
            self.updateSprites(self.C, camera)
            
            self.todraw.add(self.C.hit())
            
            self.drawSprites(self.todraw)
            
            #self.updateScreen()
            
            self.eventGet()
            self.keyGet(camera)
            
            self.postIter()
            
        self.postLoop()

def main():
    Screen = pygame.display.set_mode((WIDTH, HEIGHT))
    Camera = CameraEngine.screen.Camera(
                           #0, 0, WIDTH, HEIGHT,
                           0, 0, WIDTH, HEIGHT-100,
                           CAM_BOUND_X_NEG, CAM_BOUND_X_POS,
                           CAM_BOUND_Y_NEG, CAM_BOUND_Y_POS,
                           SPEED_X_CAM, SPEED_Y_CAM,)
    Clock = pygame.time.Clock()
    
    L = Loop(Screen, Clock, None)
    
    L.mainLoop(40, Camera)
    
if __name__ == '__main__':
    import cProfile as profile
    profile.run('main()')
    #main()