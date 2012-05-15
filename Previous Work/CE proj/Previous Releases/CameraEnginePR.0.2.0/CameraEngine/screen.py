# NOTICE
# screen.Screen is soon to be deprecated.
# I am not completely sure if it should stay or not,
# because I do not want to expose the pygame library
# as much as possible
# This makes it easier to program

import pygame as _pygame
from sys import stderr as _stderr

# The Screen Object contains the main pygame surface,
# as well as the universal camera.

class Screen():
    
    def __init__(self, (WIDTH, HEIGHT), caption, fullscreen=0):
        _pygame.init()
        if (fullscreen == 0):
            self.Display = _pygame.display.set_mode((WIDTH, HEIGHT))
        else:
            self.Display = _pygame.display.set_mode(
                (WIDTH, HEIGHT),
                _pygame.FULLSCREEN
                )
        _pygame.display.set_caption(caption)
        # This is where we set self.Camera = camera class
        #self.Camera = Camera()

# I am leaving in the old Camera class from the previous
# release. It was working fine, no reason to change fully working code

# Try to implement a way to zoom
# Allow the camera to follow someone
# Define the speed of the camera
# Allow switching of cameras - Screen Class
# For debug purposes, allow moving camera
#   to a certain point - Screen Class,
#                       but define if allowed in Camera
# IDEA!:
#  The Camera class should infact be
#  a sprite group class. Perhaps combine
#  with the Tree Idea
# This idea _might_ not work if it has
# to follow a sprite
# Perhaps make two seperate classes?
# OKAY:
# This class cannot be a sprite group
class Camera(_pygame.rect.Rect):
    
    # The Bound attributes define where the
    # camera is allowed to move around to
    BOUND_X_NEG = 0
    _BOUND_X_NEG = 0
    BOUND_X_POS = 0
    _BOUND_X_POS = 0
    BOUND_Y_NEG = 0
    _BOUND_Y_NEG = 0
    BOUND_Y_POS = 0
    _BOUND_Y_POS = 0
    
    # These are the speeds that the camera
    # moves at, not defining if the camera
    # should be moving
    SPEED_X = 0
    _SPEED_X = 0
    SPEED_Y = 0
    _SPEED_Y = 0
    
    # These tell if the camera should move
    # at all, and in which direction
    # If perpetual x or y is 1,
    # then the camera will move in that
    # direction on every update
    # If move x or y is greater than -1 or 1
    # then when moved, the value is added
    # onto speed when the new position is
    # calculated
    MOVE_X = 0
    #_MOVE_X = 0
    PERPETUAL_X = 0
    MOVE_Y = 0
    #_MOVE_Y = 0
    PERPETUAL_Y = 0
    
    # These are just extra attributes
    # Zoomable allows the camera to be
    #  zoomed in and out [duh]
    # Following is an object that the
    #  camera will stay centered on,
    #  regardless of the perpetual and
    #  speed settings
    #  It will however, follow the
    #  bound attributes
    #  Only follows if update() is called
    #  every iteration
    # Customxy allows the camera's x and y
    #  to be changed outside of the class
    # Zoom not functioning yet
    ZOOMABLE = 0
    FOLLOWING = None
    # Not functioning
    # perhaps make _x and _y, and in the
    # update(), set x and y = _x and _y,
    # then do all the updating, and reset
    # _x and _y to x and y. GENIOUS!
    CUSTOMXY = 0
    
    def __init__(self, left, top, width, height,
                       B_x_neg, B_x_pos, B_y_neg, B_y_pos,
                       S_x=10, S_y=10,
                       M_x=0, P_x=0, M_y=0, P_y=0,
                       off_x=0, off_y=0,
                       Follow=None, xy=0):
        _pygame.rect.Rect.__init__(self, left, top, width, height)
        
        self.BOUND_X_NEG = B_x_neg
        self._BOUND_X_NEG = B_x_neg
        self.BOUND_X_POS = B_x_pos
        self._BOUND_X_POS = B_x_pos
        self.BOUND_Y_NEG = B_y_neg
        self._BOUND_Y_NEG = B_y_neg
        self.BOUND_Y_POS = B_y_pos
        self._BOUND_Y_POS = B_y_pos
        
        self.SPEED_X = S_x
        self._SPEED_X = S_x
        self.SPEED_Y = S_y
        self._SPEED_Y = S_y
        
        self.MOVE_X = M_x
        self.PERPETUAL_X = P_x
        self.MOVE_Y = M_y
        self.PERPETUAL_Y = P_y
        
        # off_x and off_y determine where on the screen they occur
        self.offset_x = off_x
        self.offset_y = off_y
        
        if (Follow != None):
            if ((hasattr(Follow, 'posInWorld'))
                ):
                self.FOLLOWING = Follow
            else:
                _stderr.write("Follow object has no attribute x and y\n")
        
        self.CUSTOMXY = xy
        
    def update(self):
        # Move x and y must be reset to 0
        # at the end
        # Change the following code
        
        # Adjust according to the follow object
        if (self.FOLLOWING != None):
            self.centerx = self.FOLLOWING.posInWorld.centerx
            self.centery = self.FOLLOWING.posInWorld.centery
            
        # Otherwise:
        else:
            # Move the x and y axis;
            if (self.MOVE_X == 1):
                self.x += self.SPEED_X
            elif (self.MOVE_X == -1):
                self.x -= self.SPEED_X
            elif (self.MOVE_X != 0):
                self.x += self.MOVE_X
            
            if (self.MOVE_Y == 1):
                self.y += self.SPEED_Y
            elif (self.MOVE_Y == -1):
                self.y -= self.SPEED_Y
            elif (self.MOVE_Y != 0):
                self.y += self.MOVE_Y
            
        # Make sure that the camera stays in bounds:
        if (self.x < self.BOUND_X_NEG):
            self.x = self.BOUND_X_NEG
        if (self.y < self.BOUND_Y_NEG):
            self.y = self.BOUND_Y_NEG
        if (self.x > self.BOUND_X_POS):
            self.x = self.BOUND_X_POS
        if (self.y > self.BOUND_Y_POS):
            self.y = self.BOUND_Y_POS
        
        # Reset the mover only if perpetual is not set
        if (self.PERPETUAL_X == 0):
            self.MOVE_X = 0
        if (self.PERPETUAL_Y == 0):
            self.MOVE_Y = 0
    
    def hit(self, sprites):        
        """Return a list of items that collide with their camera
        """
        hits = []
        for x in sprites:
            if (
                (x.posInWorld.right >= self.left)
                and
                (x.posInWorld.bottom >= self.top)
                and
                (x.posInWorld.left <= self.right)
                and
                (x.posInWorld.top <= self.bottom)
               ):
                hits.append(x)

        return hits
    
    def changeBound(self, x_neg=None, x_pos=None,
                          y_neg=None, y_pos=None):
        '''Change the x or y neg or pos bounds
           Only include ones that are changing'''
        if (x_neg != None):
            self.BOUND_X_NEG = x_neg
            self._BOUND_X_NEG = x_neg
        if (x_pos != None):
            self.BOUND_X_POS = x_pos
            self._BOUND_X_POS = x_pos
        if (y_neg != None):
            self.BOUND_X_NEG = y_neg
            self._BOUND_X_NEG = y_neg
        if (y_pos != None):
            self.BOUND_X_POS = y_pos
            self._BOUND_X_POS = y_pos
        
    def changeBound_tmp(self, x_neg=None, x_pos=None,
                          y_neg=None, y_pos=None):
        '''Assign values to x or y neg or pos
           bounds temporarily.
           If any are set as None, resets that 
           one to _x or _y _neg or _pos'''
        if (x_neg != None):
            self.BOUND_X_NEG = x_neg
        elif (x_neg == None):
            self.BOUND_X_NEG = self._BOUND_X_NEG
        if (x_pos != None):
            self.BOUND_X_POS = x_pos
        elif (x_pos == None):
            self.BOUND_X_POS = self._BOUND_X_POS
        if (y_neg != None):
            self.BOUND_X_NEG = y_neg
        elif (y_neg == None):
            self.BOUND_X_NEG = self._BOUND_X_NEG
        if (y_pos != None):
            self.BOUND_X_POS = y_pos
        elif (y_pos == None):
            self.BOUND_X_POS = self._BOUND_X_POS

    def getBounds(self):
        return self.BOUND_X_NEG, self.BOUND_X_POS, \
               self.BOUND_Y_NEG, self.BOUND_Y_POS
    
    def changeSpeed(self, x=None, y=None):
        if (x != None):
            self.SPEED_X = x
            self._SPEED_X = x
        if (y != None):
            self.SPEED_Y = y
            self._SPEED_Y = y
    
    def changeSpeed_tmp(self, x=None, y=None):
        if (x != None):
            self.SPEED_X = x
        elif (x == None):
            self.SPEED_X = self._SPEED_X
        if (y != None):
            self.SPEED_Y = y
        elif (y == None):
            self.SPEED_Y = self._SPEED_Y
    
    def getSpeed(self):
        return self.SPEED_X, self.SPEED_Y

