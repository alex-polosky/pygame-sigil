##########################################
##########################################
# I need to implement a collision test thingy 
# I've looked into hitmasks, that is the most likely
# one that i'm going to use; 
# include ability to use RECT or CIRCLE collision
# As of right now, everything is hitmask collision
#
# Implement as a group function
#
# Also include a collisionType attr;
# ###Always calls self.onCollide() on collision###
# None; Nothing happens on collision
# Platform; Used to block a sprite from moving past;
#         ;  Does not kill
# Block; Blocks sprite; becomes something else after
#      ; collision
# Pickup; Does not block sprite; does something special
# Kill; Kills sprite if collides
#
#
#
#
#
#
#
#
#
#
#
#
##########################################
##########################################

from locals import *
from locals import _pygame, _os, _stderr

def _pixelPerfectCollisionDetection(sp1,sp2):
    """
    Internal method used for pixel perfect collision detection.
    """
    rect1 = sp1.rect;     
    rect2 = sp2.rect;                            
    rect  = rect1.clip(rect2)
                    
    hm1 = sp1.hitmask
    hm2 = sp2.hitmask
            
    x1 = rect.x-rect1.x
    y1 = rect.y-rect1.y
    x2 = rect.x-rect2.x
    y2 = rect.y-rect2.y

    for r in range(0,rect.height):      
        for c in range(0,rect.width):
            #if hm1[c+x1][r+y1] | hm2[c+x2][r+y2]:
            #    return 1
            if ((hm1[c+x1][r+y1] > 0) and (hm2[c+x2][r+y2] > 0)):
                return 1

    return 0

class Group(_pygame.sprite.RenderUpdates):
    
    def setGroupAttrs(self, attrs, method='='):
        ''' '''
        for s in self.sprites():
            if (method == '='):
                for attr in attrs:
                    s.__setattr__(attr, attrs[attrs])
            elif (method == '+'):
                for attr in attrs:
                    a = s.__getattribute__(attr)
                    a += attrs[attr]
                    s.__setattr__(attr, a)
            elif (method == '-'):
                for attr in attrs:
                    a = s.__getattribute__(attr)
                    a -= attrs[attr]
                    s.__setattr__(attr, a)
            elif (method == '*'):
                for attr in attrs:
                    a = s.__getattribute__(attr)
                    a *= attrs[attr]
                    s.__setattr__(attr, a)
            elif (method == '/'):
                for attr in attrs:
                    a = s.__getattribute__(attr)
                    a /= attrs[attr]
                    s.__setattr__(attr, a)
    
    def setGroupAttr(self, attr, value, method='='):
        ''' '''
        for x in self.sprites():
            if (method == '='):
                x.__setattr__(attr, value)
            elif (method == '+'):
                a = x.__getattribute__(attr)
                a += value
                x.__setattr__(attr, a)
            elif (method == '-'):
                a = x.__getattribute__(attr)
                a -= value
                x.__setattr__(attr, a)
            elif (method == '*'):
                a = x.__getattribute__(attr)
                a *= value
                x.__setattr__(attr, a)
            elif (method == '/'):
                a = x.__getattribute__(attr)
                a /= value
                x.__setattr__(attr, a)
    
    def collideGroup(self, group):
        ppcollide = _pixelPerfectCollisionDetection
        for s1 in self.sprites():
            spritecollide = s1.rect.colliderect
            for s2 in group.sprites():
                if (s1 == s2):
                    pass
                else:
                    if (spritecollide(s2)):
                        if (ppcollide(s1, s2)):
                            s2.onCollide(s1)
    
    def collideSprite(self, sprite):
        #collide = []
        spritecollide = sprite.rect.colliderect
        ppcollide = _pixelPerfectCollisionDetection
        for s in self.sprites():
            if (sprite == s):
                pass
            else:
                if spritecollide(s.rect):
                    if ppcollide(s, sprite):
                        sprite.onCollide(s)
    
    def __init__(self, *sprites):
        _pygame.sprite.RenderUpdates.__init__(self, sprites)

