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
"""

#TODO: Use Vertex Buffer Objects insted of client side arrays; not hard, I hope
#    : Extra note: Using PyOpenGLs VBO object causes a massive performance
#    : penalty. I suspect the bind, unbind and associated methods are not
#    : efficient enough. May have to implement it from first principals.

from PyGL3Display_infrastructure import *
from PyGL3Display_2dSprites import *


