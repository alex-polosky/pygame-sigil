"""
PyGL3Display
(C) David Griffin (2010-present)
"Habilain" is a pseudonym used by David Griffin in a number of places.

A high performance Pygame OpenGL library, capable of handling 1000s of sprites

Requirements: Python, Pygame, PyOpenGL, Open GL 2.0 graphics hardware

Licensed under GPLv2 or GPLv3. You should have received a copy of both of these
licenses in the files GPLv2.txt and GPLv3.txt. If not these licenses can be
found at http://www.gnu.org/licenses/gpl-2.0.html (GPLv2) and
http://www.gnu.org/licenses/gpl-3.0.html (GPLv3). By using this file you agree
to be bound by at least one of these licenses.

Other licenses, including commercial/proprietary licenses, can be arranged by 
contacting me via e-mail at habilain@gmail.com. If you do not have in physical 
writing an alternative license agreement from me, you must use one of the 
licenses specified above when releasing work which makes use of this library.

PyGL3Display_2dSprites.py

This file provides "oldschool style" 2d Sprite specific features.
"""

from __future__ import division
import math, ctypes, os, pygame, OpenGL, weakref
from PyGL3Display_infrastructure import *
from pygame.locals import *
from weakref import WeakKeyDictionary
from collections import namedtuple

GL3Rect = namedtuple('GL3Rect', ('x', 'y', 'width', 'height', 'area'))
GL3FloatCoords = namedtuple('GL3FloatCoords', ('bl', 'br', 'tr', 'tl'))

class GL3SpriteCommon(object):
    """The shared state between 2d sprites"""
    
    class __metaclass__(type):
        """Enables easy lazy creation of default objects
           by redefining the class __getattr__"""
        def __getattr__(cls, attr):
            if attr == 'defaultManager':
                kwargs = cls.defaultVertexArrays.arrayData
                kwargs['shader'] = cls.defaultShader
                cls.defaultManager = GL3TextureAtlas2dManager(**kwargs)
                return cls.defaultManager
            elif attr == 'defaultShader':
                cls.makeDefaultShader()
                return cls.defaultShader
            elif attr == 'defaultVertexArrays':
                cls.makeDefaultVertexArrays()
                return cls.defaultVertexArrays
            else:
                raise AttributeError('GL3SpriteCommon does not have ' + attr)
    
    noOfCameras = 8
    defaultArrayLength = 65535
    
    @classmethod
    def makeDefaultVertexArrays(cls):
        """Create the default vertex arrays object"""
        arrays = {'pos': 
                   [(ctypes.c_float * (4 * cls.defaultArrayLength))(), 
                   [4, GL_FLOAT, GL_FALSE, 0]],
                 'color': [(ctypes.c_uint8 * (4 * cls.defaultArrayLength))(), 
                           [4, GL_UNSIGNED_BYTE, GL_TRUE, 0]],
                 'offsets': 
                   [(ctypes.c_float * (4 * cls.defaultArrayLength))(), 
                   [4, GL_FLOAT, GL_FALSE, 0]],
                 'texOriginCoords': 
                   [(ctypes.c_float * (4 * cls.defaultArrayLength))(), 
                   [4, GL_FLOAT, GL_FALSE, 0]],
                 'rotozoomCam': 
                   [(ctypes.c_float * (4 * cls.defaultArrayLength))(), 
                   [4, GL_FLOAT, GL_FALSE, 0]],
        }
        
        cls.defaultVertexArrays = GL3VertexArrays(cls.defaultArrayLength, 
                                                  arrays)        
    @classmethod
    def makeDefaultShader(cls):
        """Create the default shader object"""
        matrixType = ctypes.c_float * 16
        # Projection matrix formulas. 
        projMatrix = matrixType()
        projMatrix[0] = 2 / GL3Common.resolution[0]
        projMatrix[5] = 2 / -GL3Common.resolution[1]
        projMatrix[12] = -1
        projMatrix[13] = 1
        projMatrix[15] = 1
        camVecType = ctypes.c_float * (2*(cls.noOfCameras))
        cls.defaultShader = GL32dSpriteShader(cls.defaultVertexArrays, 
                                              camVecType(), projMatrix)


class GL32dSpriteShader(GL3Shader):
    def __init__(self, arrays, cameraArray, projMatrix):
        """Initialise the 2d sprite shader
        Arguments:
         arrays     : A GL3VertexArrays object, which has 4d attributes for
                      pos, texOriginCoords, color, rotozoomCam and offsets
         cameraArray: A ctypes array for camera data (floats, 2* no Of Cameras
                      long)
         projMatrix : A 4x4 projection matrix"""
        noOfCameras = int(len(cameraArray) / 2)
        vertexProg = """
            attribute vec4 pos;   // x,y = position, z,w unused
            attribute vec4 texOriginCoords; // x,y = texture, z,w = origin
            attribute vec4 color; 
            attribute vec4 rotozoomCam; // x = scaleX, y = scaleY, 
                                        // z = rotation, w = camera
            attribute vec4 offsets;     // x,y = offset from origin, z,w unused
            uniform mat4 projMatrix;
            uniform vec2 cameras[""" + str(noOfCameras) + """];
            varying vec4 v2fColor;
            varying vec2 v2fTex;
            void main()
            {   vec2 offsets = vec2 ((offsets.x - texOriginCoords.z)
                                        * rotozoomCam.x,
                                     (offsets.y - texOriginCoords.w)
                                        * rotozoomCam.y);
                mat2 rotation = mat2 (cos(rotozoomCam.z), sin(rotozoomCam.z),
                                     -sin(rotozoomCam.z), cos(rotozoomCam.z));
                offsets = (rotation * offsets) - cameras[int(rotozoomCam.w)];
                vec4 vertexPos = vec4 (pos.x + offsets.x, 
                                       pos.y + offsets.y, 0, 1);
                gl_Position = projMatrix * vertexPos;
                v2fTex = texOriginCoords.xy;
                v2fColor = color;
            }"""
        fragmentProg = """
            uniform sampler2D tex;
            varying vec4 v2fColor;
            varying vec2 v2fTex;
            void main()
            {
                gl_FragColor = v2fColor * texture2D(tex, v2fTex);
            }"""

        uniforms = {'camera': 
                        [cameraArray, glUniform2fv, [noOfCameras]],
                    'projMatrix': 
                        [projMatrix, glUniformMatrix4fv, [1, GL_FALSE]]}
                        
        super(GL32dSpriteShader, self).__init__(vertexProg, fragmentProg, arrays, uniforms)
        self.vertexArray = self.arrays['pos']
        self.offsetArray = self.arrays['offsets']
        self.texArray = self.arrays['texOriginCoords']
        self.colorArray = self.arrays['color']
        self.rotozoomCamArray = self.arrays['rotozoomCam']
        self.cameras = self.uniforms['camera']
                    
    def setPositionCoords(self, slots, coord):
        """Sets each slot in slots to position coord specified
        Arguments:
         slots: list of slots to set color of
         coord: position coordinate to set slots to"""       
        for pos in slots:
            self.vertexArray[pos*4:pos*4+2] = coord
                    
    def setOffsets(self, slots, coords):
        """Set the offset of each slot in slots to the corresponding 
        element in coords
        Arguments:
         slots  : The slots to set
         coords : The offsets to set the slots to"""
        for x in xrange(len(slots)):
            self.offsetArray[slots[x]*4:slots[x]*4+2] = coords[x]
                
    def setTexCoords(self, slots, coords):
        """Set the texture coords of each slot in slots to the 
        corresponding element in coords
        Arguments:
         slots  : The slots to set
         coords : The textire coords to set the slots to"""
        for x in xrange(len(slots)):
            self.texArray[slots[x]*4:slots[x]*4+2] = coords[x]
    
    def setOriginCoords(self, slots, coord): 
        """Sets each slot in slots to origin coord specified
        Arguments:
         slots: list of slots to set color of
         coord: origin coordinate to set slots to"""
        for pos in slots:
            self.texArray[pos*4+2:pos*4+4] = coord
                    
    def setColorCoords(self, slots, color):
        """Sets each slot in slots to color specified
        Arguments:
         slots: list of slots to set color of
         color: coloration to set slots to"""
        for pos in slots:
            self.colorArray[pos*4:pos*4+4] = color 
    
    def setScaleXs(self, slots, scalex):
        """Sets each slot in slots to x scale specified
        Arguments:
         slots: list of slots to set color of
         scalex: x scale to set slots to"""
        for pos in slots:
            self.rotozoomCamArray[pos*4] = scalex
            
    def setScaleYs(self, slots, scaley):
        """Sets each slot in slots to y scale specified
        Arguments:
         slots: list of slots to set color of
         scalex: y scale to set slots to"""
        for pos in slots:
            self.rotozoomCamArray[pos*4+1] = scaley
            
    def setRotations(self, slots, rotation):
        """Sets each slot in slots to rotation specified
        Arguments:
         slots: list of slots to set color of
         rotation: rotation to set slots to"""
        for pos in slots:
            self.rotozoomCamArray[pos*4+2] = rotation

    def setCameras(self, slots, camera):
        """Sets each slot in slots to camera specified
        Arguments:
         slots: list of slots to set color of
         camera: camera to set slots to"""
        for pos in slots:
            self.rotozoomCamArray[pos*4+3] = camera
            
    def setCameraCoord(self, camera, pos):
        """Set the position of a camera.
        Arguments:
         camera : The camera to set the position of
         pos    : the position to set the camera to."""
        self.cameras[2*(camera):2*(camera)+2] = pos
        self.dirtyUniforms.add('camera')


