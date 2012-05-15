#! /usr/bin/env python
# This is a .map loader for use with my
# tile maps

# Next step is to allow loading of
# an enemy sprite part

from locals import *
from locals import _pygame, _os, _stderr
import sprite
import tools

class Parser(object):

    def loadMap(self, mapString):
        return [[int(y) for y in x.split(' ')] for x in mapString.split('\n')]

    def uncommentString(self, string):
        # new is the string to return
        # uncomment is 1 when a comment is found
        
        new = ''
        uncomment = 0

        newline = 0
        
        for x in range(0, len(string)):
            if (string[x] == '#'):
                if ((uncomment == 0) and (newline != 1)):
                    new += '\n'
                uncomment = 1
            newline = 0

            if (uncomment != 1):
                new += string[x]

            if (string[x] == '\n'):
                uncomment = 0
                newline = 1
                
        return new

    def getSections(self, string):
        string = self.uncommentString(string)
        sections = string.split('\n\n')
        new = []
        for s in sections:
            head = ''
            body = ''
            tag = 0
            for x in s:
                if (x == '['):
                    tag = 1
                if ((tag == 1) and (x != '[') and (x != ']')):
                    head += x
                if (tag == 0):
                    body += x
                if (x == ']'):
                    tag = 0
            try:
                if (body[-1] == '\n'):
                    body = body[:-1]
            except:
                print sections
                print head
                print body
            new.append([head, body[1:]])
        #return new
        toret = []
        for x in new:
            if ((x[0] != 'Design') and (x[0] != 'Collision')):
                attrs = {}
                for line in x[1].split('\n'):
                    att = line.split('=')[1]
                    try:
                        att0 = int(line.split('=')[0])
                    except:
                        att0 = line.split('=')[0]
                    attrs[att0] = eval(att)
                toret.append([x[0], attrs])
            else:
                toret.append([x[0], {'Map':self.loadMap(x[1])}])
        #return dict(toret)
        toret = dict(toret)
        for x in toret['Design-Config']:
            toret['Design'][x] = toret['Design-Config'][x]
        for x in toret['Collision-Config']:
            toret['Collision'][x] = toret['Collision-Config'][x]
        del toret['Design-Config']
        del toret['Collision-Config']
        return toret