class Sprite(_pygame.sprite.Sprite):
    
    def __init__(self,
                 worldRect,
                 image,
                 collisionType=None,
                 collisionMask='black',
                 attr={},
                 ):
        _pygame.sprite.Sprite.__init__(self)
        self.rect = worldRect
        self.posInWorld = _pygame.rect.Rect \
                    (worldRect.x, worldRect.y,
                     worldRect.w, worldRect.h)
        self.image = image.copy()
        self.collisionType = collisionType
        
        # Deal with the collision mask here
        # can be: string saying alpha,
        # a tuple representing a color key,
        # or an actual 2d array representing the mask
        # It can also be a string saying black
        # this will cause it to just use pixels2darray
        if (collisionMask == 'alpha'):
            self.hitmask = _pygame.surfarray.pixels_alpha(image)
        if (collisionMask == 'black'):
            self.hitmask = _pygame.surfarray.pixels2d(image)
        
        for x in attr:
            self.__setattr__(x, attr[x])
        
        self.direction = None
    
    def update(self):
        pass
    
    def collideGroup(self, group):
        #collide = []
        spritecollide = self.rect.colliderect
        ppcolide = _pixelPerfectCollisionDetection
        for s in group.sprites():
            if (s == self):
                pass
            else:
                if spritecollide(s.rect):
                    if ppcolide(self, s):
                        self.onCollide(s)
    
    def onCollide(self, sprite):
        if (sprite.collisionType == None):
            pass
        elif (sprite.collisionType == Platform):
            if (self.posInWorld.right > sprite.posInWorld.x):
                if (self.direction == 'right'):
                    self.posInWorld.right = sprite.posInWorld.x
                elif (self.direction == 'left'):
                    self.posInWorld.x = sprite.posInWorld.right
                elif (self.direction == 'up'):
                    pass
                elif (self.direction == 'down'):
                    pass
                
            if (self.posInWorld.right < sprite.posInWorld.x):
                if (self.direction == 'right'):
                    self.posInWorld.right = sprite.posInWorld.x
                elif (self.direction == 'left'):
                    self.posInWorld.x = sprite.posInWorld.right
                elif (self.direction == 'up'):
                    pass
                elif (self.direction == 'down'):
                    pass
                
            if (self.posInWorld.y < sprite.posInWorld.bottom):
                if (self.direction == 'right'):
                    pass
                elif (self.direction == 'left'):
                    pass
                elif (self.direction == 'up'):
                    self.posInWorld.y = sprite.posInWorld.bottom
                elif (self.direction == 'down'):
                    self.posInWorld.bottom = sprite.posInWorld.y
                
            if (self.posInWorld.y > sprite.posInWorld.bottom):
                if (self.direction == 'right'):
                    pass
                elif (self.direction == 'left'):
                    pass
                elif (self.direction == 'up'):
                    self.posInWorld.y = sprite.posInWorld.bottom
                elif (self.direction == 'down'):
                    self.posInWorld.bottom = sprite.posInWorld.y
            
        elif (sprite.collisionType == Block):
            pass
        elif (sprite.collisionType == Kill):
            pass
    
    def _OLDonCollide(self, sprite):
        if (sprite.collisionType == None):
            pass
        elif (sprite.collisionType == Platform):
            # Find out where exactly the sprite is inside the colliding
            # sprite. Eventually, once gravity is included,
            # the sprite will be pushed away by the amount of force
            # For now, it is just pushed to be just touching the
            # offending sprite
            if (self.direction == 'right'):
                if (self.posInWorld.right > sprite.posInWorld.x):
                    self.posInWorld.right = sprite.posInWorld.x
            if (self.direction == 'left'):
                if (self.posInWorld.x < sprite.posInWorld.right):
                    self.posInWorld.x = sprite.posInWorld.right
            if (self.direction == 'up'):
                if (self.posInWorld.y < sprite.posInWorld.bottom):
                    self.posInWorld.y = sprite.posInWorld.bottom
            if (self.direction == 'down'):
                if (self.posInWorld.bottom > sprite.posInWorld.y):
                    self.posInWorld.bottom = sprite.posInWorld.y
        elif (sprite.collisionType == Block):
            pass
        elif (sprite.collisionType == Pickup):
            pass
        elif (sprite.collisionType == Kill):
            self.onKill()
    
    def onKill(self):
        self.kill()

class GameObject(Sprite):
    
    '''
    Mainly for game logic. Has no real image
    Only call .update() in the loop;
    Used in order to update any extra things
    in the world
    '''
    
    def __init__(self,
                 pos=(-10000000, -10000000),
                 attr={},
                 ):
        Sprite.__init__(self, [pos[0], pos[1], 0, 0], None, attr)
    
    def update(self):
        pass

