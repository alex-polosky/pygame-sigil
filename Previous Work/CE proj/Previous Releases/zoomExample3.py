#! /usr/bin/env python
import random

import CameraEngine
from CameraEngine.locals import *

class MyWorld(CameraEngine.world.CameraBaseWorld):
    
    def preIter(self):
        self.screen.setCaption(
            "FPS: %d\tCamera-X: %d\tCamera-Y: %d\tCamera-Zoom: %.2f\tS-X: %d\tS-Y: %d\tW-X: %d\tW-Y: %d" %(
                self.FPS,
                self.camera.x, self.camera.y, self.camera.zoom,
                self.character.rect.x, self.character.rect.y,
                self.character.posInWorld.x, self.character.posInWorld.y
            )
        )
    
    def event_m4_down(self):
        self.camera.changeZoom = 1
    
    def event_m5_down(self):
        self.camera.changeZoom = -1
    
    def event_ESCAPE_down(self):
        self.running = 0
    
    def event_f_down(self):
        if (self.camera.FOLLOWING):
            self.camera.FOLLOWING = None
        else:
            self.camera.FOLLOWING = self.character
    
    def event_LCTRL_down(self):
        self.camera.zoomScale += 1.0
    
    def event_LCTRL_up(self):
        self.camera.zoomScale -= 1.0
    
    def event_LSHIFT_down(self):
        self.camera.zoomScale += 1.0
    
    def event_LSHIFT_up(self):
        self.camera.zoomScale -= 1.0
    
    def key_PAGEUP_pressed(self):
        self.camera.changeZoom = 1
    
    def key_PAGEDOWN_pressed(self):
        self.camera.changeZoom = -1
    
    def key_LEFT_pressed(self):
        self.camera.MOVE_X = -1
    
    def key_RIGHT_pressed(self):
        self.camera.MOVE_X = 1
    
    def key_UP_pressed(self):
        self.camera.MOVE_Y = -1
    
    def key_DOWN_pressed(self):
        self.camera.MOVE_Y = 1
    
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

    def update(self):
        self.sprites.update()
        
        #self.sprites.collideSprite(self.character)
        
        self.camera.update()
        if (hasattr(self.camera, "zoomUpdate")):
            self.camera.zoomUpdate()
        
        self.sprites.camUpdate()
        
        self.toDraw.add(self.camera.hit(self.sprites.sprites()))
    
    def postIter(self):
        self.character.draw(self.screen.Display)

class Character(CameraEngine.sprite.ZoomSprite):
    
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

WIDTH = 800
HEIGHT = 600
SCALE = .01
LIMIT = 1
TARGETFPS = 40

Screen = CameraEngine.screen.Screen((WIDTH, HEIGHT), "Zoom Test")
bg = CameraEngine.tools.gridBackground(
    WIDTH, HEIGHT,
    20, 
)
bg.fill(COLORS['black'])
Screen.Display.blit(bg, (0, 0, WIDTH, HEIGHT))

Camera = CameraEngine.screen.ZoomCamera(
    0, 0, WIDTH, HEIGHT,
    0, 1000, 0, HEIGHT,
    SCALE, LIMIT,
    #S_x=1,
    #M_x=1, P_x=1
)

Group = CameraEngine.sprite.ZoomGroup()
toDraw = CameraEngine.sprite.ZoomGroup()

World = MyWorld(
    Screen,
    Group,
    toDraw,
    bg,
    TARGETFPS,
    Camera
)

image = CameraEngine.tools.createRect(
    10, 10,
    #(255, 255, 255)
    COLORS['white']
)

charimage = CameraEngine.tools.createRect(
    10, 10,
    (255, 0, 0)
)

sprite = Character(
    CameraEngine.Rect(WIDTH/2-10, HEIGHT/2-10, 10, 10),
    charimage,
    Camera,
    Platform
)

sprite2 = CameraEngine.sprite.ZoomSprite(
    CameraEngine.Rect(0, 0, 10, 10),
    image,
    Camera,
)
Group.add(sprite, sprite2)

sprite3 = CameraEngine.sprite.ZoomSprite(
    CameraEngine.Rect(100, 400, 400, 300),
    CameraEngine.tools.createRect(
        400, 300,
        (COLORS['blue'])
    ),
    Camera,
    Platform
)
Group.add(sprite3)


World.character = sprite
World.camera.FOLLOWING = sprite

for x in range(0, 100):
    X = random.randint(0, WIDTH)
    Y = random.randint(0, HEIGHT)
    Group.add(CameraEngine.sprite.ZoomSprite(
        CameraEngine.Rect(X, Y, 10, 10),
        image,
        Camera,
        Platform
    ))

World.run()