class GL3Image(object):
    """GL3 Images are internal things, mainly. GL3Image handles the storing
    of a texture in GPU memory, and hence most of the Pygame surface duties.
    It does not handle all such duties though.
    """
    def __init__(self, atlas, redrawData, floatCoords):
        """Initialise the image"""
        self.atlas = atlas
        self.redrawData = redrawData
        self.coords = floatCoords
        self.reuploadData = None
    
    def __del__(self):
        """Deallocates the image from the texture atlas"""
        self.atlas.deallocateImage(self)
        
    def reupload(self):
        """Reuploads the surface to the texture atlas"""
        if self.reuploadData: 
            self.atlas.uploadToBox(self.reuploadData, self.redrawData)
        
    def upload(self, surface):
        """Upload a pygame surface to the atlas
        Arguments:
          surface: a pygame surface to upload"""
        self.reuploadData = surface
        self.atlas.uploadToBox(surface, self.redrawData)
        
    def subsurface(self, rect):
        """Return a subsurface of the image
           Arguments:
             rect: a Pygame Rect indicating the area to become the subsurface
        """
        dx, dy = rect.topleft
        rect.topleft = self.redrawData.left + dx, self.redrawData.top + dy
        childArea = self.redrawData.clip(rect)
        atlasWidth, atlasHeight = self.atlas.size
        top = childArea.top / atlasHeight
        bottom = childArea.bottom / atlasHeight
        left = childArea.left / atlasWidth
        right = childArea.right / atlasWidth
        
        floatCoords = GL3FloatCoords(
                      tl = (left, top),
                      tr = (right, top),
                      br = (right, bottom),
                      bl = (left, bottom)
                      )
        
        return GL3Image(self.atlas, childArea, floatCoords)


class GL3Surface(GL3Image):
    """A GL3Image which is intended to be created by the user."""
    def __init__(self, widthHeight, manager=None):
        """Initialise the Gl3Surface. 
        Arguments:
          widthHeight: A tuple containing the width / height of the surface
        """
        width, height = widthHeight
        manager = GL3SpriteCommon.defaultManager if manager is None \
                                                     else manager
        manager.getBox(width, height, self)
        self.reuploadData = None


