import pygame as _pygame

# This module has several loops in a class
# that can be overridden
# Used for the game loop
class Loop():
    
    _debug = 0
    running = 0
    paused = 0
    modKeys = {
        'LEFT_CTRL' : 0,
        'RIGHT_CTRL' : 0,
        'LEFT_SHIFT' : 0,
        'RIGHT_SHIFT' : 0,
        'LEFT_ALT' : 0,
        'RIGHT_ALT' : 0,
        'SUPER' : 0
    }
    #funcs = {}
    
    def __init__(self, screen, clock, sprites):
        self.screen = screen
        self.clock = clock
        self.sprites = sprites
    
    def setCaption(self, caption):
        _pygame.display.set_caption(caption)
    
    def preLoop(self):
        pass
    
    def preIter(self):
        pass
    
    def clockTick(self, frames):
        self.clock.tick(frames)
    
    def eventGet(self):
        for event in _pygame.event.get():
            # Check if user has quit
            if (event.type == _pygame.QUIT):
                self.running = 0
            # Iterate through any pressed down keys ONCE
            elif (event.type == _pygame.KEYDOWN):
                # Quit if user has hit escape
                # On second thought, make it pause
                if (event.key == _pygame.K_ESCAPE):
                    self.pauseLoop()
                # These will check any of the modifier keys
                # and set to 1 for the keyGet function
                if (event.key == _pygame.K_LCTRL):
                    self.modKeys['LEFT_CTRL'] = 1
                if (event.key == _pygame.K_RCTRL):
                    self.modKeys['RIGHT_CTRL'] = 1
                if (event.key == _pygame.K_LSHIFT):
                    self.modKeys['LEFT_SHIFT'] = 1
                if (event.key == _pygame.K_RSHIFT):
                    self.modKeys['RIGHT_SHIFT'] = 1
                if (event.key == _pygame.K_LALT):
                    self.modKeys['LEFT_ALT'] = 1
                if (event.key == _pygame.K_RALT):
                    self.modKeys['RIGHT_ALT'] = 1
                if (
                    (event.key == _pygame.K_LSUPER)
                    or
                    (event.key == _pygame.K_RSUPER)
                    or
                    (event.key == _pygame.K_LMETA)
                    or
                    (event.key == _pygame.K_RMETA)
                   ):
                    self.modKeys['SUPER'] = 1
                    
                
                if (
                    (event.key == _pygame.K_TAB)
                    and
                    (self.modKeys['LEFT_CTRL'])
                    and
                    (self.modKeys['LEFT_SHIFT'])
                   ):
                    self._debug = 1
                    #try:
                    #    exec(raw_input(">> "))
                    #except:
                    #    print("Error")

            # Here is where we check if any modKeys are let go of
            elif (event.type == _pygame.KEYUP):
                if (event.key == _pygame.K_LCTRL):
                    self.modKeys['LEFT_CTRL'] = 0
                if (event.key == _pygame.K_RCTRL):
                    self.modKeys['RIGHT_CTRL'] = 0
                if (event.key == _pygame.K_LSHIFT):
                    self.modKeys['LEFT_SHIFT'] = 0
                if (event.key == _pygame.K_RSHIFT):
                    self.modKeys['RIGHT_SHIFT'] = 0
                if (event.key == _pygame.K_LALT):
                    self.modKeys['LEFT_ALT'] = 0
                if (event.key == _pygame.K_RALT):
                    self.modKeys['RIGHT_ALT'] = 0
                if (
                    (event.key == _pygame.K_LSUPER)
                    or
                    (event.key == _pygame.K_RSUPER)
                    or
                    (event.key == _pygame.K_LMETA)
                    or
                    (event.key == _pygame.K_RMETA)
                   ):
                    self.modKeys['SUPER'] = 0
    
    def eventGetPause(self):
        for event in _pygame.event.get():
            # Check if user has quit
            if (event.type == _pygame.QUIT):
                self.running = 0
                self.paused = 0
            # Iterate through any pressed down keys ONCE
            elif (event.type == _pygame.KEYDOWN):
                # Exit paused loop
                if (event.key == _pygame.K_ESCAPE):
                    self.paused = 0

    def keyGet(self):
        pass
    
    def clearSprites(self, bg):
        self.sprites.clear(self.screen, bg)
    
    def updateSprites(self, sprites):
        sprites.update()
        #sprites.camUpdate()

    def drawSprites(self, sprites):
        r = sprites.draw(self.screen)
        if (r == None):
            _pygame.display.update()
        else:
            _pygame.display.update(r)
    
    def postIter(self):
        pass
    
    def postLoop(self):
        pass
    
    def pauseLoop(self):
        oldCap = _pygame.display.get_caption()[0]
        
        self.setCaption("Paused!")
        
        self.paused = 1
        while self.paused:
            self.eventGetPause()
        
        self.setCaption(oldCap)
        return
    
    def mainLoop(self, framecap, bg):
        # framecap is a num;
        # sprites is a spritegroup
        # Might get rid of sprites
        # and bg
        self.preLoop()
        
        self.running = 1
        while self.running:
            self.preIter()
            
            self.clockTick(framecap)
            
            self.clearSprites(sprites, bg)
            self.updateSprites(sprites)
            self.drawSprites(sprites)
            
            self.eventGet()
            self.keyGet()
            
            self.postIter()
            
        self.postLoop()
    
    #def keyGetExp(self, keys):
    #    key = _pygame.key.get_pressed()
    #    for x in keys:
    #        exec('if (key[pygame.K_%s]): self.funcs["%s"]()' %(x, x))
    #   
    #    return

class CameraLoop(Loop):
    
    def __init__(self, screen, clock, sprites, drawGroup):
        '''Screen is a surface to blit to, sprites is a CamSprite group containing
           all sprites, drawGroup is an empty CamSprite group used to draw'''
        Loop.__init__(self, screen, clock, sprites)
        self.drawGroup = drawGroup
    
    #def

if __name__ == '__main__':
    surface = _pygame.display.set_mode((1, 1))
    class L(Loop):
        def mainLoop(self):
            a = 0
            while 1:
                self.eventGet()
                self.keyGet()
                if a == 10000:
                    a = 0
                    for x in self.modKeys:
                        print "%s: %d" %(x, self.modKeys[x])
                a += 1
    l = L(surface, None, None)
    l.mainLoop()