from locals import *
from locals import _pygame, _os, _stderr, _funny

# This file contains the Buffer class, which gets handed all moving events
# in order to use for collision

class Buffer():
    
    queue = []
    
    def __init__(self, targetFPS):
        print "World clock is set at %d Frames a Second" %(targetFPS)
        self.targetFPS = targetFPS
        #self.delta = 1.0 / targetFPS
        #self._delta = 1.0 / targetFPS
        self.delta = targetFPS / targetFPS
    
    def checkDelta(self, lastFPS):
        #self.delta = 1.0 / lastFPS
        #if (self.delta > self._delta):
        #    self.delta = self._delta
        if (lastFPS) == 0:
            self.delta = self.targetFPS
            return
        self.delta = float(self.targetFPS) / lastFPS
    
#  add function update()
#   - pre-update any items in the queue
#   - check for ANY collisions 
#   - if collision, use old position to change the new pre-update position
#   - if collision and no old position, just push up if floor collide, to the side if wall collide, etc.
#   - set new pos



    def update(self, lastFPS):
        # Run the checkDelta
        self.checkDelta(lastFPS)
        #print self.targetFPS, lastFPS, self.delta
    
        # Set up a temporary old position used for later colliding alg
        for x in self.queue:
            #x[0].__setattr__('tempOldPos', x[0].posInWorld)
            x[0].tempOldPos.x = x[0].posInWorld.x
            x[0].tempOldPos.y = x[0].posInWorld.y
        
        # Advance the sprites wherever it needs to go
        for x in self.queue:
            if hasattr(x[0], 'posInWorld'):
                x[0].posInWorld.__setattr__(
                    x[1],
                    (getattr(x[0].posInWorld, x[1]) + (x[2] * round(self.delta, 2)))
                    )
        
        # Do any collision alg
        collide = []
        for x in self.queue:
            for y in x[0].groups():
                x[0].collideGroup(y)
                #if (x[0].collide == None):
                #    continue
                #else:
                #    if (x[0].collide[0] == Wall):
                #        #print "Collision with wall"
                #        #continue
                #        xv = x[0].tempOldPos.x - x[0].posInWorld.x
                #        yv = x[0].tempOldPos.y - x[0].posInWorld.y
                #        if (xv < 0):
                #            x[0].posInWorld.x = x[0].collide[1].posInWorld.left \
                #                                - x[0].posInWorld.w
                #        if (xv > 0):
                #            x[0].posInWorld.x = x[0].collide[1].posInWorld.right
                #        if (yv < 0):
                #            x[0].posInWorld.y = x[0].collide[1].posInWorld.top \
                #                                - x[0].posInWorld.h
                #        if (yv > 0):
                #            x[0].posInWorld.y = x[0].collide[1].posInWorld.bottom
                #        #print x[0].tempOldPos.x, x[0].posInWorld.x
                #        #x[0].posInWorld.x = 0
            
            x[0].collide = None
            x[0].tempOldPos
        
        #for x in self.queue:
        #    if hasattr(x[0], 'direction'):
        #        x[0].direction = ''
        # 
        self.queue = []
        
        