#! /usr/bin/env python
import pygame
import random

import CameraEngine

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
        self.character.posInWorld.y -= 5
    
    def key_s_pressed(self):
        self.character.posInWorld.y += 5
    
    def key_a_pressed(self):
        self.character.posInWorld.x -= 5
    
    def key_d_pressed(self):
        self.character.posInWorld.x += 5

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
Screen.Display.blit(bg, (0, 0, WIDTH, HEIGHT))

Camera = CameraEngine.screen.ZoomCamera(
    0, 0, WIDTH, HEIGHT,
    0, 1000, 0, HEIGHT,
    SCALE, LIMIT,
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

charimage = CameraEngine.tools.createRect(
    10, 10,
    (255, 0, 0)
)

sprite = CameraEngine.sprite.ZoomSprite(
    pygame.rect.Rect(WIDTH/2-10, HEIGHT/2-10, 10, 10),
    charimage,
    Camera,
)
Group.add(sprite)

World.character = sprite

World.run()