class Map(object):

    def __init__(
        self,
        name, # Name of map
        _type, # Type of map
        size, # Tuple of grids
        layout, # Grid
        collision, # Grid
        camera=None, # only used in creating Camera Sprites
        background=None, # Background path
        tileSize=(24,24), # size of tiles
        layoutImage={0:None}, # paths to image numbers
        collisionTypes={0:None}, # types of collisions
        ):
        self.name = name
        self.type = _type
        self.size = size
        self.layout = layout
        self.collision = collision
        self.camera = camera
        
        if (background == None):
            self.background = _pygame.Surface((WIDTH, HEIGHT))
            self.background.fill(COLORS['black'])
        else:
            self.background = tools.loadImage(background)
        
        
        self.tileSize = tileSize
        self.defaultTile = _pygame.Surface(tileSize)
        self.defaultTile.set_alpha(0)
        
        self.layoutImage = {0:self.defaultTile}
        for x in layoutImage:
            if ((x != -1) and (x != 'Map')):
                try:
                    if (type(layoutImage) != type([])):
                        layoutImage[x] = [layoutImage[x], 0, 0]
                    
                    if (layoutImage[x][0] in COLORS):
                        #print COLORS[layoutImage[x][0]]
                        load = tools.createRect(
                            tileSize[0], tileSize[1], COLORS[layoutImage[x][0]]
                        )
                    elif (
                        (
                            (type(layoutImage[x][0]) == type([]))
                            or
                            (type(layoutImage[x][0]) == type(tuple([])))
                        )
                        and
                        (len(layoutImage[x][0]) == 3)
                        ):
                        load = tools.createRect(
                            tileSize[0], tileSize[1], layoutImage[x][0]
                        )
                    else:                
                        load = tools.loadImage(layoutImage[x][0])
                    
                    location = layoutImage[x][1] * tileSize[0] , \
                                   layoutImage[x][2] * tileSize[1]
                        
                    image = _pygame.Surface(tileSize)
                    image.blit(load, [0, 0, 0, 0],
                               [location[0], location[1], load.get_width(), load.get_height()])
                except:
                    print("Warning: %s was not loaded" %(layoutImage[x][0].__repr__()))
                    image = self.defaultTile
                self.layoutImage[x] = image
        
        self.collisionTypes = {}
        for x in collisionTypes:
            if (x != 'Map'):
                self.collisionTypes[x] = collisionTypes[x]

    def createSprites(self):
        if (self.type == 'Normal'):
            group = sprite.Group()
        elif (self.type == 'Camera'):
            group = sprite.CamGroup()
        elif (self.type == 'Camera-Zoom'):
            group = sprite.ZoomGroup()

        for R in range(0, self.size[0]):
            for C in range(0, self.size[1]):
                if (self.layout[R][C] != 0):
                    rect = _pygame.rect.Rect(
                        C*self.tileSize[0], R*self.tileSize[1],
                        self.tileSize[0], self.tileSize[1]
                        )
                    image = self.layoutImage[self.layout[R][C]].copy()
                    
                    collision = self.collisionTypes[self.collision[R][C]]
                    camera = self.camera
                    #if ('Camera' not in self.type):
                    #    group.add(sprite.Sprite(rect, image, collision))
                    if (self.type == 'Camera'):
                        group.add(sprite.CamSprite(rect, image,  camera, collision))
                    elif (self.type == 'Camera-Zoom'):
                        group.add(sprite.ZoomSprite(rect, image, camera, collision))
        return group

    def __getitem__(self, key):
        if (
            (type(key) != type(tuple([])))
            and
            (type(key) != type([]))
            ):
            raise KeyError, "Index must be a list or tuple of two elements"
        if (len(key) != 2):
            raise KeyError, "Index must be a list or tuple of two elements"
        try:
            return self.layout[key[0]][key[1]], self.collision[key[0]][key[1]]
        except IndexError:
            raise IndexError, "No tile found at (%d, %d)" %key

    def __setitem__(self, key, attr):
        if (
            (type(key) != type(tuple([])))
            and
            (type(key) != type([]))
            ):
            raise KeyError, "Index must be a list or tuple of two elements"
        if (len(key) != 2):
            raise KeyError, "Index must be a list or tuple of two elements"
        if (len(attr) != 2):
            raise AttributeError, "Attribute must have an item for each map"
        if (type(attr[0]) != type(0)):
            raise AttributeError, "Attribute [0] must be an integer representing design"
        if (type(attr[1]) != type(0)):
            raise AttributeError, "Attribute [1] must be an integer representing collision"
        
        try:
            cur = self[key]
        except IndexError:
            raise IndexError, "No tile found at (%d, %d)" %(key)
        self.layout[key[0]][key[1]] = attr[0]
        self.collision[key[0]][key[1]] = attr[1]

    def __repr__(self):
        toret = ''
        toret += ("<Map Object '%s' with size (%d, %d)>" %(self.name, self.size[0], self.size[1]))
        toret += '\n'
        toret += ("Tile Size: (%d, %d)" %self.tileSize)
        toret += '\n'
        toret += ("Layout:")
        toret += '\n'
        for x in self.layout: toret += ' '.join([str(y) for y in x]); toret += '\n'
        toret += ("Collision:")
        toret += '\n'
        for x in self.collision: toret += ' '.join([str(y) for y in x]); toret += '\n'
        toret += ("</Map>")
        return toret

    def __len__(self):
        return self.size[0] * self.size[1]

def getMap(map,Camera=None):
    map = tools.filePath(map)
    P = Parser()
    f = open(map)
    data = f.read()
    f.close()
    data = P.getSections(data)
    return Map(
        data['Map']['Name'],
        data['Map']['Type'],
        data['Map']['Size'],
        data['Design']['Map'],
        data['Collision']['Map'],
        camera=Camera,
        tileSize=data['Map']['TileSize'],
        layoutImage=data['Design'],
        collisionTypes=data['Collision']
    )

if (__name__ == '__main__'):
    
    # This is an example .map file
    example='''\
[Map]
Name='Test'
Type='Camera'
Background='./Data/background.png'
#Background.800='./Data/background-800.png'
#Background.640='./Data/background-640.png'
TileSize=16,16 # Can be any size so long as it's square
Size=6,24

[Design]
0 4 5 0 0 0 0 0 0 4 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

[Design-Config]
0=None
1='./Data/ground.png',0,0 # 0,0 is the position and is assumed
2='./Data/lava.png'
3='./Data/cloud.png'
4='./Data/cloud-L.png',0,0
5='./Data/cloud-L.png',0,1
6='./Data/block.png'

[Collision]
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 4 4 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

[Collision-Config]
0=None
1=Platform
2=Block
3=Pickup
4=Kill
'''
    P = Parser()
    data = P.getSections(example)
    M = Map(
            data['Map']['Name'],
            data['Map']['Type'],
            data['Map']['Size'],
            data['Design']['Map'],
            data['Collision']['Map'],
            tileSize=data['Map']['TileSize'],
            layoutImage=data['Design'],
            collisionTypes=data['Collision']
            )
    a = M.createSprites()
    #b = a.sprites()[0]
