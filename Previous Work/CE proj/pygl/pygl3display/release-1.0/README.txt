PyGL3Display Readme
(C) Habilain 2011+
Most of this is dual licensed under the GPLv2 and GPLv3 licenses. Some files
may have different licenses; consult the source code of the file for specific
information.

Thanks for the interest in PyGL3Display.

At present the project is working up to its 0.9 release. That means there are
several important areas that are being worked on, and one of them is
documentation. As such, this Readme isn't going to provide much just yet. Only
some important notes. To get started, go look at an example or the docstrings.

The first such note is this: PyGL3Displays 2d Sprites have a *similar* feel
to Pygames 2d sprites, when using the GL3PygameSurface and GL3PGStyleSprite.
The important note is as follows: THEY ARE NOT THE SAME. Whilst the APIs are
similar, a GL3Image and a GL3Sprite of any nature are different things to
their Pygame equivelants. The biggest example of this would be image
transforms (rotation, scaling etc). In vanilla Pygame transforms are applied
to images, resulting in new images. In PyGL3Display, transforms are properties
of sprites, and the graphics hardware applies the transform.
