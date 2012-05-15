#!/usr/bin/env python
"""
This is pygame's chimp.py example ported to PyGL3Display.

Original attempt by Jason M. Marshall, bugfixed by David Griffin.
Also the conversation around this either convinced or inspired David to
make the GL3PGStyleSprite class, for people more at ease with Pygames way
of setting attributes.

License for this file is GPL v2, as it is based on Pygames chimp.py
example. """


#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import PyGL3Display
import math

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = PyGL3Display.PyGL3Display_2dSprites.GL3PygameSurface.GL3Load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


#classes for our game objects
class Fist(PyGL3Display.PyGL3Display_2dSprites.GL3PGStyleSprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        image, self.rect = load_image('fist.bmp', -1)
        self.punching = 0
        PyGL3Display.PyGL3Display_2dSprites.GL3PGStyleSprite.__init__(self, image=image, layer=2)
        self.origin = (0.0, 0.0)

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)
        self.position = self.rect.topleft

    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0


class Chimp(PyGL3Display.PyGL3Display_2dSprites.GL3PGStyleSprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        image, self.rect = load_image('chimp.bmp', -1)
        self.area = pygame.Rect(0, 0, 640, 480)
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0
        PyGL3Display.PyGL3Display_2dSprites.GL3PGStyleSprite.__init__(self, image=image, layer=1)

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.flipx = not self.flipx
        self.rect = newpos
        self.position = self.rect.center

    def _spin(self):
        "spin the monkey image"
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.rotation = 0.0
        else:
            self.rotation = math.radians(self.dizzy)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1

class Background(PyGL3Display.PyGL3Display_2dSprites.GL3PGStyleSprite):
    """There's probably a better way to show a background than this"""
    def __init__(self):
        image = PyGL3Display.PyGL3Display_2dSprites.GL3PygameSurface((468, 60))
        image.fill((250, 250, 250))
        
        #Put Text On The Background, Centered
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
            textpos = text.get_rect(centerx=image.get_width() // 2)
            image.blit(text, textpos)

        PyGL3Display.PyGL3Display_2dSprites.GL3PGStyleSprite.__init__(self, image=image, layer=0, origin=(0,0))

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    PyGL3Display.GL3Common.initEnvironment((468, 60))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(0)

#Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    background = Background()
    chimp = Chimp()
    fist = Fist()

#Main Loop
    going = True
    while going:
        clock.tick(60)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play() #punch
                    chimp.punched()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

#        background.update()
        chimp.update()
        fist.update()

        #Draw Everything
        PyGL3Display.GL3Common.doTasks()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
