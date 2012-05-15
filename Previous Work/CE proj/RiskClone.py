#! /usr/bin/env python
import random

import CameraEngine

class MyWorld(CameraEngine.world.CameraBaseWorld):
    
    def preIter(self):
        self.screen.setCaption(
            "FPS: %d\tCamera-X: %d\tCamera-Y: %d\tCamera-Zoom: %.2f" %(
                self.FPS,
                self.camera.x, self.camera.y, self.camera.zoom,
            )
        )
    
    def event_m4_down(self):
        self.camera.changeZoom = 1
    
    def event_m5_down(self):
        self.camera.changeZoom = -1
    
    def event_ESCAPE_down(self):
        self.running = 0
    
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

WIDTH = 800
HEIGHT = 600
SCALE = .01
LIMIT = 1
TARGETFPS = 40

Screen = CameraEngine.screen.Screen((WIDTH, HEIGHT), "Zoom Test")

Camera = CameraEngine.screen.ZoomCamera(
    0, 0, WIDTH, 400,
    0, WIDTH, 0, 600,
    SCALE, LIMIT,
)

map = CameraEngine.tools.loadImage('./data/board.png')

mapSprite = CameraEngine.sprite.ZoomSprite(
    CameraEngine.Rect(0, 0, 800, 400),
    map,
    Camera,
)

Group = CameraEngine.sprite.ZoomGroup()
toDraw = CameraEngine.sprite.ZoomGroup()

Group.add(mapSprite)

bg = CameraEngine.tools.createRect(
    WIDTH, HEIGHT,
    (0, 0, 0)
)

World = MyWorld(
    Screen,
    Group,
    toDraw,
    bg,
    TARGETFPS,
    Camera
)

World.run()