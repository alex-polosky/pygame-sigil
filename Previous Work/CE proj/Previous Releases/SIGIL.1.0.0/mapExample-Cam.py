#! /usr/bin/env python
import random

# It's best to import sigil this way,
# because there are certain locals that
# you can change that will affect each
# package. In the future anyways
import sigil
from sigil.locals import *

# Subclass CameraBaseWorld,
# because we will be using a camera,
# and because we want to define keypresses
class MyWorld(sigil.world.CameraBaseWorld):
    
    # The preIter happens before any other statements
    # in the game loop. We want to set the caption to
    # display data we want to look at
    # Mainly the FPS, the camera position, the
    # position of the character's offset,
    # and the position of the character in the world
    def preIter(self):
        self.screen.setCaption(
            "FPS: %d\tCamera-X: %d\tCamera-Y: %d\tS-X: %d\tS-Y: %d\tW-X: %d\tW-Y: %d" %(
                self.FPS,
                self.camera.x, self.camera.y,
                self.character.rect.x, self.character.rect.y,
                self.character.posInWorld.x, self.character.posInWorld.y
            )
        )
    
    # EVENTS only happen once, we don't want these
    # to be repeated
    
    # End the game
    def event_ESCAPE_down(self):
        self.running = 0
    
    # Follow the character
    def event_f_down(self):
        if (self.camera.FOLLOWING):
            self.camera.FOLLOWING = None
        else:
            self.camera.FOLLOWING = self.character
    
    # Key presses are repeated
    
    # Move the camera around
    # (as long as we're not following anything)
    def key_LEFT_pressed(self):
        self.camera.MOVE_X = -1
    
    def key_RIGHT_pressed(self):
        self.camera.MOVE_X = 1
    
    def key_UP_pressed(self):
        self.camera.MOVE_Y = -1
    
    def key_DOWN_pressed(self):
        self.camera.MOVE_Y = 1
    
    # Move the character around
    # The direction is used for collsion
    # (which isn't completely working)
    def key_w_pressed(self):
        self.character.move_y = -1
        self.character.direction = 'up'
    
    def key_s_pressed(self):
        self.character.move_y = 1
        self.character.direction = 'down'
    
    def key_a_pressed(self):
        self.character.move_x = -1
        self.character.direction = 'left'
    
    def key_d_pressed(self):
        self.character.move_x = 1
        self.character.direction = 'right'

    # The update is called after erasing the sprites
    # and before drawing them
    # The only this that is different than the
    # baseworld update, is the second function
    # call. In future versions, this is what
    # the standard will look like
    def update(self):
        self.sprites.update()
        
        self.sprites.collideSprite(self.character)
        
        self.camera.update()
        
        self.sprites.camUpdate()
        
        self.toDraw.add(self.camera.hit(self.sprites.sprites()))

# Create a character class that subclasses CamSprite
# (because we want a camera)
class Character(sigil.sprite.CamSprite):
    
    direction = ''
    move_x = 0
    move_y = 0
    speed_x = 5
    speed_y = 5
    
    def update(self):
        if (self.move_x == 1):
            self.posInWorld.x += self.speed_x
        elif (self.move_x == -1):
            self.posInWorld.x -= self.speed_x
        if (self.move_y == 1):
            self.posInWorld.y += self.speed_y
        elif (self.move_y == -1):
            self.posInWorld.y -= self.speed_y
        self.move_x = 0
        self.move_y = 0
        
        for x in self.groups():
            self.collideGroup(x)
        self.direction = ''

# Everything but MAP is a sigil local.
WIDTH = 800
HEIGHT = 600
TARGETFPS = 30
MAP = './example.map'

# Create the screen. If you want to access the surface created,
# call Screen.Display
Screen = sigil.screen.Screen((WIDTH, HEIGHT), "Map Test")

# Create the camera, placed at 0, 0, WIDTH, HEIGHT,
Camera = sigil.screen.Camera(
    0, 0, WIDTH, HEIGHT,
    # With X and Y bounds
    -100000, 100000, -100000, 100000,
)

# Load the map file
loadMap = sigil.parsing.getMap(MAP, Camera)
# Print it
print loadMap

# Create the background, blit to screen
# always needed to display your screen
# I want to change this though
bg = loadMap.background
Screen.Display.blit(bg, (0, 0, WIDTH, HEIGHT))
sigil.locals._pygame.display.flip()

# Create the groups needed
# The top is used to keep the character on top
# Group is all sprites
# toDraw is used to keep reference only to sprites needed
# to draw
Top = sigil.sprite.CamGroup()
Group = sigil.sprite.CamGroup()
toDraw = sigil.sprite.CamGroup()

# Create the world
World = MyWorld(
    Screen,
    Group,
    toDraw,
    bg,
    TARGETFPS,
    Camera,
    topSprites=Top
)

# Create the character and his image
# for right now, it's just a red square
charimage = sigil.tools.createRect(
    10, 10,
    (255, 0, 0)
)

# His collision type is platform
# (see sigil.sprite for more details?)
sprite = Character(
    sigil.Rect(WIDTH/2-10, HEIGHT/2-10, 10, 10),
    charimage,
    Camera,
    Platform
)

# Add the sprite to both groups
Top.add(sprite)
Group.add(sprite)


World.character = sprite

# Load the sprites from loadMap,
# and add them to the group
sprites = loadMap.createSprites()
Group.add(sprites)

# Start the loop
World.run()