# Here is where we define if we're playing:
# top-down;
# scrolling;
# platforms;
# gravity?

###########
# We also need to implement loading of map
# files here
# IDEA
# For tiles, in the map, we have two seperate things for each
# world, so it'd be like this:
# image=[00000000000000000,
#        11111111111111111]
# collide=[00000000000000000,
#          11111111111111111]
# where image 0 = no image; image 1 = tile 1
# collide 0 = no collision; collide 1 = block sprites from entering
# collide 2 = sprite death

from locals import *
from locals import _pygame, _os, _stderr
#from parsing import Parser, Map

#### HOW A LOOP MIGHT WORK
allkeys = 'BACKSPACE,TAB,CLEAR,RETURN,PAUSE,ESCAPE,' +\
          'SPACE,EXCLAIM,QUOTEDBL,HASH,DOLLAR,AMPERSAND,' +\
          'QUOTE,LEFTPAREN,RIGHTPAREN,ASTERISK,PLUS,' +\
          'COMMA,MINUS,PERIOD,SLASH,0,1,2,3,4,5,6,7,8,9,' +\
          'COLON,SEMICOLON,LESS,EQUALS,GREATER,QUESTION,' +\
          'AT,LEFTBRACKET,BACKSLASH,RIGHTBRACKET,CARET,' +\
          'UNDERSCORE,BACKQUOTE,a,b,c,d,e,f,g,h,i,j,k,l,' +\
          'm,n,o,p,q,r,s,t,u,v,w,x,y,z,DELETE,KP0,KP1,KP2,' +\
          'KP3,KP4,KP5,KP6,KP7,KP8,KP9,KP_PERIOD,' +\
          'KP_DIVIDE,KP_MULTIPLY,KP_MINUS,KP_PLUS,' +\
          'KP_ENTER,KP_EQUALS,UP,DOWN,RIGHT,LEFT,' +\
          'INSERT,HOME,END,PAGEUP,PAGEDOWN,' +\
          'F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12,F13,F14,F15,' +\
          'NUMLOCK,CAPSLOCK,SCROLLOCK,RSHIFT,LSHIFT,RCTRL,LCTRL,' +\
          'RALT,LALT,RMETA,LMETA,LSUPER,RSUPER,MODE,HELP,' +\
          'PRINT,SYSREQ,BREAK,MENU,POWER,EURO'


class KeyManager():
    
    keys = allkeys.split(',')
    kevents = allkeys.split(',')
    mevents = [int(x) for x in '1,2,3,4,5,6'.split(',')]
    
    def event_QUIT(self):
        pass
    
    def queueGet(self, events=None, key=None):
        # Get the event queue and the key pressed
        if (events == None):
            events = _pygame.event.get()
        
        if (key == None):
            key = _pygame.key.get_pressed()
        
        # Manage the event queue
        for event in events:
            if (event.type == _pygame.QUIT):
                self.event_QUIT()
            
            if (event.type == _pygame.KEYDOWN):
                #print("KEYDOWN")
                for x in self.kevents:
                    if (
                        (event.key == eval('_pygame.K_'+x))
                        and
                        (hasattr(self, 'event_' +x+ '_down'))
                    ):
                        exec('self.event_' +x+ '_down()')
            
            if (event.type == _pygame.KEYUP):
                #print("KEYUP")
                for x in self.kevents:
                    if (
                        (event.key == eval('_pygame.K_'+x))
                        and
                        (hasattr(self, 'event_' +x+ '_up'))
                    ):
                        exec('self.event_' +x+ '_up()')
            
            if (event.type == _pygame.MOUSEBUTTONDOWN):
                #print("MOUSEBUTTONDOWN")
                for x in self.mevents:
                    if (
                        (event.button == x)
                        and
                        (hasattr(self, 'event_m' +str(x)+ '_down'))
                    ):
                        exec('self.event_m' +str(x)+ '_down()')
            
            if (event.type == _pygame.MOUSEBUTTONUP):
                #print("MOUSEBUTTONUP")
                for x in self.mevents:
                    if (
                        (event.button == x)
                        and
                        (hasattr(self, 'event_m' +str(x)+ '_up'))
                    ):
                        exec('self.event_m' +str(x)+ '_up()')
        
        # Manage the key press
        for x in self.keys:
            if (eval('key[_pygame.K_'+x+']')):
                if (hasattr(self, 'key_' +x+ '_pressed')):
                    exec('self.key_' +x+ '_pressed()')
    
    def eventGet(self, event=None):
        if (event == None):
            events = _pygame.event.get()
        
        for event in events:
            if (event.type == _pygame.QUIT):
                self.event_QUIT()
            
            if (event.type == _pygame.KEYDOWN):
                #print("KEYDOWN")
                for x in self.kevents:
                    if (
                        (event.key == eval('_pygame.K_'+x))
                        and
                        (hasattr(self, 'event_' +x+ '_down'))
                    ):
                        exec('self.event_' +x+ '_down()')
            
            if (event.type == _pygame.KEYUP):
                #print("KEYUP")
                for x in self.kevents:
                    if (
                        (event.key == eval('_pygame.K_'+x))
                        and
                        (hasattr(self, 'event_' +x+ '_up'))
                    ):
                        exec('self.event_' +x+ '_up()')
            
            if (event.type == _pygame.MOUSEBUTTONDOWN):
                #print("MOUSEBUTTONDOWN")
                for x in self.mevents:
                    if (
                        (event.button == x)
                        and
                        (hasattr(self, 'event_m' +str(x)+ '_down'))
                    ):
                        exec('self.event_m' +str(x)+ '_down()')
            
            if (event.type == _pygame.MOUSEBUTTONUP):
                #print("MOUSEBUTTONUP")
                for x in self.mevents:
                    if (
                        (event.button == x)
                        and
                        (hasattr(self, 'event_m' +str(x)+ '_up'))
                    ):
                        exec('self.event_m' +str(x)+ '_up()')
    
    def keyGet(self, key=None):
        if (key == None):
            key = _pygame.key.get_pressed()
        for x in self.keys:
            if (eval('key[_pygame.K_'+x+']')):
                if (hasattr(self, 'key_' +x+ '_pressed')):
                    exec('self.key_' +x+ '_pressed()')