class CamGroup(Group):
    
    def __init__(self, *sprites):
        Group.__init__(self, sprites)
    
    # This function is ripped off of the sprite.RenderUpdates
    # function. But I make it so that way it only draws the
    # sprites that are in the cam
    def draw(self, surface):
       spritedict = self.spritedict
       surface_blit = surface.blit
       dirty = self.lostsprites
       self.lostsprites = []
       dirty_append = dirty.append
       for s in self.sprites():
           r = spritedict[s]
           newrect = surface_blit(s.image, s.rect)
           if r is 0:
               dirty_append(newrect)
           else:
               if newrect.colliderect(r):
                   dirty_append(newrect.union(r))
               else:
                   dirty_append(newrect)
                   dirty_append(r)
           spritedict[s] = newrect
       return dirty
    
    def camCollide(self):
        pass
    
    def camUpdate(self):
        for x in self.sprites():
            if not hasattr(x, 'camUpdate'):
                x.posCamera.x = x.posInWorld.x - x.camera.x
                x.posCamera.y = x.posInWorld.y - x.camera.y
                x.rect.x = x.posCamera.x
                x.rect.y = x.posCamera.y
            else:
                x.camUpdate()

class CamSprite(Sprite):
    
    def __init__(self,
                 worldRect,
                 image,
                 camera,
                 collisionType=None,
                 collisionMask='black',
                 attr={}
                 ):
        Sprite.__init__(self,
                        worldRect,
                        image,
                        collisionType,
                        collisionMask,
                        attr)
        
        self.camera = camera
        
        self.posCamera = _pygame.rect.Rect \
                    (worldRect.x, worldRect.y,
                     worldRect.w, worldRect.h)

class ZoomGroup(CamGroup):
    
    # This function is ripped off of the sprite.RenderUpdates
    # function. But I make it so that way it only draws the
    # sprites that are in the cam
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for s in self.sprites():
            # modify the image
            s.image = _pygame.transform.scale(
                s._image,
                (
                    s.posCamera.w,
                    s.posCamera.h
                )
            )
            #s.hitmask = _pygame.surfarray.pixels2d(_pygame.transform.scale(
            #    s._hitmask,
            #    (
            #        s.posCamera.w,
            #        s.posCamera.h
            #    )
            #))
           #
            r = spritedict[s]
            
            # Limit the s.rect x and y in the camera
            nrect = _pygame.rect.Rect(
                0, 0, s.posCamera.w, s.posCamera.h
            )
            if (s.posCamera.right > s.camera.width):
                nrect.w = s.camera.w - nrect.x
            if (s.posCamera.bottom > s.camera.height):
                nrect.h = s.camera.h - nrect.y
            
            #if (s.posCamera.x < s.camera.offset_x):
            #    nrect.x = abs(nrect.x)
            #if (s.posCamera.y < s.camera.offset_y):
            #    nrect.y = abs(nrect.y)
           
            newrect = surface_blit(s.image, s.rect, nrect)
            if r is 0:
                dirty_append(newrect)
            else:
                if newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                else:
                    dirty_append(newrect)
                    dirty_append(r)
            spritedict[s] = newrect
        return dirty

    def camUpdate(self):
        for x in self.sprites():
            if not hasattr(x, 'zoomUpdate'):
                x.hitmask = _pygame.surfarray.array2d(x.image)
                
                x.posCamera.w = x.posInWorld.w * x.camera.zoom
                x.posCamera.h = x.posInWorld.h * x.camera.zoom
                
                x.posCamera.x = (x.posInWorld.x * x.camera.zoom) - x.camera.x
                x.posCamera.y = (x.posInWorld.y * x.camera.zoom) - x.camera.y
            
                x.rect.x = x.posCamera.x
                x.rect.y = x.posCamera.y
            else:
                x.zoomUpdate()

class ZoomSprite(CamSprite):
    
    def __init__(
        self,
        worldRect,
        image,
        camera,
        collisionType=None,
        collisionMask='black',
        attr={}
    ):
        CamSprite.__init__(
            self,
            worldRect,
            image,
            camera,
            collisionType,
            collisionMask,
            attr
        )
        
        self._image = image
        #self._hitmask = _pygame.surfarray.make_surface(self.hitmask)
        #self.hitmasked = _pygame.surfarray.make_surface(self.hitmask)
        #self._hitmask = _pygame.surfarray.make_surface(self.hitmask)