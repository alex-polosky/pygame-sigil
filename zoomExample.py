#!/usr/bin/env python
import pygame
import random

import sigil

WIDTH = 800
HEIGHT = 600
SCALE = .01
LIMIT = .01

Screen = sigil.screen.Screen((WIDTH, HEIGHT), "Zoom Test")

Camera = sigil.screen.ZoomCamera(
    0, 0, WIDTH, HEIGHT,
    0, 1000, 0, 1000,
    SCALE, LIMIT,
    #S_x=1,
    #M_x=1, P_x=1
)

Group = sigil.sprite.ZoomGroup()

image = pygame.Surface((10, 10))
pygame.draw.rect(image,
                 (255, 255, 255),
                 (0, 0, 10, 10))

image2 = pygame.Surface((10, 10))
pygame.draw.rect(image2,
                 (255, 0, 0),
                 (0, 0, 10, 10))

bg = pygame.Surface((WIDTH, HEIGHT))
bg.fill((0, 0, 0))
Screen.Display.blit(bg, (0, 0, WIDTH, HEIGHT))

sprite = sigil.sprite.ZoomSprite(
    pygame.rect.Rect(WIDTH/2-10, HEIGHT/2-10, 10, 10),
    image2,
    Camera,
)

Camera.FOLLOWING = sprite

sprite2 = sigil.sprite.ZoomSprite(
    pygame.rect.Rect(0, 0, 10, 10),
    image,
    Camera,
)
Group.add(sprite, sprite2)

####
class NewSprite(sigil.sprite.ZoomSprite):
    def update(self):
        pass
    def camUpdate(self): pass
    def zoomUpdate(self): pass


### THIS IS WHERE Robert Leachman HACKED SOME STUFF IN
image3 = pygame.Surface((100, 100))
pygame.draw.rect(image3,
                (100, 100, 100),
                (0, 0, 100, 100))

sprite3 = NewSprite(
    pygame.rect.Rect(0, 0, 100, 100),
    image3,
    Camera,
)
 # UNCOMMENT LINE TO ADD THIS SPRITE
#Group.add(sprite3)
###


for x in range(0, 100):
    X = random.randint(0, WIDTH)
    Y = random.randint(0, HEIGHT)
    Group.add(sigil.sprite.ZoomSprite(
        pygame.rect.Rect(X, Y, 10, 10),
        image,
        Camera,
    ))

Group.add(sigil.sprite.ZoomSprite(pygame.rect.Rect(30, 500, 10, 10), image, Camera))
todraw = sigil.sprite.ZoomGroup()

Clock = pygame.time.Clock()

TARGETFPS = 40
FPS = 40

running = 1

class Key(sigil.world.KeyManager):
    
    def event_QUIT(self):
        global running
        running = 0
    
    def event_m4_down(self):
        Camera.changeZoom = 1
    
    def event_m5_down(self):
        Camera.changeZoom = -1
    
    def event_ESCAPE_down(self):
        global running
        running = 0
    
    def event_f_down(self):
        if (Camera.FOLLOWING):
            Camera.FOLLOWING = None
        else:
            Camera.FOLLOWING = sprite
    
    def event_LCTRL_down(self):
        Camera.zoomScale += 1.0
    
    def event_LCTRL_up(self):
        Camera.zoomScale -= 1.0
    
    def event_LSHIFT_down(self):
        Camera.zoomScale += 1.0
    
    def event_LSHIFT_up(self):
        Camera.zoomScale -= 1.0
    
    def key_PAGEUP_pressed(self):
        Camera.changeZoom = 1
    
    def key_PAGEDOWN_pressed(self):
        Camera.changeZoom = -1
    
    def key_LEFT_pressed(self):
        Camera.MOVE_X = -1
    
    def key_RIGHT_pressed(self):
        Camera.MOVE_X = 1
    
    def key_UP_pressed(self):
        Camera.MOVE_Y = -1
    
    def key_DOWN_pressed(self):
        Camera.MOVE_Y = 1
    
    def key_w_pressed(self):
        sprite.posInWorld.y -= 5
    
    def key_s_pressed(self):
        sprite.posInWorld.y += 5
    
    def key_a_pressed(self):
        sprite.posInWorld.x -= 5
    
    def key_d_pressed(self):
        sprite.posInWorld.x += 5


K = Key()

while running:
    
    Clock.tick(TARGETFPS)
    FPS = Clock.get_fps()

    pygame.display.set_caption(
        "FPS: %d\tCamera-X: %d\tCamera-Y: %d\tCamera-Zoom: %.2f\tS-X: %d\tS-Y: %d\tW-X: %d\tW-Y: %d" %(
            FPS,
            Camera.x, Camera.y, Camera.zoom,
            sprite.rect.x, sprite.rect.y,
            sprite.posInWorld.x, sprite.posInWorld.y
            )
    )
    
    # Clear sprites
    todraw.clear(Screen.Display, bg)
    todraw.empty()

    #K.eventGet()
    #K.keyGet()
    K.queueGet()
    
    Group.update()
    Camera.update()
    Camera.zoomUpdate()
    
    Group.camUpdate()
    
    todraw.add(Camera.hit(Group.sprites()))
    
    # Draw sprites
    pygame.display.update(todraw.draw(Screen.Display))

pygame.quit()
