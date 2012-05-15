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

PyGL3Display_infrastructure.py

This file provides the basic infrastructure of the PyGL3Display project.
"""

from __future__ import division
import math, ctypes, os, pygame, OpenGL, weakref
from OpenGL.GL import *
from pygame.locals import *

class GL3VertexArrays(object):
    """Handles Vertex arrays, so that they can be shared amongst
    shaders as necessary."""
    
    def __init__(self, noSlots, arrays):
        """Initialise the vertex array container
        Arguments:
         noSlots: The total number of slots (i.e. length of the arrays)
         arrays : A Dictionary mapping array names (as in the shader program)
                  to a list containing the array itself as first element,
                  and as second element a list of the arguments to 
                  glVertexAttribPointer, without the first (location) or 
                  last (the actual array) argument
                  e.g. [someCTypesArray, [4, GL_FLOAT, GL_FALSE, 0]]"""
        self.positions = range(noSlots)
        self.arrays = arrays
        
        if noSlots < 256:
            self.indicesType = GL_UNSIGNED_BYTE
            self.indicesCType = ctypes.c_uint8
            self.indicesArrayType = ctypes.c_uint8 * noSlots
            self.sizeOfIndices = 1
        elif noSlots < 65536:
            self.indicesType = GL_UNSIGNED_SHORT
            self.indicesCType = ctypes.c_uint16
            self.indicesArrayType = ctypes.c_uint16 * noSlots
            self.sizeOfIndices = 2
        else:
            self.indicesType = GL_UNSIGNED_INT
            self.indicesCType = ctypes.c_uint32
            self.indicesArrayType = ctypes.c_uint32 * noSlots
            self.sizeOfIndices = 4
            
        self.arrayData = {'indicesCType': self.indicesCType, 
                          'indicesType': self.indicesType,
                          'indicesLength': noSlots,
                          'sizeOfIndices': self.sizeOfIndices}
        
    def getSlots(self, no):
        """Get slots for storing vertex information
        Arguments:
         no: The number of slots to get"""
        try: return [self.positions.pop(0) for x in xrange(no)]
        except IndexError: raise MemoryError('Ran out of slots in renderer')
        
    def releaseSlots(self, slots):
        """Release slots to be reused
        Arguments:
         slots: The slots to be released"""
        self.positions.extend(slots) 
        
class GL3Shader(object):
    """Abstraction of a shader program and the vertex arrays which support it"""
    
    def __init__(self, vertexProg, fragmentProg, vertexArrays, uniforms):
        """Initialise the shader.
        Arguments:
         vertexProg  : The vertex program source
         fragmentProg: The fragment program source
         vertexArrays: A GL3VertexArrays object containing all arrays that
                       this shader will use
         uniforms    : A Dictionary mapping the name of each uniform to a list
                       with the uniforms actual value as its first element,
                       the function used to set that uniform as its second
                       element, and the arguments to that function minus
                       the first and last arguments (uniform location and
                       the uniform itself). e.g.
                         [projMatrix, glUniformMatrix4fv, [1, GL_FALSE]]
                         where projMatrix is a c_types matrix"""
        self.vertexProg = vertexProg
        self.fragmentProg = fragmentProg
        
        self.vertexArrays = vertexArrays
        
        self.inUniforms = uniforms
        self.setup()
        self.managers = weakref.WeakKeyDictionary()
        GL3Common.addShader(self)

    def setup(self):
        """Perform the setup of the actual shader program, and the necessary
        setup of data for binding arrays/uniforms."""
        
        self._vertexShader = glCreateShader(GL_VERTEX_SHADER)
        self._fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self._vertexShader, [self.vertexProg])
        glShaderSource(self._fragmentShader, [self.fragmentProg])
        glCompileShader(self._vertexShader)
        glCompileShader(self._fragmentShader)
        
        self.shaderProgram = glCreateProgram()
        glAttachShader(self.shaderProgram, self._vertexShader)
        glAttachShader(self.shaderProgram, self._fragmentShader)
        glLinkProgram(self.shaderProgram)
        
        GL3Common.useProgram(self)
        
        inArrays = self.vertexArrays.arrays
        self.arrays = dict([(key, inArrays[key][0]) for key in inArrays])
        self.arrayLocs = dict([(key, 
            glGetAttribLocation(self.shaderProgram, key)) for key in inArrays])
        self.arrayArgs = [[self.arrayLocs[key]] + inArrays[key][1] + \
                          [self.arrays[key]] for key in inArrays]
        
        self.uniforms = dict([(key, self.inUniforms[key][0])\
                               for key in self.inUniforms])
        self.uniformLocs = dict([(key, 
                                  glGetUniformLocation(self.shaderProgram, key)
                                 ) for key in self.inUniforms])
        self.dirtyUniforms = set([key for key in self.inUniforms])
        
        self.uniformArgs = dict(
            [(key, 
              (self.inUniforms[key][1], 
               [self.uniformLocs[key]] + self.inUniforms[key][2] + \
                [self.uniforms[key]],
               self.uniformLocs[key], self.uniforms[key])
             ) for key in self.inUniforms])

    def rebind(self):
        """Reset the shader, and all managers attached to it"""
        glDeleteProgram(self.shaderProgram)
        glDeleteShader(self._vertexShader)
        glDeleteShader(self._fragmentShader)
        self.setup()
        for ref in self.managers.iterkeyrefs():
            if ref(): ref().rebind()      
        
    def addManager(self, manager):
        """Add a manager which uses this shader"""
        self.managers[manager] = True
        
    def bind(self):
        """Ensure that the shader is the running program"""
        if GL3Common.boundShader is not self:
            GL3Common.useProgram(self)
            for arrayArgs in self.arrayArgs:
                GL3Common.bindArray(*arrayArgs)
            for uniform in self.uniforms:
                GL3Common.bindUniform(*self.uniformArgs[uniform], 
                                      force=uniform in self.dirtyUniforms)
            GL3Common.boundShader = self
        else:
            for uniform in self.dirtyUniforms:
                GL3Common.bindUniform(*self.uniformArgs[uniform], 
                                      force=self.uniform in self.dirtyUniforms)
        self.dirtyUniforms.clear()
            
    def doTasks(self, layer):
        """Do tasks on this layer"""        
        for manager in self.managers:
            manager.doTasks(layer=layer)        

    def getSlots(self, no):
        """Get slots for storing vertex information
        Arguments:
         no: The number of slots to get"""
        return self.vertexArrays.getSlots(no)
        
    def releaseSlots(self, slots):
        """Release slots to be reused
        Arguments:
         slots: The slots to be released"""
        self.vertexArrays.releaseSlots(slots)


class GL3Common(object):
    """The 'shared state' between other things, mainly to track the GL state"""
    shaders = weakref.WeakKeyDictionary()
    layers = []
    currentProgram = None
    boundArrays = {}
    boundUniforms = {}
    boundShader = None
    
    @classmethod
    def useProgram(cls, program):
        """Replaces calls to glUseProgram. Only changes the program as
        necessary, which is somewhat faster.
        Arguments:
         program: The program to use"""
        if cls.currentProgram is not program:
            cls.currentProgram = program
            glUseProgram(program.shaderProgram)
            
    @classmethod
    def updateLayers(cls, layer):
        """Add a new rendering layer"""
        if layer not in cls.layers:
            cls.layers.append(layer)
            cls.layers.sort()
    
    @classmethod
    def bindArray(cls, index, glSize, glType, glNormalise, glStride, array, 
                  force=False):
        """Replaces calls to glVertexAttribPointer, glEnableVertexAttribArray
        and glDisableVertexAttribArray. Performs the binding on an "as 
        necessary" basis, which is somewhat faster. Arguments the same as
        glEnableVertexAttribArray.
        Additional arguments:
         force: The detection is by index/array, not by any other arguments. On
         the off chance that someone wants to change the arguments on 
         glVertexAttribPointers (which I can't think of why you'd want to do)
         specifying force guarantees that the array will be rebound.
        """
        if cls.boundArrays.get(index, None) is not array or force:
            cls.boundArrays[index] = array
            glDisableVertexAttribArray(index)
            glVertexAttribPointer(index, glSize, glType, glNormalise, 
                                  glStride, array)
            glEnableVertexAttribArray(index)
            
    @classmethod
    def bindUniform(cls, bindFunc, args, index, array, force=False):
        """Replaces calls to glUniform functions. Performs binding on an
           as necessary basis.
           Arguments:
             bindFunc: The OpenGL function that binds the uniform 
                       (e.g. glUniform1v)
             args    : A list of arguments to bindFunc which will bind the
                       uniform as desired.
             force   : Force, even if array already bound (to change arguments
                       on bindFunc)
        """
        if cls.boundUniforms.get(args[0], None) is not array or force:
            cls.boundArrays[index] = array
            bindFunc(*args)
                    
    @classmethod
    def initEnvironment(cls, resolution, mode=0):
        """Initialise the OpenGL environment. This function is basically
        a version of display.set_mode which should always work. The mode
        argument automatically has the OPENGL and DOUBLEBUF flags added to
        it.
          Arguments:
            resolution: The resolution of the window
            mode: Additional parameters to give to pygames set_mode call
        """
        
        mode = pygame.OPENGL | pygame.DOUBLEBUF | mode
        
        pygame.init()
        pygame.display.set_mode(resolution, mode)
        
        glViewport(0, 0, resolution[0], resolution[1])
        glClearColor(0.0,0.5,1.0,1.0)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        cls.resolution = resolution
        
        # Recreate the context as necessary
        if os.name in ('nt',):
            for ref in cls.shaders.iterkeyrefs():
                if ref(): 
                    ref().rebind()
            
    @classmethod
    def addShader(cls, shader):
        """Register a shader with GL3Common"""
        cls.shaders[shader] = True
        
    @classmethod
    def doTasks(cls):
        """Draw everything that GL3Common knows about"""
        cls.clear()
        for layer in cls.layers:
            for ref in cls.shaders.iterkeyrefs():
                if ref(): 
                    shader = ref()
                    if cls.boundShader is not shader: shader.bind()
                    shader.doTasks(layer=layer)
        pygame.display.flip()
 
    @classmethod
    def clear(cls):
        """Clears the screen"""
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) 
    
    @classmethod
    def setClearColour(cls, rgba):
        """Set the colour to clear the screen with"""
        if len(rgba) == 3: rgba.append(255)
        r,g,b,a = [x/255 for x in rgba]
        OpenGL.GL.glClearColor(r,g,b,a)