class GL3PygameSurface(GL3Surface):
    """A Wrapper around a Pygame surface. One thing to note is that this
    maintains a copy of the surface in main memory as well as in video RAM; it
    behaves just like a Pygame surface in most respects, uploading to VRAM
    where necessary. Note that uploading is a fairly slow operation,
    especially on large surfaces, so if using this class please refrain from
    modifying large surfaces. Whilst a surface is locked, uploading doesn't
    occur, so if you're doing lots of operations it might be a good idea
    to lock the surface even if you wouldn't normally.
    
    Due to me being lazy, the docstrings are not included. Consult the pygame
    docs instead.
    """
    def __init__(self, widthheight, *args, **kwargs):
        """Initialise the GL3PygameSurface
        Arguments:
            widthheight: a tuple containing the width/height of the image
            other args as pygame surface.
        """
        if widthheight != None:
            self.surface = pygame.surface.Surface(widthheight, *args, **kwargs)
            GL3Surface.__init__(self, widthheight)
            self.upload(self.surface)
            self.parent = None

    def upload(self, surface):
        """Internal method; uploads changes in the soft-surface to the
        GL surface, when appropriate."""
        if not surface.get_locked(): GL3Image.upload(self, surface)
    
    @classmethod
    def GL3Load(cls, *args, **kwargs):
        """Replacement for pygame.image.load"""
        return cls.GL3Surfaceify(pygame.image.load(*args, **kwargs))

    @classmethod
    def GL3Surfaceify(cls, pygameSurface):
        """Convert a pygame Surface into a GL3pygameSurface"""
        ret = GL3PygameSurface(None)
        ret.surface = pygameSurface
        GL3Surface.__init__(ret, pygameSurface.get_size())
        ret.upload(pygameSurface)
        return ret
    
    def blit(self, *args, **kwargs):
        self.surface.blit(*args, **kwargs)
        self.upload(self.surface)
    
    def convert(self, *args, **kwargs): return self.GL3Surfaceify(self.surface.convert(*args, **kwargs))
    def convert_alpha(self, *args, **kwargs): 
        return self.GL3Surfaceify(self.surface.convert_alpha(*args, **kwargs))
    def copy(self): return self.GL3Surfacify(self.surface.copy(self))
    
    def fill(self, *args, **kwargs):
        self.surface.fill(*args, **kwargs)
        self.upload(self.surface)
    
    def scroll(self, dx, dy):
        self.surface.scroll(dx, dy)
        self.upload(self.surface)
        
    def set_colorkey(self, *args, **kwargs):
        self.surface.set_colorkey(*args, **kwargs)
        self.upload(self.surface)
        
    def get_colorkey(self): return self.surface.get_colorkey()
        
    def set_alpha(self, *args, **kwargs):
        self.surface.set_alpha(*args, **kwargs)
        self.upload(self.surface)
    
    def get_alpha(self): return self.surface.get_alpha()
    def lock(self): self.surface.lock()

    def unlock(self):
        self.surface.unlock()
        self.upload(self.surface)
            
    def mustlock(self): return True
    def get_locks(self): return self.surface.get_locks()
    def get_at(self, xy): return self.surface.get_at(xy)

    def set_at(self, xy, color): 
        self.surface.set_at(xy, color)
        self.upload(self.surface)
    
    def get_palette(self): return self.surface.get_palette()
    def get_palette_at(self, index): return self.surface.get_palette_at(index)
    
    def set_palette_at(self, index, rgb):
        self.surface.set_palette_at(index, rgb)
        self.upload(self.surface)
    
    def map_rgb(self, color): return self.surface.map_rgb(color)
    def unmap_rgb(self, mapped_int): return self.surface.unmap_rgb(mapped_int)
    def set_clip(self, rect): self.surface.set_clip(rect)
    def get_clip(self): return self.surface.get_clip()

    def subsurface(self, rect):
        ret = GL3PygameSurface(None)
        ret.surface = self.surface.subsurface(rect)
        ret.parent = self
        hwsubsurface = GL3Image.subsurface(rect)
        ret.coords = hwsubsurface.coords
        ret.atlas = hwsubsurface.atlas
        ret.redrawData = hwsubsurface.redrawData
        return ret
    
    def get_parent(self): return self.parent
    
    def get_abs_parent(self):
        ret = self.parent
        while ret != None: ret = ret.parent
        return ret
    
    def get_offset(self): return self.surface.get_offset()
    def get_abs_offset(self): return self.surface.get_abs_offset()
    def get_size(self): return self.surface.get_size()
    def get_width(self): return self.surface.get_width()
    def get_height(self): return self.surface.get_height()
    def get_rect(self, **kwargs): return self.surface.get_rect(**kwargs)
    def get_bit_size(self): return self.surface.get_bit_size()
    def get_byte_size(self): return self.surface.get_byte_size()
    def get_flags(self): return self.surface.get_flags()
    def get_pitch(self): return self.surface.get_pitch()
    def get_masks(self): return self.surface.get_masks()
    
    def set_masks(self, *args, **kwargs): 
        self.surface.set_masks(*args, **kwargs)
        self.upload(self.surface)
        
    def get_shifts(self): return self.surface.get_shifts()
    
    def set_shifts(self, *args, **kwargs): 
        self.surface.set_shifts(*args, **kwargs)
        self.upload(self.surface)
        
    def get_losses(self): return self.surface.get_losses()
    def get_bounding_rect(self): return self.surface.get_bounding_rect()
    def get_buffer(self): return self.surface.get_buffer()
    
GL3Load = GL3PygameSurface.GL3Load

class CannotAllocateError(Exception):
    def __init__(self, str):
        self.str = str


class CannotBlitIntoError(Exception):
    def __init__(self, str):
        self.str = str


