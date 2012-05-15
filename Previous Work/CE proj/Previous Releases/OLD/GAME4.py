#! /usr/bin/env python
import os
import pygame
import random

import CameraEngine

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
            self.rect.x = self.camera.x + WALL_BORDER
            self.posInWorld.x = self.rect.x + self.camera.x
        if (self.rect.x >= WIDTH - WALL_BORDER_RIGHT):
            self.rect.x = self.camera.right - WALL_BORDER_RIGHT
            self.posInWorld.x = self.rect.x + self.camera.x
        
        if (self.rect.y <= WALL_BORDER):
            self.rect.y = self.camera.y + WALL_BORDER
            self.posInWorld.y = self.rect.y + self.camera.y
        if (self.rect.y >= HEIGHT - WALL_BORDER_RIGHT):
            self.rect.y = self.camera.bottom - WALL_BORDER_RIGHT
            self.posInWorld.y = self.rect.y + self.camera.y

def pause_loop():
    pygame.display.set_caption("PAUSED!")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return
            
def main():
    
    colors = [
    (255, 255, 255), # WHITE
    (255, 255, 0),   # YELLOW
    (255, 0, 255),   # PURPLE
    (0, 255, 255),   # CYAN
    (0, 255, 0),     # GREEN
    #(255, 0, 0),     # RED
    (0, 0, 255)      # BLUE
    ]
        
    Camera = CameraEngine.screen.Camera(0, 0, WIDTH, HEIGHT,
                           CAM_BOUND_X_NEG, CAM_BOUND_X_POS,
                           CAM_BOUND_Y_NEG, CAM_BOUND_Y_POS,
                           SPEED_X_CAM, SPEED_Y_CAM,)
    C = Contain()
    
    for i in range(SQUARE_NUM):
        x = random.randint(BOUND_X_NEG, BOUND_X_POS)
        y = random.randint(-BOUND_Y_NEG, BOUND_Y_POS)
        w = SQUARE_SIZE
        h = SQUARE_SIZE
        color = random.choice(colors)
        C.add(Sprite(Camera, pygame.rect.Rect(x, y, w, h), color))
        
    character = Fly(Camera, pygame.rect.Rect(0, HEIGHT/2, CHAR_SIZE, CHAR_SIZE), (255, 0, 0))
    C.add(character)

    # Create the screen and camera
    FULLSCREEN = 0
    Screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    blacksur = pygame.surface.Surface((WIDTH, HEIGHT))
    blacksur.fill((0, 0, 0))
    
    # Setup the clock
    clock = pygame.time.Clock()
    
    running = 1
    
    while running:
        pygame.display.set_caption("WSAD Moves\tFPS: %d" %(clock.get_fps()))
        
        # Slow Frames Per Second
        clock.tick(40)#40)
        
        # Get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    running = 0
            ### PAUSE
                elif (event.key == pygame.K_p):
                    pause_loop()
            ### RESTART
                elif (event.key == pygame.K_r):
                    pass
            ### FULLSCREEN
                elif (event.key == pygame.K_f):
                    if (FULLSCREEN == 0):
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                        FULLSCREEN = 1
                    elif (FULLSCREEN == 1):
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        FULLSCREEN = 0
        
        # Get keys pressed
        key = pygame.key.get_pressed()
        
        # Change any location for keys
        if key[pygame.K_w]:
            character.Y_DIR -= SPEED_Y
        if key[pygame.K_s]:
            character.Y_DIR += SPEED_Y
        if key[pygame.K_a]:
            character.X_DIR -= SPEED_X
        if key[pygame.K_d]:
            character.X_DIR += SPEED_X
        
        # Clear the screen of sprites
        C.clear(Screen, blacksur)
        
        # Update all of the sprites
        # and camera
        C.update()
        C.camUpdate()
        Camera.update()
        
        # draw the sprites
        rects = C.draw(Screen)
        character.draw(Screen)
        pygame.display.update(rects)
        
    pygame.quit()
    
if __name__ == '__main__':
    main()