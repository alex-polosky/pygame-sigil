#!/usr/bin/env python
import pygame
import random

import CameraEngine

WIDTH = 800
HEIGHT = 600
SCALE = .1

Screen = CameraEngine.screen.Screen((WIDTH, HEIGHT), "Zoom Test")

Camera = CameraEngine.screen.ZoomCamera(
    0, 0, WIDTH, HEIGHT-200,
    -1000, 1000, -1000, 1000,
    SCALE
)

Group = CameraEngine.sprite.ZoomGroup()

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

sprite = CameraEngine.sprite.ZoomSprite(
    pygame.rect.Rect(WIDTH/2-10, HEIGHT/2-10, 10, 10),
    image2,
    Camera,
    SCALE,
    1
)
sprite2 = CameraEngine.sprite.ZoomSprite(
    pygame.rect.Rect(0, 0, 10, 10),
    image,
    Camera,
    SCALE,
    1
)
Group.add(sprite, sprite2)
####
class NewSprite(CameraEngine.sprite.ZoomSprite):
    def update(self):
        pass
    def camUpdate(self): pass
    def zoomUpdate(self): pass


### THIS IS WHERE Robert Leachman HACKED SOME STUFF IN
#image3 = pygame.Surface((WIDTH, HEIGHT))
#pygame.draw.rect(image3,
#(100, 100, 100),
#(0, 0, 100, 100))##

#sprite3 = NewSprite(#CameraEngine.sprite.ZoomSprite(
#pygame.rect.Rect(0, 0, WIDTH, HEIGHT),
#image3,
#Camera,
#SCALE,
#1
#)
#Group.add(sprite3)
###


for x in range(0, 100):
    X = random.randint(0, WIDTH)
    Y = random.randint(0, HEIGHT)
    Group.add(CameraEngine.sprite.ZoomSprite(
        pygame.rect.Rect(X, Y, 10, 10),
        image,
        Camera,
        SCALE,
        1
    ))

Group.add(CameraEngine.sprite.ZoomSprite(pygame.rect.Rect(30, 500, 10, 10), image, Camera, SCALE, 1))
todraw = CameraEngine.sprite.ZoomGroup()

Clock = pygame.time.Clock()

TARGETFPS = 40
FPS = 40

while True:
    
    Clock.tick(TARGETFPS)
    FPS = Clock.get_fps()

    pygame.display.set_caption(
        "FPS: %d\tCamera-X: %d\tCamera-Y: %d\tS-X: %d\tS-Y: %d\tW-X: %d\tW-Y: %d" %(
            FPS,
            Camera.x, Camera.y,
            sprite.rect.x, sprite.rect.y,
            sprite.posInWorld.x, sprite.posInWorld.y
            )
    )
    
    # Clear sprites
    todraw.clear(Screen.Display, bg)
    todraw.empty()
    
    # Get input, update sprites
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            break
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (event.button == 4):
                #sprite.zoom += sprite.zoomScale
                Group.setGroupAttr('changeZoom', 1)
                Camera.changeZoom = 1
            if (event.button == 5):
                #sprite.zoom -= sprite.zoomScale
                Group.setGroupAttr('changeZoom', -1)
                Camera.changeZoom = 1
    key = pygame.key.get_pressed()
    
    if key[pygame.K_PAGEUP]:
        Group.setGroupAttr('changeZoom', 1)
        Camera.changeZoom = 1
    if key[pygame.K_PAGEDOWN]:
        Group.setGroupAttr('changeZoom', -1)
        Camera.changeZoom = 1
    
    if key[pygame.K_LEFT]:
        Camera.MOVE_X = -1
    if key[pygame.K_RIGHT]:
        Camera.MOVE_X = 1
    if key[pygame.K_UP]:
        Camera.MOVE_Y = -1
    if key[pygame.K_DOWN]:
        Camera.MOVE_Y = 1
        
    # Change any location for keys
    if key[pygame.K_w]:
        sprite.posInWorld.y -= 5
    if key[pygame.K_s]:
        sprite.posInWorld.y += 5
    if key[pygame.K_a]:
        sprite.posInWorld.x -= 5
    if key[pygame.K_d]:
        sprite.posInWorld.x += 5
    
    Group.update()
    Camera.update()
    Camera.zoomUpdate()
    
    Group.zoomUpdate()
    #Group.camUpdate()
    
    todraw.add(Camera.hit(Group.sprites()))
    #todraw.add(Group.sprites())
    
    
    # Draw sprites
    todraw.draw(Screen.Display)
    
    pygame.display.flip()

pygame.quit()