class GL3TextureAtlas2d(object):
    """A 2d texture atlas. These are responsible for storing images, and for
    drawing to screen any sprite using an image they contain. Configured for
    optimal use when rendering squares; triangles can be rendered as well, but
    they'll be overallocated slots in the texture atlas."""
    def __init__(self, size, indicesCType, indicesType, indicesLength,
                 sizeOfIndices, manager, wasteWidth=10, border=1):
        """Initialise the texture array
        Arguments:
         size          : the size of the texture atlas to create
         indicesCType  : the ctype of the indices
         indicesType   : the GL type of the indices
         indicesLength : the number of indices
         sizeOfIndices : the size in bytes of the indices
         wasteWidth    : the wasted width tolerable
         border        : the border to give sprites; if None use 1/40th of 
                         minimum side size.
        """
        self.border = border
        self.size = size
        self.wasteWidth = wasteWidth
        self.map = [(self.size[0], (self.border, self.border))]
        self.surface = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.surface)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.size[0], self.size[1], 
                     0, GL_RGBA, GL_UNSIGNED_BYTE, 
                     (ctypes.c_int * self.size[0] * self.size[1])())      
        self.indicesArrayType = indicesCType * (int(indicesLength * 1.5))
        self.indicesType = indicesType
        self.sizeOfIndices = sizeOfIndices
        self.slots = [range(x*6, x*6+6) for \
                      x in xrange(0, int(indicesLength * 1.5 / 6))]
        self.rects = [GL3Rect(0, 0, self.size[0], self.size[1], self.size[0]*self.size[1])]
        self.layers = {}
        self.manager = manager
        self.images = WeakKeyDictionary()
    
    def unbind(self):
        """Destroy the gl texture"""
        glDeleteTextures(self.surface)
        self.surface = None
        
    def rebind(self):
        """Recreates the atlas"""
        self.surface = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.surface)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.size[0], self.size[1], 
                     0, GL_RGBA, GL_UNSIGNED_BYTE, 
                     (ctypes.c_int * self.size[0] * self.size[1])())
        
        for ref in self.images.iterkeyrefs():
            if ref(): ref().reupload()
        
    def makeLayer(self, layer):
        """Create a new layer
        Arguments:
         layer   : the layer to create
        Notes:
         The data format of the layer is a list, with items as follows:
         [0] indices: a ctypes array containing the triangle indices to draw
         [1] min: the index of the first element to draw of indices
         [2] len: the index of the last element to draw of indices - min
         [3] slots: a list of slots groups to give out
         [4] allocated: a list of slots already allocated
         [5] dirty: flag to determine if housekeeping is necessary
         [6] pending: a list of slots (ungrouped) to reuse
         [7] unusedSlots: a list of slots (grouped) to reuse
        This format is used over named tuples as named tuples do not have
        assignment to values (used on min, len, dirty) and lists are faster
        than dicts.
        """
        GL3Common.updateLayers(layer)
        self.manager.addAtlasLayer(self, layer)
        self.layers[layer] = [self.indicesArrayType(), 0, 0, \
                              self.slots[:], set(), False, [], []]
        
    def getSlots(self, no, layer):
        """Get enough slots to draw n triangles
        Arguments:
         image: The image to allocate slots to
         no: The number of triangles needed; returns no * 3 slots
         layer: The layer the sprite should appear on
        """
        if layer not in self.layers: self.makeLayer(layer)
        layerData = self.layers[layer]
        try: 
            ret = layerData[3].pop()
        except IndexError: 
            raise MemoryError('Ran out of slots in arrays or Invalid Layer')
        layerData[5] = True
        layerData[4].update(ret)
        return ret
        
    def releaseSlots(self, slots, layer):
        """Release slots from a sprite
        Arguments:
         slots: the slots to release
         layer: the layer to release the slots from
        """
        layerData = self.layers[layer]
        layerData[5] = True
        layerData[6].extend(slots)
        layerData[7].append(slots)
    
    def getAtlasImage(self, top=0.0, bottom=1.0, left=0.0, right=1.0):
        """Get an image of the atlas for debug purposes.
        Arguments:
          top, bottom, left, right: Floats between 0 and 1 describing
                                    the rectangle to view. Defaults to
                                    entire atlas.
        """
        floatCoords = GL3FloatCoords(
                      tl = (left, top),
                      tr = (right, top),
                      br = (right, bottom),
                      bl = (left, bottom)
                      )
        redrawData = Rect(left * self.size[0], top * self.size[1],
                          (right - left) * self.size[0],
                          (bottom - top) * self.size[1])
        return GL3Image(self, redrawData, floatCoords)
            
    def getBox(self, width, height, image=None):
        """Try to get a Box in this atlas. Returns None if it can't be
        allocated. 
        
        Arguments:
         width: The width to find
         height: The height to find
         image : a GL3Image to use; if None create a new GL3Image
        """
        findWidth = width + self.border
        findHeight = height + self.border
        findSize = findWidth * findHeight
        
        foundRect = None
        bestWastage = self.size[0] * self.size[1] + 1 
        for rect in self.rects:
            if rect.width > findWidth and rect.height > findHeight:
                thisWastage = rect.area - findSize
                if thisWastage < bestWastage:
                    foundRect = rect
                    bestWastage = thisWastage
        if foundRect is None:
            return None
        else:
            # We found a rect to upload to, so split it appropriately
            newX = foundRect.x + findWidth
            remainingX = foundRect.width - findWidth
            newY = foundRect.y + findHeight
            remainingY = foundRect.height - findHeight
            self.rects.remove(foundRect)
            ## Keep as large a box available as possible
            bigBox1 = GL3Rect(newX, foundRect.y, remainingX, foundRect.height,
                              remainingX * foundRect.height)
            bigBox2 = GL3Rect(foundRect.x, newY, foundRect.width, remainingY, 
                              foundRect.width * remainingY)
            if bigBox1.area > bigBox2.area:
                bigBox = bigBox1
                smallBox = GL3Rect(foundRect.x, newY, findWidth, remainingY, 
                                   findWidth * remainingY)
            else:
                bigBox = bigBox2
                smallBox = GL3Rect(newX, foundRect.y, remainingX, findHeight, 
                                   remainingX * findHeight)
            
            if bigBox.area > 0: self.rects.append(bigBox)
            if smallBox.area > 0: self.rects.append(smallBox)

            redrawData = Rect((foundRect.x, foundRect.y), 
                              (findWidth, findHeight))
            top = foundRect.y / self.size[0]
            left = foundRect.x / self.size[1]
            right = newX / self.size[0]
            bottom = newY / self.size[1]
            floatCoords = GL3FloatCoords(
                        tl = (left, top),
                        tr = (right, top),
                        br = (right, bottom),
                        bl = (left, bottom)
                        )
                        
        if not image:
            ret = GL3Image(self, redrawData, floatCoords)
            self.images[ret] = True
            return ret
        else:
            self.images[image] = True
            image.redrawData = redrawData
            image.coords = floatCoords
            image.atlas = self
            return image
            
    def deallocateImage(self, image):
        """Deallocates an image. This returns the box of the image
           to the pool. It does not defragment so fragmentation will
           happen."""
        imageRd = image.redrawData
        left, up = imageRd.left, imageRd.top
        width, height = imageRd.width, imageRd.height
        area = width * height
        self.rects.append(GL3Rect(left, up, width, height, area))

    def uploadToBox(self, image, rect):
        """Put a pygame image into a rectangle in the atlas
        Arguments:
         image: a pygame image to upload
         rect:  the rect inside the atlas to upload to
        """
        x, y = rect.topleft
        size = image.get_size()
        if size > (rect.w, rect.h):
            raise CannotBlitIntoError('Image is bigger than allocated area.')
        data = pygame.image.tostring(image , "RGBA")
        glBindTexture(GL_TEXTURE_2D, self.surface)
        glTexSubImage2D(GL_TEXTURE_2D, 0, x, y, size[0], size[1], 
                        GL_RGBA, GL_UNSIGNED_BYTE, data)
    
    def uploadQuad(self, quad, slots, layer):
        """Upload a quad to be rendered.
        Arguments:
         indices: the 4 slots corresponding to the vertices of the quad
         slots: the 6 slots to upload to
         layer: the layer to upload to
        """
        if layer not in self.layers: return
        twoTriangles = (quad[0], quad[1], quad[2], quad[0], quad[2], quad[3])
        for x in xrange(len(slots)):
            self.layers[layer][0][slots[x]] = twoTriangles[x]
    
    def uploadTriangles(self, triangles, slots, layer=0):
        """Upload some triangles to be rendered.
        Arguments:
         triangles: the 3n slots corresponding to the vertices of the triangles
         slots: the 3n slots to upload to
         layer: the layer to upload to
        """
        if layer not in self.layers: return
        for x in xrange(len(slots)):
            self.layers[layer][0][slots[x]] = triangles[x]
        
    def doTasks(self, layer):
        """Instuct the atlas to draw all sprites it is responsible for to
        screen. Will also perform housekeeping if necessary."""
        if layer not in self.layers: return
        layerData = self.layers[layer]
        
        if layerData[5] is True:
            layerData[3].extend(layerData[7])
            layerData[3].sort()
            layerData[4].difference_update(layerData[6])
            for slot in layerData[6]: layerData[0][slot] = 0
            layerData[6:8] = [], []
            layerData[5] = False
            if layerData[4]:
                layerData[1] = min(layerData[4])
                maximum = max(layerData[4])
                layerData[2] = maximum - layerData[1] + 1
            else:
                layerData[1:3] = 0, 0
        if layerData[2] == 0: return # short circuit if nothing to do
        
        glBindTexture(GL_TEXTURE_2D, self.surface)
        glDrawElements(GL_TRIANGLES, layerData[2], self.indicesType,
            self.indicesArrayType.from_address(ctypes.addressof(layerData[0]) +
                                            (self.sizeOfIndices*layerData[1])))


