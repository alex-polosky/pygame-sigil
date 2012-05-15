"""
PyGL3Display
(C) David Griffin (2010-present)
"Habilain" is a pseudonym used by David Griffin in a number of places.

A high performance Pygame OpenGL library, capable of handling 1000s of sprites

Requirements: Python, Pygame, PyOpenGL, Open GL 2.0 graphics hardware

Licensed under GPLv2 or GPLv3. You should have received a copy of both of these
licenses in the files GPLv2.txt and GPLv3.txt. If not these licenses can be
found at http://www.gnu.org/licenses/gpl-2.0.html (GPLv2) and
http://www.gnu.org/licenses/gpl-3.0.html (GPLv3). By using this file you agree
to be bound by at least one of these licenses.

Other licenses, including commercial/proprietary licenses, can be arranged by 
contacting me via e-mail at habilain@gmail.com. If you do not have in physical 
writing an alternative license agreement from me, you must use one of the 
licenses specified above when releasing work which makes use of this library.

PyGL3Display_example_text.py

This file provides an example of most of the high performance usage of
PyGL3Display 2d Sprites
"""


import pygame
pygame.init()
from PyGL3Display import *
from pygame.locals import *

class RenderedString(GL3Group):
    """A higher performance version of GL3Group for text strings; speeds up
    setOrigin by storing geometry."""
    def __init__(self, *args, **kwargs):
        """Initialise the RenderedString"""
        if 'geometry' in kwargs:
            self.geometry = kwargs['geometry']
            del kwargs['geometry']
        GL3Group.__init__(self, *args, **kwargs)
        
    def setOrigin(self, *args, **kwargs):
        """Insert the geometry argument before calling GL3Group.setOrigin"""
        kwargs['geometry'] = self.geometry
        GL3Group.setOrigin(self, *args, **kwargs)
    
    
class SpriteFont(object):
    def __init__(self, font, size):
        """Prerender the font"""
        chars  = ' abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM,.'
        chars += '/?!"$%^\\\';&*()-_=+1234567890'
        font = pygame.font.Font(pygame.font.match_font(font), size)
        self.fontmap = {}
        self.height = 0
        for char in chars:
            character = font.render(char, True, (255,255,255,255))
            self.height = max((self.height, character.get_height()))
            self.fontmap[char] = (GL3PygameSurface.GL3Surfaceify(character), 
                                 character.get_width())
        self.spriteBuffer = GL3SpriteBuffer(100)
    
    def makeString(self, string):
        """Creates a GL3Group which renders the string."""
        lines = string.split('\n')
        sprites = []
        ypos = 0
        maxXpos = 0
        for line in lines:
            xpos = 0
            for char in line:
                if char in self.fontmap:
                    if char != ' ':
                        newSprite = self.spriteBuffer.createSprite()
                        newSprite.setImage(self.fontmap[char][0])
                        newSprite.setOrigin((0,0))
                        newSprite.setPosition((xpos, ypos))
                        sprites.append(newSprite)
                    xpos += self.fontmap[char][1]
            maxXpos = max(xpos, maxXpos)
            ypos += self.height
        ret = RenderedString(sprites, geometry=(0, 0, maxXpos, ypos))
        ret.setOrigin((0.0, 0.0))
        return ret
        
        
if __name__ == '__main__':
    class TestApp(object):
        def __init__(self, name):
            self.name = name
            self.screen_resolution = 800, 800
            self.string = ('Things you can do: \n' +
                           ' r: cycle red values \n' +
                           ' g: cycle green values \n' +
                           ' b: cycle blue values \n' +
                           ' arrow keys: move text \n' +
                           ' y: clockwise rotate \n' +
                           ' f: toggle CPU usage limiter ' + 
                           '(technically pointless) \n' +
                           ' asdw: move origin point \n' +
                           ' ijkl: increase / decrease x/y scale\n' +
                           'I\'m afraid that holding keys down won\'t work.\n'+
                           'Also theres a little funky interaction between' + 
                           ' origin points, and everything else, as \n' +
                           ' origin points are really meant to be set once ' + 
                           'and left alone from there on in. \n\n' +
                           'Apologies for the problems with this sample.\n ' + 
                           '      Habilain')
            self.origx, self.origy = (0, 0)
            self.r, self.g, self.b = (255, 255, 255)
            self.posx, self.posy = (0, 0)
            self.scalex, self.scaley = (1, 1)
            self.rotation = 0
            self.limit = True

        def run(self):
            """The main loop is by no means a good main loop. I'd strongly
            recommend ignoring this as a programming style and integrating
            PyGL3Display into your existing programming style."""
            GL3Common.initEnvironment(self.screen_resolution)
            
            z = 0
            frames = 0
            countedTime = 0
            self.font = SpriteFont('dejavu-sans', 20)
            self.text = self.font.makeString(self.string)
            time = pygame.time.Clock()
            
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            return
                        elif event.key == K_r:
                            self.r = (self.r + 10) % 256
                            self.text.setColoration((self.r, self.b, self.g, 255))
                        elif event.key == K_g:
                            self.g = (self.g + 10) % 256
                            self.text.setColoration((self.r, self.b, self.g, 255))
                        elif event.key == K_b:
                            self.b = (self.b + 10) % 256
                            self.text.setColoration((self.r, self.b, self.g, 255))
                        elif event.key == K_DOWN:
                            self.posy += 10
                            self.text.setPosition((self.posx, self.posy))
                        elif event.key == K_UP:
                            self.posy -= 10
                            self.text.setPosition((self.posx, self.posy))
                        elif event.key == K_RIGHT:
                            self.posx += 10
                            self.text.setPosition((self.posx, self.posy))
                        elif event.key == K_LEFT:
                            self.posx -= 10
                            self.text.setPosition((self.posx, self.posy))
                        elif event.key == K_s:
                            self.origy += 0.1
                            self.text.setOrigin((self.origx, self.origy))
                        elif event.key == K_w:
                            self.origy -= 0.1
                            self.text.setOrigin((self.origx, self.origy))
                        elif event.key == K_d:
                            self.origx += 0.1
                            self.text.setOrigin((self.origx, self.origy))
                        elif event.key == K_a:
                            self.origx -= 0.1
                            self.text.setOrigin((self.origx, self.origy))
                        elif event.key == K_y:
                            self.rotation += 0.1
                            self.text.setRotation(self.rotation)
                        elif event.key == K_i:
                            self.scaley -= 0.1
                            self.text.setScaleY(self.scaley)
                        elif event.key == K_k:
                            self.scaley += 0.1
                            self.text.setScaleY(self.scaley)
                        elif event.key == K_j:
                            self.scalex -= 0.1
                            self.text.setScaleX(self.scalex)
                        elif event.key == K_l:
                            self.scalex += 0.1
                            self.text.setScaleX(self.scalex)
                        elif event.key == K_y:
                            self.rotation += 0.1
                            self.text.setRotation(self.rotation)
                        elif event.key == K_f:
                            self.limit = not self.limit
                            frames, countedTime = 0, 0
                            time.tick()
                z += time.tick()
                if z > 500:
                    z -= 500
                    countedTime += 0.5
                    caption = 'torture test pygame (instant) fps ' + \
                              str(round(time.get_fps(), 2)) + ' averaged fps '\
                              + str(round((frames / countedTime), 2)) + \
                              ' limiter ' + ('on' if self.limit else 'off')
                    pygame.display.set_caption(caption)
                GL3Common.doTasks()
                frames += 1
                if self.limit: pygame.time.wait(10)

    demo = TestApp('test')
    demo.run()
