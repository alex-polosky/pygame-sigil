# The screen contains the camera
from pygame import rect
from sys import stderr
_rect = rect.Rect
_stderr = stderr
del rect
del stderr

class screen(object):
    
    pass

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
class Camera(_rect):
    
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
                       Zoom=0, Follow=None, xy=0):
        _rect.__init__(self, left, top, width, height)
        
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
        
        self.ZOOMABLE = Zoom
        
        if (Follow != None):
            if ((hasattr(Follow, 'x'))
                 and
                (hasattr(Follow, 'y'))
                ):
                self.FOLLOWING = Follow
            else:
                _stderr.write("Follow object has no attribute x and y\n")
        
        self.CUSTOMXY = xy
        
    def update(self):
        # Move x and y must be reset to 0
        # at the end
        if (self.FOLLOWING != None):
            self.x = self.FOLLOWING.x
            self.y = self.FOLLOWING.y
        else:
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
        #if (self.PERPETUAL_X != 0):
        #    self.MOVE_X = 0
        #if (self.PERPETUAL_Y != 0):
        #    self.MOVE_Y = 0
        self.MOVE_X = 0
        self.MOVE_Y = 0
    
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
        pass
    
    def changeSpeed_tmp(self, x=None, y=None):
        pass
    