class GL3TextureAtlas2dManager(object):
    """Provides the necessary infrastructure to create and handle 2d texture
    atlases."""
    def __init__(self, indicesCType, indicesType, indicesLength,    
                       sizeOfIndices, shader):
        self.atlases = []
        self.length = indicesLength
        self.indicesCType = indicesCType
        self.indicesType = indicesType
        self.sizeOfIndices = sizeOfIndices
        self.minAtlasSize = 512
        self.atlasSize = 2**14
        self.atlasLayers = {}
        self.shader = shader
        self.shader.addManager(self)
        
    def rebind(self):
        """Rebind all atlases in the shader manager"""
        for atlas in self.atlases: atlas.unbind()
        for atlas in self.atlases: atlas.rebind()
        
    def findAtlasSize(self):
        """Function to determine maximum atlas size"""
        while not self.testAtlasSize(self.atlasSize):
            self.atlasSize = self.atlasSize >> 1
        if self.atlasSize <= self.minAtlasSize:
            raise MemoryError('Cannot create an atlas of minimum size')
            
    def addAtlasLayer(self, atlas, layer):
        """Allow at atlas to draw on a layer
        Arguments:
         atlas : The atlas to allow
         layer : The layer to allow to draw on"""
        if layer not in self.atlasLayers: self.atlasLayers[layer] = set()
        self.atlasLayers[layer].add(atlas)
        
    def removeAtlasLayer(self, atlas, layer):
        """Disallow an atlas to draw on a layer; this is for performance,
        if it gets used.
        Arguments:
         atlas: The atlas to disallow
         layer: The layer to disallow drawing onto"""
        if layer in self.atlasLayers: self.atlasLayer[layer].remove(atlas)
        
    def testAtlasSize(self, atlasSize):
        """Helper function to determine maximum atlas size
        Arguments:
         atlasSize : test if an atlas of atlasSizexatlasSize can be created"""
        try:
            glTexImage2D(GL_PROXY_TEXTURE_2D, 0, GL_RGBA, 
                         atlasSize, atlasSize, 0,
                         GL_RGBA, GL_UNSIGNED_BYTE, None)
            return glGetTexLevelParameteriv(GL_PROXY_TEXTURE_2D, 
                        0, GL_TEXTURE_WIDTH)
        except GLError:
            return False
                    
    def makeNewAtlas(self):
        """Create a new atlas of maximum possible size"""
        self.findAtlasSize()
        temp = GL3TextureAtlas2d(size=(self.atlasSize, self.atlasSize),
                               indicesCType = self.indicesCType,
                               indicesType = self.indicesType,
                               indicesLength = self.length,
                               sizeOfIndices = self.sizeOfIndices,
                               manager = self)
        self.atlases.append(temp)        

    def getBox(self, width, height, image=None):
        """Get a box in a texture atlas.
        Arguments:
         width  : width needed
         height : height needed
         image  : a GL3Image object; if not specified, create a new GL3Image 
        """
        if width >= self.atlasSize or height >= self.atlasSize:
            raise CannotAllocateError('Cannot allocate area of size ' +
                                      str(width) + 'x' + str(height))
        x = None
        n = len(self.atlases) - 1
        while not x and n != -1:
            x = self.atlases[n].getBox(width, height, image)
            n -= 1
        if x is None:
            self.makeNewAtlas()
            x = self.atlases[-1].getBox(width, height, image)
        return x
        
    def doTasks(self, layer):
        """Perform all tasks on a given layer
        Arguments:
         layer : the layer to draw"""
        if layer in self.atlasLayers:
            self.shader.bind()
            for atlas in self.atlasLayers[layer]:
                atlas.doTasks(layer)


