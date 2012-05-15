import os as _os
import pygame as _pygame
from sys import stderr as _stderr

WIDTH = 800
HEIGHT = 600
TARGETFPS = 60
FPS = 0

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
Platform = 1
Block = 2
Pickup = 4
Kill = 8
