import sys as _sys
import os as _os
_sys.path.append(_os.path.dirname(__file__))
del _os, _sys

import pygame.rect as rect
Rect = rect.Rect
del rect

import buffer
import hud
import parsing
import screen
import sprite
import tools
import version
import world
from locals import *

# I want to implement a simple HUD class
# Use the HUD class for displaying any
# scores or other important data

# also, perhaps a Particles Engine