class BaseWorld(KeyManager):
    
    def __init__(self,
                 screen,
                 sprites,
                 background,
                 frameCap=40,
                 clock=None,
                 ):
        self.screen = screen
        self.sprites = sprites
        self.background = background
        if (clock == None):
            clock = _pygame.time.Clock()
        self.clock = clock
        self.frameCap = frameCap
        self.FPS = 0
        self.running = 0
        self.paused = 0
    
    def event_QUIT(self):
        self.running = 0
    
    def tick(self):
        self.clock.tick(self.frameCap)
        self.FPS = self.clock.get_fps()
    
    def clearSprites(self):
        self.sprites.clear(self.screen.Display, self.background)
    
    def drawSprites(self):
        r = self.sprites.draw(self.screen.Display)
        _pygame.display.update(r)
    
    def update(self):
        self.sprites.update()
    
    def preLoop(self):
        _pygame.display.flip()
    
    def preIter(self):
        pass
    
    def postIter(self):
        pass
    
    def postLoop(self):
        _pygame.quit()
    
    def run(self):        
        self.preLoop()
        
        self.running = 1
        while self.running:
            self.preIter()
            
            self.tick()
            
            self.clearSprites()
            
            self.queueGet()
            
            self.update()
            
            self.drawSprites()
            
            self.postIter()
        
        self.postLoop()
    
class CameraBaseWorld(BaseWorld):
    
    def __init__(self,
                 screen,
                 sprites,
                 drawSprites,
                 background,
                 frameCap,
                 camera,
                 clock=None,
                 topSprites=None,
                 ):
        BaseWorld.__init__(self,
                           screen,
                           sprites,
                           background,
                           frameCap,
                           clock,)
        self.camera = camera
        self.toDraw = drawSprites
        self.topSprites = topSprites
        
    
    def clearSprites(self):
        self.toDraw.clear(self.screen.Display, self.background)
        self.toDraw.empty()
    
    def drawSprites(self):
        r = self.toDraw.draw(self.screen.Display)
        if (self.topSprites != None):
            self.topSprites.draw(self.screen.Display)
        _pygame.display.update(r)

    def update(self):
        self.sprites.update()
        self.camera.update()
        if (hasattr(self.camera, "zoomUpdate")):
            self.camera.zoomUpdate()
        
        self.sprites.camUpdate()
        
        self.toDraw.add(self.camera.hit(self.sprites.sprites()))
