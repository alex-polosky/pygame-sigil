#! /usr/bin/env python
import os
import pygame
import random

import sys
f = sys.stdout
a = 0

os.environ["SDL_VIDEO_CENTERED"] = "1"

#WIDTH = 640
#HEIGHT = 480
WIDTH = 800
HEIGHT = 600
#WIDTH = 320
#HEIGHT = 320

#BOUND_X_NEG = 600
#BOUND_X_POS = 50000 + BOUND_X_NEG
#BOUND_Y_NEG = 100
#BOUND_Y_POS = 670

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
LINE_THICK = 2

SPEED_X_CAM = 20 /4
SPEED_Y_CAM = 20 /4
SPEED_X_CAM_NORM = 20 /4

SPEED_X_REG = 5#10 /4
SPEED_X = 20 / 4 + 1#20 /3
SPEED_Y = 20 / 4 + 1#20 /3

WALL_BORDER = 5
WALL_BORDER_RIGHT = WALL_BORDER + CHAR_SIZE


class QuadTree(object):
    """Create a Quad Tree Object
    """

    items = None

    def __init__(self, items):      
        """Create a Quad Tree Object
 
        @param items:
            List of Rect items
        """
        if (
            (type(items) != type([]))
            or
            (type(items) != type((None, None)))
            ):
            self.items = items
        else:
            raise BaseException("Items must be of type list")

    def hit(self, rect):        
        """Return a list of items that collide with rect
 
        @param rect:
            pygame rect or similar
            Must have right, left, top, and bottom attributes
        """
        hits = []
        
        #for x in self.items:
        #    if ((rect.right >= x.left)
        #        and
        #        (x.left <= x.right)
        #        and
        #        (x.bottom >= x.top)
        #        and
        #        (x.top <= x.bottom)):
        #        hits.append(x)
        for x in self.items:
            if (
                (rect.right >= x.left)
                and
                (rect.left <= x.right)
                and
                (rect.top <= x.bottom)
                and
                (rect.bottom >= x.top)
               ):
                hits.append(x)

        return hits

class Item(pygame.rect.Rect):

    """A class used as an enhanced Rect"""
    
    def __init__(self, left, top, width, height, color=(255, 255, 255)):
        """Enhanced Pygame Rect for Drawing"""
        pygame.rect.Rect.__init__(self, left, top, width, height)
        self.color = color
        
    def draw(self, screen, camera, color=None):
        """Draw to surface"""
        if color == None: color = self.color
        x = self.left - camera.x
        y = self.top - camera.y
        w = self.right - self.left
        h = self.bottom - self.top
        pygame.draw.rect(screen,
                         color,
                         [x, y, w, h],
                         LINE_THICK)

    def update(self, camera):
        pass

