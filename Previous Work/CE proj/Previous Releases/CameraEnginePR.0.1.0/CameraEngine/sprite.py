import pygame as _pygame

class Group(_pygame.sprite.RenderUpdates):
    
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
    
    def __init__(self, *sprites):
        _pygame.sprite.RenderUpdates.__init__(self, sprites)

class Sprite(_pygame.sprite.Sprite):
    
    def __init__(self,
                 worldRect,
                 image,
                 attr={},
                 ):
        _pygame.sprite.Sprite.__init__(self)
        self.rect = worldRect
        self.posInWorld = _pygame.rect.Rect \
                    (worldRect.x, worldRect.y,
                     worldRect.w, worldRect.h)
        self.image = image
        for x in attr:
            self.__setattr__(x, attr[x])
    
    def update(self):
        pass

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
                 attr={}
                 ):
        Sprite.__init__(self,
                        worldRect,
                        image,
                        attr)
        
        self.camera = camera
        
        self.posCamera = _pygame.rect.Rect \
                    (worldRect.x, worldRect.y,
                     worldRect.w, worldRect.h)

class ZoomGroup(CamGroup):
    
    def camUpdate(self):
        pass

    def zoomUpdate(self):
        for x in self.sprites():
            if not hasattr(x, 'zoomUpdate'):
                if (x.changeZoom == 1):
                    x.zoom += x.zoomScale
                elif (x.changeZoom == -1):
                    x.zoom -= x.zoomScale
                x.changeZoom = 0
                    
                if (x.zoom < x.zoomLimit):
                    x.zoom = x.zoomLimit
               
                xP = float(x.posCamera.x)
                yP = float(x.posCamera.y)
                
                x.posCamera.w = x.posInWorld.w * x.zoom
                x.posCamera.h = x.posInWorld.h * x.zoom
                
                x.posCamera.x = (x.posInWorld.x - x.camera.x) * x.zoom 
                x.posCamera.y = (x.posInWorld.y - x.camera.y) * x.zoom
                
                x.image = _pygame.transform.scale(
                    x._image,
                    (
                        x.posCamera.w,
                        x.posCamera.h
                    )
                )
                
                x._zoom = x.zoom
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
        zoomScale=1.0,
        zoomLimit=1,
        attr={}
    ):
        CamSprite.__init__(
            self,
            worldRect,
            image,
            camera,
            attr
        )
        
        self._image = image
        
        self.zoom = 1
        self._zoom = 1
        self.zoomLimit = zoomLimit
        self.zoomScale = zoomScale
        
        self.changeZoom = 0