class GL3Sprite(object):
    """A GL3Sprite is primarily a GL3Image and the information needed
    to draw it to screen."""
    
    def __init__(self, **kwargs):
        """Initialise the GL3Sprite. Arguments (all optional):
           image: a GL3Image to use as the sprites image.
           shader: Set the shader to use; will default to a shared
                   shader, which is normally fine. Setting the shader
                   is for advanced users.
           position: The (x, y) coordinate for the top left coordinate.
                     Default (0, 0)
           layer: The layer of the sprite. Default 0
           origin: The point relative to the top left of the texture which
                   operations happen about. Default: centre of texture.
           flipx: If the surface should be initially flipped X-axis. 
                  Default False
           flipy: If the surface should be initially flipped Y-axis. 
                  Default False
           visible: If the sprite should be visible. Default True/
           rotation: The rotation of the sprite in radians. Default 0
           scalex: The x scaling of the sprite. Default 1.
           scaley: The y scaling of the sprite. Default 1.
           scale: The scale of the sprite. Default 1. 
                  Overrides scalex and scaley.
           color: The coloration of the sprite. Uses normal pygame RGBA color
                  values. Each pixel in the image is "multiplied" by this
                  color, so it's very useful for doing fading with the alpha
                  component. Default White with full opacity (255,255,255,255)
           buffer: optional GL3SpriteBuffer for recycling the sprite
           Notes:
            As a small note, GL3Sprites are iterable. Iterating over them gives
            the sprite itself. This is done for the sake of GL3Sprite and
            GL3Group having a common interface.
        """
        if 'shader' in kwargs:
            self._shader = shader
        else:
            self._shader = GL3SpriteCommon.defaultShader
            
        self._renderSlots = self._shader.getSlots(4)
        self._twoTriangles = (self._renderSlots[0], self._renderSlots[1], 
                             self._renderSlots[2], self._renderSlots[0], 
                             self._renderSlots[2], self._renderSlots[3])

        self._atlas = None
        self._atlasSlots = []
        
        layer = kwargs['layer'] if 'layer' in kwargs else 0
        self._layer = layer
        self._flipx = False
        self._flipy = False
        self.setVisibility(kwargs.get('visible', True) )
        
        if 'image' in kwargs: self.setImage(kwargs['image'])
        else:
            self._image = None
            self._width, self._height = 0, 0
            self._baseOffsets = ((0, 0), (0, 0), (0, 0), (0, 0))
            self._shader.setOffsets(self._renderSlots, self._baseOffsets)
            
        self._buffer = kwargs.get('buffer', None) 

        scalex = kwargs.get('scalex', 1)
        scaley = kwargs.get('scaley', 1)
        scale = kwargs.get('scale', 1)
        if scale == 1:
            self.setScaleX(scalex)
            self.setScaleY(scaley)
        else:
            self.setScale(scale)
            
        self.setColoration(kwargs.get('color', (255, 255, 255, 255)))
        self.setPosition(kwargs.get('position', (0, 0)) )
        self.setLayer(layer)
        origin = kwargs.get('origin', (0.5, 0.5))
        self._origin = (self._width * origin[0], self._height * origin[1])
        self._shader.setOriginCoords(self._renderSlots, self._origin)
        self.setRotation(kwargs.get('rotation', 0))
        self.setCamera(kwargs.get('camera', 0))
        self.flipX(kwargs.get('flipx', False))
        self.flipY(kwargs.get('flipy', False))
        
    def reset(self):
        """Resets the sprite to default configuration"""
        self._shader.setOffsets(self._renderSlots, ((0,0),(0,0),(0,0),(0,0)))
        self._color = (255,255,255,255)
        self._shader.setColorCoords(self._renderSlots, self._color)
        self._position = (0, 0)
        self._visible = True
        if self._atlasSlots:
            self._atlas.uploadTriangles(self._twoTriangles, self._atlasSlots, self._layer)
        self._shader.setScaleXs(self._renderSlots, 1)
        self._shader.setScaleYs(self._renderSlots, 1)
        self._scalex = 1
        self._scaley = 1        
        self._flipx = False
        self._flipy = False
        if self._layer:
            self._layer = 0
            if self._atlasSlots:
                self._atlas.releaseSlots(self._atlasSlots, self._layer)
                self._atlasSlots = self._atlas.getSlots(2, self._layer)
                self._atlas.uploadTriangles(self._twoTriangles, self._atlasSlots, self._layer)
        self._origin = (0, 0)
        self._shader.setOriginCoords(self._renderSlots, self._origin)
                
    def __iter__(self):
        """GL3Sprites are iterable as GL3Groups are, and it's desirable to have
        both share the same interface."""
        return (self,).__iter__()
        
    def __len__(self):
        """GL3Sprites share the same API as GL3Groups, so..."""
        return 1
    
    def __del__(self):
        """Release the slots so they can be used by other things.
        Alternatively, if the sprite is registered with a buffer and the buffer
        is not yet full, return the sprite to the buffer."""
        destroy = self._buffer.releaseSprite(self) if self._buffer else True
        if destroy:
            try: self._shader.releaseSlots(self._renderSlots)
            except AttributeError: pass
            try: self._atlas.releaseSlots(self._atlasSlots, self._layer)
            except AttributeError: pass
        
    def setImage(self, image):
        """Set the image of the sprite
        Arguments:
         image: A GL3Image (or subclass) or a Pygame surface. If it's a Pygame
                surface it is converted to a GL3Image - but this won't check
                if an equivelant image has been created, so you're better off
                converting pygame surfaces to GL3Images yourself and doing
                resource management like you would in Pygame."""
        if isinstance(image, GL3Image):
            self._image = image
            self._width, self._height = self._image.redrawData.size
        else: 
            raise TypeError('surface must be a GL3image')
        
        if self._atlas != self._image.atlas:
            if self._atlas:
                self._atlas.releaseSlots(self._atlasSlots)
            self._atlas = self._image.atlas
            self._atlasSlots = self._atlas.getSlots(2, self._layer)
            if self._visible:
                self._atlas.uploadTriangles(self._twoTriangles, 
                                            self._atlasSlots, self._layer)
        
        self._baseOffsets = [(0, self._height), (self._width, self._height),
                            (self._width, 0), (0, 0)]    
        self._shader.setTexCoords(self._renderSlots, self._image.coords)
        self._shader.setOffsets(self._renderSlots, self._baseOffsets)
                
    def setColoration(self, color):
        """Set the coloration of the sprite
        Arguments:
         color : coloration to set the sprite to"""
        self._color = color
        self._shader.setColorCoords(self._renderSlots, color)
    
    def setVisibility(self, visibility):
        """Set the visibility of the sprite
        Arguments:
         visibility: if the sprite should be visible"""
        self._visible = True if visibility else False
        if self._atlasSlots:
            uploadSlots = self._twoTriangles if visibility else (0, 0, 0, 0, 0, 0)
            self._atlas.uploadTriangles(uploadSlots, self._atlasSlots, self._layer)
        
    def setScale(self, scale):
        """Set the scale of the sprite
        Arguments:
         scale: the scale to set the sprite to"""
        self._shader.setScaleXs(self._renderSlots, scale)
        self._shader.setScaleYs(self._renderSlots, scale)
        self._scalex = scale
        self._scaley = scale
        
    def setScaleX(self, scale):
        """Set the X scale of the sprite; scaling applied before rotation
        Arguments:
         scale: the scale to set the sprite to"""
        self._shader.setScaleXs(self._renderSlots, scale)
        self._scalex = scale

    def setCamera(self, camera):
        """Set the camera of the sprite
        Arguments:
         camera: the camera the sprite should be associated with"""
        self._shader.setCameras(self._renderSlots, camera)
        self._camera = camera
        
    def setScaleY(self, scale):
        """Set the Y scale of the sprite; scaling applied before rotation
        Arguments:
         scale: the scale to set the sprite to"""
        self._shader.setScaleYs(self._renderSlots, scale)
        self._scaley = scale
        
    def flipX(self, flipped = None):
        """Flip the sprite horizontally"""
        if flipped != self._flipx:
            self._flipx = not self._flipx
            self._baseOffsets = [self._baseOffsets[3], self._baseOffsets[2], 
                                self._baseOffsets[1], self._baseOffsets[0]]
            self._shader.setOffsets(self._renderSlots, self._baseOffsets)
            
    def flipY(self, flipped = None):
        """Flip the sprite vertically"""
        if flipped != self._flipy:
            self._flipy = not self._flipy
            self._baseOffsets = [self._baseOffsets[1], self._baseOffsets[0], 
                                self._baseOffsets[3], self._baseOffsets[2]]
            self._shader.setOffsets(self._renderSlots, self._baseOffsets)
            
    def setRotation(self, rotation):
        """Set the rotation of the sprite
        Arguments:
         rotation: the rotation to set the sprite to"""
        self._rotation = rotation
        self._shader.setRotations(self._renderSlots, self._rotation)

    def setLayer(self, layer):
        """Set the layer of the sprite
        Arguments:
         layer: the layer to set the sprite to"""
        if layer != self._layer and self._atlasSlots:
            self._atlas.releaseSlots(self._atlasSlots, self._layer)
            self._layer = layer
            self._atlasSlots = self._atlas.getSlots(2, layer)
            self._atlas.uploadTriangles(self._twoTriangles, self._atlasSlots, layer)
    
    def setPosition(self, newpos):
        """Set the position of the sprite
        Arguments:
         newpos: the newpos to set the sprite to"""
        self._position = newpos
        self._shader.setPositionCoords(self._renderSlots, self._position)
        
    def setOrigin(self, origin, relative=True):
        """Set the origin of the sprite. The origin is relative to the top left
        of the image, and all other attributes are calculated relative to the
        origin (i.e. position = set where the sprites origin is on screen,
        rotate/scale = rotate/scale about origin)
        
        Setting the origin adjusts the position of the sprite to compensate.
        Arguments:
         origin:   The new origin
         relative: By default, origin is specified relatively (i.e. the top
                   left of the sprite is (0,0), the bottom right (1,1)). By
                   specifying relative=False, you can set the origin in 
                   pixels.
        """
        if relative:
            origin = (self._width * origin[0], self._height * origin[1])
            
        self._position = (self._position[0] + (origin[0] - self._origin[0]),
                         self._position[1] + (origin[1] - self._origin[1]))
        self._origin = origin
        self._shader.setOriginCoords(self._renderSlots, self._origin)
        self._shader.setPositionCoords(self._renderSlots, self._position)
        

