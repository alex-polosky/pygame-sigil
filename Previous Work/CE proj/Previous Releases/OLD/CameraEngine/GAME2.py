#! /usr/bin/env python
import os
import pygame
import random

import screen as SCREEN
#f = open("log.game2.py.txt", 'a')

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
LINE_THICK = 2

SPEED_X_CAM = 20 /4
SPEED_Y_CAM = 20 /4
SPEED_X_CAM_NORM = 20 /4

SPEED_X_REG = 5#10 /4
SPEED_X = 20 / 4 + 1#20 /3
SPEED_Y = 20 / 4 + 1#20 /3

WALL_BORDER = 5
WALL_BORDER_RIGHT = WALL_BORDER + CHAR_SIZE


class CamTree(pygame.sprite.RenderUpdates):

    def __init__(self, *sprites):      
        """Create a Quad Tree Object
        """
        pygame.sprite.RenderUpdates.__init__(self, sprites)

    def hit(self):#, cam):        
        """Return a list of items that collide with rect
 
        @param rect:
            pygame rect or similar
            Must have right, left, top, and bottom attributes
            Should be the camera.
        """
        hits = []
        
        for x in self.sprites():
            if (
                (x.camera.right >= x.posInWorld.left)
                and
                (x.camera.left <= x.posInWorld.right)
                and
                (x.camera.top <= x.posInWorld.bottom)
                and
                (x.camera.bottom >= x.posInWorld.top)
               ):
                hits.append(x)

        return CamTree(hits)
    
    def getObjs(self, Obj, limit=0, sprites=None):
        ''' The Obj is another sprite to intersect
            if limit is 0, hit is called first
            if sprites is not none, that is used instead'''
        temp = []
        if (sprites == None):
            if limit == 0:
                sprites = self.sprites()
            elif limit != 0:
                sprites = self.hit()
            for x in sprites:
                if hasattr(Obj, 'rect'):
                    if Obj.rect.colliderect(x.rect):
                        temp.append(x)
                else:
                    if Obj.colliderect(x.rect):
                        temp.append(x)
        else:
            for x in sprites:
                if hasattr(Obj, 'rect'):
                    if Obj.rect.colliderect(x.rect):
                        temp.append(x)
                else:
                    if Obj.colliderect(x.rect):
                        temp.append(x)
        return temp
    
    def camUpdate(self):
        for x in self.sprites():
            x.rect.x = x.posInWorld.x - x.camera.x
            x.rect.y = x.posInWorld.y - x.camera.y
            #x.rect.w = x.posInWorld.right - x.camera.left
            #x.rect.h = x.posInWorld.bottom - x.camera.top

class CamSprite(pygame.sprite.Sprite):
    
    def __init__(self, camera, rect1, color=(255,255,255), rect2=None):
        self.camera = camera
        pygame.sprite.Sprite.__init__(self)
        self.posInWorld = rect1
        if (rect2 != None):
            self.posCamera = self.rect = rect2
        else:
            self.posCamera = self.rect = \
                pygame.rect.Rect(rect1.x, rect1.y,
                          rect1.w, rect1.h)
        
        # Create the self.image
        self.image = pygame.surface.Surface((rect1.w, rect1.h))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image,
                         color,
                         #[0, 0, rect1.w, rect1.h],
                        (0, 0, rect1.w, rect1.h),
                         LINE_THICK)

    def changecam(self, camera):
        self.camera = camera
    
    def drawcam(self, surface):
        self.draw(surface)
    
    def clearcam(self, surface, camera):
        pass

    def update(self, camera=None):
        if (camera != None):
            self.changecam(camera)

