# The sprites need to have an extra draw function
# They also need to have two images:
#  - one for clearing [transparency of filled]
#  - one for drawing

# The sprites will have two rects;
# one for actual x/y coords,
# other for there translated coords
from pygame import sprite, rect, draw, surface

# This class should contain ALL sprites
class CamTree(sprite.RenderUpdates):

    def __init__(self, *sprites):      
        """Create a Quad Tree Object
        """
        sprite.RenderUpdates.__init__(self, sprites)
    
    # This function is ripped off of the sprite.RenderUpdates
    # function. But I make it so that way it only draws the
    # sprites that are in the cam
    def draw(self, surface):
       #a = 0
       spritedict = self.spritedict
       surface_blit = surface.blit
       dirty = self.lostsprites
       self.lostsprites = []
       dirty_append = dirty.append
       for s in self.hit():
           #a += 1
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
       return dirty#, a

    def hit(self):        
        """Return a list of items that collide with their camera
        """
        hits = []
        for x in self.sprites():
            if (
                (x.posInWorld.right >= x.camera.left)
                and
                (x.posInWorld.bottom >= x.camera.top)
                and
                (x.posInWorld.left <= x.camera.right)
                and
                (x.posInWorld.top <= x.camera.bottom)
               ):
                hits.append(x)

        return hits
    
    def getObjs(self, Obj, limit=0, sprites=None):
        ''' The Obj is another sprite to intersect
            if limit is 0, hit is called first
            if sprites is not none, that is used instead'''
        temp = []
        if (sprites == None):
            if limit == 0:
                sprites = self.sprites()
            elif limit != 0:
                sprites = self.hit()
            for x in sprites:
                if hasattr(Obj, 'rect'):
                    if Obj.rect.colliderect(x.rect):
                        temp.append(x)
                else:
                    if Obj.colliderect(x.rect):
                        temp.append(x)
        else:
            for x in sprites:
                if hasattr(Obj, 'rect'):
                    if Obj.rect.colliderect(x.rect):
                        temp.append(x)
                else:
                    if Obj.colliderect(x.rect):
                        temp.append(x)
        return temp
    
    def camUpdate(self):
        for x in self.sprites():
            if not hasattr(x, 'camUpdate'):
                x.rect.x = x.posInWorld.x - x.camera.x
                x.rect.y = x.posInWorld.y - x.camera.y
            else:
                x.camUpdate()

class CamSprite(sprite.Sprite):
    
    def __init__(self, camera, rect1, color, LINE_THICK=0, rect2=None):
        self.camera = camera
        sprite.Sprite.__init__(self)
        self.posInWorld = rect1
        if (rect2 != None):
            self.posCamera = self.rect = rect2
        else:
            self.posCamera = self.rect = \
                rect.Rect(rect1.x, rect1.y,
                          rect1.w, rect1.h)
        
        # Create the self.image
        self.image = surface.Surface((rect1.w, rect1.h))
        self.image.set_colorkey((0, 0, 0))
        draw.rect(self.image,
                         color,
                        (0, 0, rect1.w, rect1.h),
                         LINE_THICK)

    def changecam(self, camera):
        self.camera = camera
    
    def clearcam(self, surface, camera):
        pass

    def update(self, camera=None):
        if (camera != None):
            self.changecam(camera)