class GL3PGStyleSprite(GL3Sprite):
    """A PGStyle sprite is a sprite with extra features to make it closer to
    a Pygame sprite. It still isn't API compatible, but close. These sprites
    support assignment to variables as a "setting" operation, so for example
    "gl3pgstylesprite.position = (0, 0)" is equivelant to 
    "gl3sprite.setPosition((0,0))". However, the caveat is that performance
    is worse on a GL3PGStyleSprite.
    
    In summary, this type of sprite is easier to program but carries a
    performance penalty. 
    
    One important note: As x and y scale can be set independently, there is
    no real "good" value to return for overall scale. So if reading the
    scale attribute, you get the x scale. If you're not setting the x or y 
    scaling independently, this is always correct. If you are, then don't
    read from the scale attribute.
    
    Magic attributes are as follows:
    image    = a GL3 image to use as the sprites image
    layer    = sprite layer
    origin   = a position on the sprite _image about which positioning,
               scaling and rotation should be performed
    flipx    = if the sprite should be flipped in x axis
    flipy    = if the sprite should be flipped in y axis
    scale    = scale the sprite by this amount
    scalex   = scale the sprite in the x direction by this amount
    scaley   = scale the sprite in the y direction by this amount
    visible  = if the sprite should be visible or not
    rotation = rotate this sprite about its origin by this amount
    """
    
    __init__ = GL3Sprite.__init__
    magicVars = {'position':GL3Sprite.setPosition, 'layer':GL3Sprite.setLayer,
                 'flipx':GL3Sprite.flipX, 'flipy':GL3Sprite.flipY, 
                 'scale':GL3Sprite.setScale, 'scalex':GL3Sprite.setScaleX,
                 'scaley':GL3Sprite.setScaleY, 'camera':GL3Sprite.setCamera,
                 'visibile':GL3Sprite.setVisibility, 
                 'rotation':GL3Sprite.setRotation, 
                 'origin':GL3Sprite.setOrigin, 'image':GL3Sprite.setImage
                 }
    magicStore = {'position':'_position', 'layer':'_layer', 'flipx':'_flipx',
                  'flipy':'_flipy', 'scale':'_scalex', 'scalex':'_scalex',
                  'scaley':'_scaley', 'visible':'_visible', 
                  'rotation':'_rotation', 'camera':'_camera',
                  '_image':'_image', 'origin':'_origin'}
    
    def __setattr__(self, attr, val):
        """Used to implement 'magic' variables"""
        if attr in type(self).magicVars:
            type(self).magicVars[attr](self, val)
        else:
            object.__setattr__(self, attr, val)
    
    def __getattr__(self, attr):
        """Used to get the value of 'magic' variables"""
        if attr in type(self).magicStore:
            return getattr(self, type(self).magicStore[attr])
        else: raise AttributeError(str(type(self)) + ' has not attribute ' + attr)


class GL3SpriteBuffer(object):
    """A buffer for sprites. Creating and deleting sprites is quite taxing
    on the CPU. If a GL3Sprite is allocated a GL3SpriteBuffer, then instead of
    being deleted it may be reset and placed in the buffer for later user.
    The buffer creates sprites as necessary, but will not let sprites which
    are still useful go to waste. To use the sprite buffer, just create one
    and use the createSprite method to create sprites. Then use setX on the
    returned sprite to control the Sprite.
    """
    def __init__(self, len=100, spriteClass=GL3Sprite, 
                 resetFunc = GL3Sprite.reset):
        """Initialise the Sprite Buffer.
         Arguments:
          len: The max number of sprites to keep in the buffer
          spriteClass: the sprites class
          resetFunc: The function to call which resets the sprite to its
                     default state."""
        self.spriteBuffer = []
        self.len = len
        self.spriteClass = spriteClass
        self.resetFunc = resetFunc

    def createSprite(self):
        """Create or get a sprite which is associated with this buffer"""
        return self.spriteBuffer.pop() if self.spriteBuffer else \
               self.spriteClass(buffer=self)
        
    def releaseSprite(self, sprite):
        """Called when a sprite is deleted. If the buffer isn't full
        the sprite is kept. Otherwise, the sprite buffer tells the sprite
        to fully kill itself.
        Arguments:
         sprite: the sprite to potentially save for later"""
        if len(self.spriteBuffer) < self.len: 
            self.spriteBuffer.append(sprite)
            self.resetFunc(sprite)
            return False
        else:
            return True

    