class Fly(CamSprite):
    """This is the flying object that can be controlled by the user"""

    X_DIR = 0
    Y_DIR = 0

    def update(self):
        # Take into account all changes in direction
        #self.posInWorld.x += SPEED_X_REG
        self.posInWorld.x += self.X_DIR
        self.posInWorld.y += self.Y_DIR

        x = self.rect.x
        y = self.rect.y
        # Keep from colliding into the borders
        #if (x <= WALL_BORDER):
        #    self.posInWorld.x = self.camera.x + WALL_BORDER
        #if (x >= WIDTH - WALL_BORDER_RIGHT):
        #    self.posInWorld.x = self.camera.right - WALL_BORDER_RIGHT
        #if (y <= WALL_BORDER):
        #    self.posInWorld.y = self.camera.y + WALL_BORDER
        #if (y >= HEIGHT - WALL_BORDER_RIGHT):
        #    self.posInWorld.y = self.camera.bottom - WALL_BORDER_RIGHT

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
    
    Camera = SCREEN.Camera(0, 0, WIDTH, HEIGHT,
                           CAM_BOUND_X_NEG, CAM_BOUND_X_POS,
                           CAM_BOUND_Y_NEG, CAM_BOUND_Y_POS,
                           SPEED_X_CAM, SPEED_Y_CAM,)
                           #                           )

    # Create the objects that will fill the Screen
    items = CamTree()
    character = []
    for i in range(SQUARE_NUM):
        x = random.randint(BOUND_X_NEG, BOUND_X_POS)
        y = random.randint(-BOUND_Y_NEG, BOUND_Y_POS)
        w = SQUARE_SIZE
        h = SQUARE_SIZE
        color = random.choice(colors)
        items.add(CamSprite(Camera, pygame.rect.Rect(x, y, w, h), color))

    # Create the user controlled flyer
    #F = Fly(0, HEIGHT/2, CHAR_SIZE, CHAR_SIZE, (255, 0, 0))
    F = Fly(Camera, pygame.rect.Rect(0, HEIGHT/2, CHAR_SIZE, CHAR_SIZE), (255, 0, 0))
    items.add(F)
    character.append(F)

    # Create the screen and camera
    FULLSCREEN = 0
    Screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    blacksur = pygame.surface.Surface((WIDTH, HEIGHT))
    blacksur.fill((0, 0, 0))
    #camera = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)
    #camera2 = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)
    #_camera = camera
    
    # Setup the clock
    clock = pygame.time.Clock()
    
    running = 1
    
    inputcoord = 0

    while running:

        # Set caption
        pygame.display.set_caption("WSAD Moves\tFPS: %d\tCamera-X: %d\tCamera-Y: %d" %(clock.get_fps(), Camera.x, Camera.y))

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
        
        # Move the camera
        #camera.x += SPEED_X_CAM_NORM#SPEED_X_CAM
        # Check the camera
        #if (camera.x <= CAM_BOUND_X_NEG):
        #    camera.x = CAM_BOUND_X_NEG
        #if (camera.x >= CAM_BOUND_X_POS):
        #    camera.x = CAM_BOUND_X_POS
        ###############
        ###############
        ## UNCOMMENT THE FOLLOWING
        ## REGION IF USING FULL CAMERA
        #if (camera.y <= CAM_BOUND_Y_NEG):
        #    camera.y = CAM_BOUND_Y_NEG
        #if (camera.y >= CAM_BOUND_Y_POS):
        #    camera.y = CAM_BOUND_Y_POS

        if key[pygame.K_w]:
            character[0].Y_DIR -= SPEED_Y
        if key[pygame.K_s]:
            character[0].Y_DIR += SPEED_Y
        if key[pygame.K_a]:
            character[0].X_DIR -= SPEED_X
        if key[pygame.K_d]:
            character[0].X_DIR += SPEED_X
            
        # Use the quad-tree to restrict which items we're going to draw.
        visible_items = items.hit()
        visible_items.add(character[0])

        # Draw the visible items only.
        # The draw function takes care of translation
        #  according to the camera object
        #Screen.fill((0, 0, 0))
        visible_items.clear(Screen, blacksur)
        
        
        ################
        ################
        ## UNCOMMENT THE FOLLOWING
        ## REGION TO REGAIN CONTROL
        ## OVER THE CAMERA
        if key[pygame.K_LEFT]:
            Camera.x -= SPEED_X_CAM
        if key[pygame.K_RIGHT]:
            Camera.x += SPEED_X_CAM
        if key[pygame.K_UP]:
            Camera.y -= SPEED_Y_CAM
        if key[pygame.K_DOWN]:
            Camera.y += SPEED_Y_CAM
        
        character[0].update()
        visible_items.camUpdate()
        rects = visible_items.draw(Screen)
        pygame.display.update()#rects)
        
        del visible_items

        #f.write('x: %d\ty: %d\n' %(character[0].rect.x, character[0].rect.y))
        #f.write('real-x: %d\treal-y: %d\n' %(character[0].posInWorld.x, character[0].posInWorld.y))
        #f.write('cam-x: %d\tcam-y: %d\n' %(character[0].posCamera.x, character[0].posCamera.y))
        #f.write('\n')

    pygame.quit()

if __name__ == '__main__':
    main()
