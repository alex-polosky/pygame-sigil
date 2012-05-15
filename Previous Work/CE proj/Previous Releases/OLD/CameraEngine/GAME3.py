#! /usr/bin/env python
import os
import pygame
import random

os.environ["SDL_VIDEO_CENTERED"] = "1"

WIDTH = 800
HEIGHT = 600

SQUARE_SIZE = 16
CHAR_SIZE = 16
LINE_THICK = 0

SPEED_X = 20 / 4 + 1
SPEED_Y = 20 / 4 + 1

class Contain(pygame.sprite.RenderUpdates):
    pass

class Sprite(pygame.sprite.Sprite):
    
    def __init__(self, rect, color):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        
        # Create the self.image
        self.image = pygame.surface.Surface((rect.w, rect.h))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image,
                         color,
                        (0, 0, rect.w, rect.h),
                         LINE_THICK)        
    

class Fly(Sprite):
    """This is the flying object that can be controlled by the user"""

    X_DIR = 0
    Y_DIR = 0

    def update(self):
        # Take into account all changes in direction
        #self.posInWorld.x += SPEED_X_REG
        self.rect.x += self.X_DIR
        self.rect.y += self.Y_DIR

        # Reset the DIR speeds
        self.X_DIR = 0
        self.Y_DIR = 0
        
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
        
    C = Contain()
    
    for i in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        w = SQUARE_SIZE
        h = SQUARE_SIZE
        color = random.choice(colors)
        C.add(Sprite(pygame.rect.Rect(x, y, w, h), color))
        
    character = Fly(pygame.rect.Rect(0, HEIGHT/2, CHAR_SIZE, CHAR_SIZE), (255, 0, 0))
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
        clock.tick()#40)
        
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
        
        key = pygame.key.get_pressed()
        
        if key[pygame.K_w]:
            character.Y_DIR -= SPEED_Y
        if key[pygame.K_s]:
            character.Y_DIR += SPEED_Y
        if key[pygame.K_a]:
            character.X_DIR -= SPEED_X
        if key[pygame.K_d]:
            character.X_DIR += SPEED_X
        
        C.clear(Screen, blacksur)
        
        C.update()
        
        rects = C.draw(Screen)
        pygame.display.update(rects)
        
    pygame.quit()
    
if __name__ == '__main__':
    main()