class GL3Group(object):
    """An object to group together GL3Sprites, like a Pygame group.
    GL3Groups present a similar API to a GL3Sprite, with an operation
    applied to the group being applied to all contained sprites. Because
    the GL3Group does some caching, this normally means that the operations
    on the GL3Group are faster than what you'd get if you iterated over
    any old container of sprites.
    
    GL3Groups do not implement setImage, as it doesn't make too much sense.
    GL3Groups currently don't implement flipping.
    """
    def __init__(self, sprites=[], shader=None):
        """Create a GL3Group
           Arguments:
                sprites: The sprite or sprites to be in the group initially
        """
        self._shader = shader if shader else GL3SpriteCommon.defaultShader
        self._spritesByAtlas = {}
        self._renderSlots = set()
        self._dirtyAtlases = {}
        self._deletedRenderSlots = set()
        self._deletedSprites = set()
        self._sprites = set()
        
        for container in sprites: self.add(container)
        self.getGeometry()
        
    def __iter__(self):
        """Make the GL3Group an iterable"""
        self.clean()
        return self._sprites.__iter__()
        
    def __len__(self):
        """Provide a way of determining the number of elements in the group"""
        return self._sprites.__len__()
    
    def clean(self):
        """Remove any sprites which have been removed from the group"""
        if self._dirtyAtlases:
            for atlas in self._dirtyAtlases:
                self._spritesByAtlas[atlas][0].difference_update(
                                                  self._dirtyAtlases[atlas][0])
                self._spritesByAtlas[atlas][1].difference_update(
                                                  self._dirtyAtlases[atlas][1]) 
            self._renderSlots.difference_update(self._deletedRenderSlots)
            self._sprites.difference_update(self._deletedSprites)
            self._dirtyAtlases.clear()
            self._deletedRenderSlots.clear()
            self._deletedSprites.clear()
            
    def getGeometry(self):
        """Work out the rectangle bounding the unscaled, unrotated images in
        the group."""
        top = float('inf')
        left = float('inf')
        right = float('-inf')
        bottom = float('-inf')
        for sprite in self:            
            top = min(sprite._position[0] - sprite._origin[0], top)
            left = min(sprite._position[1] - sprite._origin[1], left) 
            right = max(sprite._position[0] - sprite._origin[0] 
                            + sprite._baseOffsets[1][0], right)
            bottom = max(sprite._position[1] - sprite._origin[1] 
                            + sprite._baseOffsets[1][1], bottom)
        return top, left, right, bottom

    def add(self, container):
        """Add a sprite or iterable container of sprites to the group
        Arguments:
         container: the sprite or container to add"""
        for sprite in container:
            if sprite._shader != self._shader:
                raise Exception('Tried to add something to a group which' + \
                                ' does not share the groups shader')
            if sprite not in self._sprites:
                spriteAtlas = sprite._atlas
                if spriteAtlas not in self._spritesByAtlas:
                    self._spritesByAtlas[spriteAtlas] = [set(),set()]
                self._spritesByAtlas[spriteAtlas][0].update(sprite._twoTriangles)
                self._spritesByAtlas[spriteAtlas][1].update(sprite._atlasSlots)
                self._sprites.add(sprite)
                self._renderSlots.update(sprite._renderSlots)

    def remove(self, container, immediate=False):
        """Remove a sprite or iterable container of sprites from the group.
        Arguments:
         container: The sprite or container of sprites to remove from the
                       group.
         immediate: For performance, remove is a lazy operation. This means
                    that the references are kept around, and so sprites
                    removed from the group won't be removed until an
                    operation is called on the group. This may be an issue
                    for deleting the sprite from screen, so by specifying
                    immediate=True you can force the sprites to immediately
                    be cleared from the group.
                    An alternative would be to set the visibility on the
                    sprite, which would have better performance.
                    """
        for sprite in container:
            if sprite in self._sprites:
                self._deletedSprites.add(sprite)
                self._deletedRenderSlots.update(sprite._renderSlots)
                spriteAtlas = sprite._atlas
                if spriteAtlas not in self._dirtyAtlases:
                    self._dirtyAtlases[spriteAtlas] = [set(),set()]
                self._dirtyAtlases[spriteAtlas][0].update(sprite._twoTriangles)
                self._dirtyAtlases[spriteAtlas][1].update(sprite._atlasSlots)
        if immediate: self.clean()
        
                                    
    def setOrigin(self, origin, relative=True, geometry=None):
        """Sets all sprites in the group to have a common origin, relative
        to the top left of the group. Then, adjusts the sprite positions so
        that they don't appear to have moved relative to each other. If you
        want to make it so that the group collectively behaves as a sprite,
        you need to call setOrigin at least once.
        
        This operation is not a particularly fast operation, because it is
        necessary to calculate the actual bounds of the group, and then do
        some math per sprite. In other words, refrain from calling too often
        on large groups; I think groups of up to about 200 at 60FPS is OK.
        Arguments:
         origin:   The new origin
         relative: By default, origin is specified relatively (i.e. the top
                   left of the group is (0,0), the bottom right (1,1)). By
                   specifying relative=False, you can set the origin in 
                   pixels.
         geometry: If you already known the edges of the group, you can
                   specify it here. If not, it is calculated, but that is
                   a fairly slow operation. The format is (top, left, right,
                   bottom). This is particularly useful for rendering text
                   strings.
        """
        if geometry is None: geometry = self.getGeometry()
        top, left, right, bottom = geometry
        if relative:
            origin = ((right - left)*origin[0], 
                      (bottom - top)*origin[1])
        if self._sprites:
            sprite = self._sprites.__iter__().next() 
            oldCoords = sprite._position
            oldOrigin = sprite._origin
            newOrigin = (oldOrigin[0] - oldCoords[0] + 
                         left + origin[0],
                         oldOrigin[1] - oldCoords[1] + 
                         top + origin[1])
            newPos = (oldCoords[0] + (newOrigin[0] - oldOrigin[0]),
                      oldCoords[1] + (newOrigin[1] - oldOrigin[1]))
            for sprite in self:
                oldOrigin = sprite._origin
                oldCoords = sprite._position
                newOrigin = (oldOrigin[0] - oldCoords[0] + 
                             left + origin[0],
                             oldOrigin[1] - oldCoords[1] + 
                             top + origin[1])
                sprite._position = newPos
                sprite._origin = newOrigin
                self._shader.setOriginCoords(sprite._renderSlots, newOrigin)
            self._shader.setPositionCoords(self._renderSlots, newPos)
    
    def setPosition(self, newPos):
        """Set the position of all sprites in the group.
        Arguments:
         newPos: The new position to set"""
        for sprite in self: sprite._position = newPos
        self._shader.setPositionCoords(self._renderSlots, newPos)
    
    def setLayer(self, layer):
        """Set the layer of all sprites in the group. This is not a
        very fast operation at present.
        Arguments:
         layer: The new layer to set"""
        for sprite in self:
            if sprite._layer != layer:
                sprite._atlas.releaseSlots(sprite._atlasSlots)
                sprite._atlasSlots = sprite._atlas.getSlots(2, layer)
                sprite._atlas.uploadTriangles(sprite._twoTriangles, 
                                             sprite._atlasSlots)
        
    def setScale(self, scale):
        """Set the scale of all sprites in the group.
        Arguments:
         scale: The new scale to set"""
        for sprite in self:
            sprite._scalex = scale
            sprite._scaley = scale
        self._shader.setScaleXs(self._renderSlots, scale)
        self._shader.setScaleYs(self._renderSlots, scale)
    
    def setScaleY(self, scaley):
        """Set the Y scale of all sprites in the group.
        Arguments:
         scaley: The new y scale to set"""
        for sprite in self: sprite._scaley = scaley
        self._shader.setScaleYs(self._renderSlots, scaley)
    
    def setScaleX(self, scalex):
        """Set the X scale of all sprites in the group.
        Arguments:
         scalex: The new x scale to set"""
        for sprite in self: sprite._scalex = scalex
        self._shader.setScaleXs(self._renderSlots, scalex)
        
    def setRotation(self, rotation):
        """Set the rotation of all sprites in the group.
        Arguments:
         rotation: The new rotation to set"""
        for sprite in self: sprite._rotation = rotation
        self._shader.setRotations(self._renderSlots, rotation)
        
    def setCamera(self, camera):
        """Set the camera of all sprites in the group.
        Arguments:
         camera: The new camera to set"""
        for sprite in self: sprite._camera = camera
        self._shader.setCameras(self._renderSlots, camera)
                            
    def setColoration(self, color):
        """Set the coloration of all sprites in the group.
        Arguments:
         color: The new color to set"""
        for sprite in self: sprite._color = color
        self._shader.setColorCoords(self._renderSlots, color)
        
    def setVisibility(self, visibility):
        """Set the visibility of all sprites in the group.
        Arguments:
         visibility: The new visibility to set"""
        self.clean()
        visibility = True if visibility else False
        for sprite in self: sprite._visible = visibility
        
        for atlas in self._spritesByAtlas:
            uploadSlots = self._spritesByAtlas[atlas][0] if visibility \
                          else (0,)*len(self._spritesByAtlas[atlas][0])
            atlas.uploadTriangles(uploadSlots, self._spritesByAtlas[atlas][1])