class Fly(Item):
    """This is the flying object that can be controlled by the user"""

    X_DIR = 0
    Y_DIR = 0

    def update(self, camera):
        # Take into account all changes in direction
        self.x += SPEED_X_REG
        self.x += self.X_DIR
        self.y += self.Y_DIR

        x = self.left - camera.x
        y = self.top - camera.y
        # Keep from colliding into the borders
        if (x <= WALL_BORDER):
            self.x = camera.x + WALL_BORDER
        if (x >= WIDTH - WALL_BORDER_RIGHT):
            self.x = camera.right - WALL_BORDER_RIGHT
        if (y <= WALL_BORDER):
            self.y = camera.y + WALL_BORDER
        if (y >= HEIGHT - WALL_BORDER_RIGHT):
            self.y = camera.bottom - WALL_BORDER_RIGHT

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
    
    def inputcoordthis(camera):
        x = int(raw_input('x coord'))
        y = int(raw_input('y coord'))
        camera.x = x
        camera.y = y

    colors = [
    (255, 255, 255), # WHITE
    (255, 255, 0),   # YELLOW
    (255, 0, 255),   # PURPLE
    (0, 255, 255),   # CYAN
    (0, 255, 0),     # GREEN
    #(255, 0, 0),     # RED
    (0, 0, 255)      # BLUE
    ]

    # Create the objects that will fill the Screen
    items = []
    character = []
    for i in range(SQUARE_NUM):
        x = random.randint(BOUND_X_NEG, BOUND_X_POS)
        y = random.randint(-BOUND_Y_NEG, BOUND_Y_POS)
        w = SQUARE_SIZE
        h = SQUARE_SIZE
        color = random.choice(colors)
        items.append(Item(x, y, w, h, color))

    # Create the user controlled flyer
    F = Fly(0, HEIGHT/2, CHAR_SIZE, CHAR_SIZE, (255, 0, 0))
    items.append(F)
    character.append(F)

    # Put the objects into the tree
    tree = QuadTree(items)

    # Create the screen and camera
    FULLSCREEN = 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    camera = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)
    #camera2 = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)
    #_camera = camera
    
    # Setup the clock
    clock = pygame.time.Clock()
    
    running = 1
    
    inputcoord = 0

    while running:

        # Set caption
        pygame.display.set_caption("WSAD Moves\tFPS: %d\tCamera-X: %d\tCamera-Y: %d" %(clock.get_fps(), camera.x, camera.y))

        # Slow Frames Per Second
        clock.tick(40)
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
                    camera.x = 0
                    camera.y = 0
                    character[0].x = 0
                    character[0].y = HEIGHT/2
                elif (event.key == pygame.K_f):
                    if (FULLSCREEN == 0):
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                        FULLSCREEN = 1
                    elif (FULLSCREEN == 1):
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        FULLSCREEN = 0
                #elif (event.key == pygame.K_c):
                #    _camera = camera
                #    camera = camera2
                #    camera2 = _camera
                if (event.key == pygame.K_LCTRL):
                    inputcoord = 1
                if (event.key == pygame.K_c):
                    if (inputcoord == 1):
                        inputcoordthis(camera)
                        inputcoord = 0
                    #else:
                    #    _camera = camera
                    #    camera = camera2
                    #    camera2 = _camera
                        
            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_LCTRL):
                    inputcoord = 0

        key = pygame.key.get_pressed()
        ################
        ################
        ## UNCOMMENT THE FOLLOWING
        ## REGION TO REGAIN CONTROL
        ## OVER THE CAMERA
        if key[pygame.K_LEFT]:
            camera.x -= SPEED_X_CAM
        if key[pygame.K_RIGHT]:
            camera.x += SPEED_X_CAM
        if key[pygame.K_UP]:
            camera.y -= SPEED_Y_CAM
        if key[pygame.K_DOWN]:
            camera.y += SPEED_Y_CAM
        
        # Move the camera
        camera.x += SPEED_X_CAM_NORM#SPEED_X_CAM
        # Check the camera
        if (camera.x <= CAM_BOUND_X_NEG):
            camera.x = CAM_BOUND_X_NEG
        if (camera.x >= CAM_BOUND_X_POS):
            camera.x = CAM_BOUND_X_POS
        ###############
        ###############
        ## UNCOMMENT THE FOLLOWING
        ## REGION IF USING FULL CAMERA
        if (camera.y <= CAM_BOUND_Y_NEG):
            camera.y = CAM_BOUND_Y_NEG
        if (camera.y >= CAM_BOUND_Y_POS):
            camera.y = CAM_BOUND_Y_POS

        if key[pygame.K_w]:
            character[0].Y_DIR -= SPEED_Y
        if key[pygame.K_s]:
            character[0].Y_DIR += SPEED_Y
        if key[pygame.K_a]:
            character[0].X_DIR -= SPEED_X
        if key[pygame.K_d]:
            character[0].X_DIR += SPEED_X
            
        # Use the quad-tree to restrict which items we're going to draw.
        visible_items = tree.hit(camera)

        # Draw the visible items only.
        # The draw function takes care of translation
        #  according to the camera object
        screen.fill((0, 0, 0))
        character[0].update(camera)
        for item in visible_items:
            item.draw(screen, camera)#, random.choice(colors))
        pygame.display.flip()
        
        #if (a == 100):
        #    os.system('clear')
        #    f.write('World - x: %d\ty: %d\n' %(character[0].x, character[0].y))
        #    f.write('Cam   - x: %d\ty: %d\n' %(character[0].rect.x, character[0].rect.y))
        #    f.write('Camera- x: %d\ty: %d\n' %(camera.x, camera.y))
        #    f.write('\n')
        #    a = 0
        #a += 1

    pygame.quit()

if __name__ == '__main__':
    main()
