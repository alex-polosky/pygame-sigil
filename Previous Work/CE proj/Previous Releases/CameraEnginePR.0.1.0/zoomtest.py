#!/usr/bin/env python
import pygame
import random

import CameraEngine

WIDTH = 800
HEIGHT = 600
SCALE = .1

Screen = CameraEngine.screen.Screen((WIDTH, HEIGHT), "Zoom Test")

Camera = CameraEngine.screen.ZoomCamera(
    0, 0, WIDTH-200, HEIGHT,
    -1000, 1000, -1000, 1000,
    SCALE
)

Group = CameraEngine.sprite.ZoomGroup()

image = pygame.Surface((10, 10))
pygame.draw.rect(image,
                 (255, 255, 255),
                 (0, 0, 10, 10))

bg = pygame.Surface((WIDTH, HEIGHT))
bg.fill((0, 0, 0))
Screen.Display.blit(bg, (0, 0, WIDTH, HEIGHT))

sprite = CameraEngine.sprite.ZoomSprite(
    pygame.rect.Rect(WIDTH/2-10, HEIGHT/2-10, 10, 10),
    image,
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

Clock = pygame.time.Clock()

while True:
    
    Clock.tick(40)
    
    # Clear sprites
    Group.clear(Screen.Display, bg)
    
    # Get input, update sprites
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            break
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (event.button == 4):
                #sprite.zoom += sprite.zoomScale
                Group.setGroupAttr('changeZoom', 1)
            if (event.button == 5):
                #sprite.zoom -= sprite.zoomScale
                Group.setGroupAttr('changeZoom', -1)
    key = pygame.key.get_pressed()
    
    if key[pygame.K_LEFT]:
        Camera.MOVE_X = -1
    if key[pygame.K_RIGHT]:
        Camera.MOVE_X = 1
    if key[pygame.K_UP]:
        Camera.MOVE_Y = -1
    if key[pygame.K_DOWN]:
        Camera.MOVE_Y = 1
    
    Group.update()
    Camera.update()
    Camera.zoomUpdate()
    
    Group.zoomUpdate()
    #Group.camUpdate()
    
    
    # Draw sprites
    Group.draw(Screen.Display)
    
    pygame.display.flip()

pygame.quit()