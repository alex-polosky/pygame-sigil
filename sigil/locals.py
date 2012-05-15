import os as _os
import pygame as _pygame
from sys import stderr as _stderr

from pygame.locals import *

WIDTH = 800
HEIGHT = 600
TARGETFPS = 30
CONSOLE = 1
ENTERC = 69
ENTERC_MOD = 4160
#FPS = 0

COLORS = {
    'white':(255, 255, 255),
    'black':(0, 0, 0),
    'red':(255, 0, 0),
    'green':(0, 255, 0),
    'blue':(0, 0, 255),
    'yellow':(255, 255, 0),
    'cyan':(0, 255, 255),
    'magenta':(255, 0, 255),
}

colorPallete = None
# The reason that these are binary, is maybe so I can use multiple
# types on each sprite.
# Like maybe I want it to be a block+pickup.
# I dunno, it might change, might not.
Wall = 0b1
# Maybe floor, as well?
Platform = 0b10
Block = 0b100
Pickup = 0b1000
Kill = 0b10000


# For easter eggs ;D
_funny = 1