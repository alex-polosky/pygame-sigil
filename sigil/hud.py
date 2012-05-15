import re as _re
import sys as _sys

from pygame.locals import *

from locals import *
from locals import _funny, _pygame, _os

CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
WHITESPACE = ' \t\r\n'
TAB = " " * 4
ENTERC = K_BACKQUOTE
HISTORY = 10 # Amount of allowed remembered lines
REPEAT = 60 # Amount of frames before repeat starts
RATE = 10 # Rate of repeat
CURSOR = "]"

_TEMP = 0

class StrBuffer(list):

    _pos = 0
    _lastBuf = ''
    #_ins = 0

    def __init__(self, s=""):
        list.__init__(self)

        for x in s:
            self.addCharacter(x)

    def clear(self):
        r = range(0, len(self))
        r.reverse()
        for x in r:
            self.__delitem__(x)
        self._pos = 0

    def flush(self):
        a = self.getStr()
        self._lastBuf = a.strip('\n')
        self.clear()
        return a
    
    def getStr(self, cursorOn=0, cursor="_"):
        if cursorOn:
            a = []
            for x in self:
                a.append(x)
            a.insert(self._pos, cursor)
            return ''.join(a).replace('\t', TAB)
        if not cursorOn:
            return ''.join(self).replace('\t', TAB)
    
    def addCharacter(self, c):
        if ((c in CHARS) or (c in WHITESPACE)):
            self.insert(self._pos, c)
            self._pos += 1

    def addBackspace(self):
        if (self._pos > 0):
            self.pop(self._pos-1)
            self._pos -= 1

    def addDelete(self):
        if (self._pos < len(self)):
            self.pop(self._pos)

    def shiftHome(self):
        self._pos = 0

    def shiftEnd(self):
        self._pos = len(self)

    def shiftLeft(self):
        if (self._pos > 0):
            self._pos -= 1

    def shiftRight(self):
        if (self._pos < len(self)):
            self._pos += 1

class Console():
    
    active = False
    history = [""]
    historyPos = 0
    lastKey = None
    
    def __init__(self, screen=None, height=.3, bg=None):
        self.buff = StrBuffer()
        self.screen = screen
        if (screen == None):
            if not _pygame.display.get_init():
                raise _pygame.error("Display not initialized.")
            self.screen = _pygame.display.get_surface()
        self.rect = self.screen.get_size()
        self.rect = (0, 0, self.rect[0], int(round(self.rect[1]*height)))
        self.bg = bg
    
    def activate(self, a=None):
        if (a == None):
            self.active = not self.active
        else:
            self.active = a
        if (self.active):
            _sys.stdout.write(CURSOR + " ")
            self._temp = self.screen.copy()
            t = _pygame.Surface((800, 200))
            t.fill((255, 255, 255))
            self.screen.blit(t, (0, 0), self.rect)
        if not self.active:
            if (self.bg):
                self.screen.blit(self.bg, (0, 0), self.rect)
            self.screen.blit(self._temp, (0, 0,), self.rect)
            self._temp = None

    def processInput(self, query):
        # Add query to list of history
        self.history.append(query.split('\n')[-1])
        # If history exceeds allowed rememebered lines, del them
        while (len(self.history) > HISTORY):
            self.history.__delitem__(0)
        self.historyPos = 0
        # Lastly, actually use the input
        # For now, just show a new line
        self.out = ""
        #print self.history[-1]
    
    def getInput(self):
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                _sys.exit()
            if (event.type == _pygame.KEYDOWN):
                self.lastKey = event
                
                # Exit Console
                if (
                    (
                        (event.key == ENTERC)
                        and
                        (event.mod == ENTERC_MOD)
                    )
                    or
                    (event.key == K_ESCAPE)
                ):
                    print ("Console deactivated\n")
                    self.buff.clear()
                    self.activate()
                
                # Adding actual characeters
                #if (
                #      (event.unicode in CHARS)
                #      or
                #      (event.unicode in WHITESPACE)
                #):
                if (
                    (event.key in range(32, 127))
                ):
                    self.buff.addCharacter(event.unicode)

                # Adding deletion
                if (event.key == K_BACKSPACE):
                    self.buff.addBackspace()
                if (event.key == K_DELETE):
                    self.buff.addDelete()

                # Shifting around
                if (event.key == K_LEFT):
                    self.buff.shiftLeft()
                if (event.key == K_RIGHT):
                    self.buff.shiftRight()
                if (event.key == K_HOME):
                    self.buff.shiftHome()
                if (event.key == K_END):
                    self.buff.shiftEnd()

                # Use history
                if (event.key == K_UP):
                    if (
                        (abs(self.historyPos) < HISTORY)
                       ):
                        self.buff.clear()
                        self.historyPos -= 1
                        try:
                            for x in self.history[self.historyPos]:
                                self.buff.addCharacter(x)
                            self.buff.shiftEnd()
                        except:
                            self.historyPos += 2
                if (event.key == K_DOWN):
                    if (self.historyPos < 0):
                        self.buff.clear()
                        self.historyPos += 1
                        for x in self.history[self.historyPos]:
                            self.buff.addCharacter(x)
                        self.buff.shiftEnd()

                # Submit/add line
                if (event.key == K_RETURN):
                    self.buff.shiftEnd()
                    self.buff.addCharacter("\n")
                    self.processInput(self.buff.flush())

    def draw(self):
        # This is the GUI [pygame] part
        pass
    
    def consoleDraw(self):        
        # This is the textual console part (ie print)
        if (self.lastKey == None): return
        elif (self.lastKey.key == K_RETURN):
            _sys.stdout.write('\b'*(len(self.buff._lastBuf)+1))
            _sys.stdout.write('\x00'*(len(self.buff._lastBuf)+1))
            _sys.stdout.write('\b'*(len(self.buff._lastBuf)+1))
            _sys.stdout.write(self.buff._lastBuf+"\n")
            #print(self.buff._lastBuf.__repr__())
            print(self.out)
            _sys.stdout.write(CURSOR + " ")
            self.lastKey = None
        elif (
            (self.lastKey.key == K_BACKSPACE)
            or
            (self.lastKey.key == K_DELETE)
        ):
            _sys.stdout.write('\b'*(len(self.buff.getStr(1))+1))
            _sys.stdout.write('\x00'*(len(self.buff.getStr(1))+1))
            _sys.stdout.write('\b'*(len(self.buff.getStr(1))+1))
            _sys.stdout.write(self.buff.getStr(1))
        else:
            _sys.stdout.write('\b'*(len(self.buff.getStr(1))-0))
            _sys.stdout.write('\x00'*(len(self.buff.getStr(1))-0))
            _sys.stdout.write('\b'*(len(self.buff.getStr(1))-0))
            _sys.stdout.write(self.buff.getStr(1))
            #_sys.stdout.write(str(self.buff._pos))
    
    def update(self):
        if self.active:
            self.getInput()
            self.draw()
            self.consoleDraw()

class Hud():
    pass