class ZoomCamera(Camera):
    
    def __init__(self, left, top, width, height,
                       B_x_neg, B_x_pos, B_y_neg, B_y_pos,
                       zoomScale=1.0, zoomLimit=1,
                       S_x=10, S_y=10,
                       M_x=0, P_x=0, M_y=0, P_y=0,
                       off_x=0, off_y=0,
                       Follow=None, xy=0):
        Camera.__init__(
            self,
            left, top, width, height,
            B_x_neg, B_x_pos, B_y_neg, B_y_pos,
            S_x, S_y,
            M_x, P_x, M_y, P_y,
            off_x, off_y,
            Follow, xy
        )
        self.changeZoom = 0
        self.zoom = 1
        self._zoom = 1
        self.zoomLimit = zoomLimit
        self.zoomScale = zoomScale
    
    def hit(self, sprites):        
        """Return a list of items that collide with their camera
        """
        hits = []
        for x in sprites:
            if (
                (x.posCamera.right >= self.offset_x)
                and
                (x.posCamera.bottom >= self.offset_y)
                and
                (x.posCamera.left <= self.w)
                and
                (x.posCamera.top <= self.h)
               ):
                hits.append(x)

        return hits
        
    def update(self):
        # Move x and y must be reset to 0
        # at the end
        # Change the following code
        
        # Adjust according to the follow object
        if (self.FOLLOWING != None):
            self.centerx = self.FOLLOWING.posInWorld.centerx * self.zoom
            self.centery = self.FOLLOWING.posInWorld.centery * self.zoom
            
        # Otherwise:
        else:
            # Move the x and y axis;
            if (self.MOVE_X == 1):
                self.x += self.SPEED_X
            elif (self.MOVE_X == -1):
                self.x -= self.SPEED_X
            elif (self.MOVE_X != 0):
                self.x += self.MOVE_X
            
            if (self.MOVE_Y == 1):
                self.y += self.SPEED_Y
            elif (self.MOVE_Y == -1):
                self.y -= self.SPEED_Y
            elif (self.MOVE_Y != 0):
                self.y += self.MOVE_Y
            
        # Make sure that the camera stays in bounds:
        if (self.x < self.BOUND_X_NEG * self.zoom):
            self.x = self.BOUND_X_NEG * self.zoom
        if (self.y < self.BOUND_Y_NEG * self.zoom):
            self.y = self.BOUND_Y_NEG * self.zoom
        if (self.x > self.BOUND_X_POS * self.zoom):
            self.x = self.BOUND_X_POS * self.zoom
        if (self.y > self.BOUND_Y_POS * self.zoom):
            self.y = self.BOUND_Y_POS * self.zoom
        
        # Reset the mover only if perpetual is not set
        if (self.PERPETUAL_X == 0):
            self.MOVE_X = 0
        if (self.PERPETUAL_Y == 0):
            self.MOVE_Y = 0
    
    def zoomUpdate(self):
        if (self.changeZoom != 0):
            self.zoom += (self.zoomScale * self.changeZoom)
            self.changeZoom = 0
            
            
            if (self.zoom < self.zoomLimit):
                self.zoom = self.zoomLimit
                    
                #self.x = self.x * self.zoom / self._zoom
                #self.y = self.y * self.zoom / self._zoom
                #self.w = self.w * self.zoom / self._zoom
                #self.h = self.h * self.zoom / self._zoom
                
            self._zoom = self.zoom