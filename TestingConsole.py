import pygame
import sys
import sigil


def loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    console = sigil.hud.Console()

    while True:

        if not console.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    print (event)
                    if event.key == 96 and event.mod == 65:
                        print( "Console Activated")
                        console.activate()

        console.update()

        pygame.display.flip()

loop()
