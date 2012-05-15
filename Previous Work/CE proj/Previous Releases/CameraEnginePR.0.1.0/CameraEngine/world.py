# Here is where we define if we're playing:
# top-down;
# scrolling;
# platforms;
# gravity?
import pygame as _pygame

class BaseWorld():
    
    def __init__(self,
                 screen,
                 sprites,
                 background,
                 clock,
                 frameCap
                 ):
        self.screen = screen
        self.sprites = sprites
        self.background = background
        self.clock = clock
        self.frameCap = frameCap
    
    def tick(self):
        self.clock.tick(self.frameCap)
    
    def clearSprites(self):
        self.sprites.clear(self.screen, self.background)
    
    def drawSprites(self):
        r = self.sprites.draw(self.screen)
        _pygame.display.update(r)
    
    def update(self):
        self.sprites.update()
    
class CameraBaseWorld(BaseWorld):
    
    def __init__(self,
                 screen,
                 sprites,
                 drawSprites,
                 background,
                 clock,
                 frameCap,
                 camera
                 ):
        BaseWorld.__init__(self,
                           screen,
                           sprites,
                           background,
                           clock,
                           frameCap)
        self.camera = camera
        self.toDraw = drawSprites
        
    
    def clearSprites(self):
        self.toDraw.clear(self.screen, self.background)
        self.toDraw.empty()
    
    def drawSprites(self):
        r = self.toDraw.draw(self.screen)
        _pygame.display.update(r)

    def update(self):
        self.camera.update()
        
        self.sprites.update()
        self.sprites.camUpdate()
        
        self.toDraw.add(self.sprites.camCollide())
