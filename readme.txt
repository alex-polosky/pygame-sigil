||||/--------------------------------------------\||||
||/        Simple Intuitive Gaming Library         \||
||                                                  ||
|\                  AKA S.I.G.I.L                   /|
=|                                                  |=
===\                Release 3.0.0                 /===
=========\\________________________________//=========

                  The Documentation
                    Revision 3.0
in ascii form. That's right. ascii. Because I'm not 
good enough yet to make a .pdf form. So deal with it
until I make one

------------------------------------------------------

Sections:
1. Intro
2. Quick Start
3. Examples
4. The Map File
5. The Editor
6. API
7. Features To Be
8. Changelog
9. Copyright
10. Where did you get this?

------------------------------------------------------

=====================
| 1. Intro          |
=====================
Don't we all wish we could make video games really 
easily and intuitively? That all the tools needed to 
create one is all in one place? That all we have to do
is design the character, the map, then plug it in and 
press "run"?

Well now you can. SIGIL (Simple and Intuitive Gaming
Library) aims to make creating games simple, and fun,
with an intuitive syntax. So you don't have to worry
about the nitty gritty drawing details, trying to 
speed up your game as much as possible.

The main release of SIGIL uses SDL and PyGame for 
rendering and for multimedia. I also borrow the
sprite code from PyGame. There are releases planned
that will use PyOpenGl, Java [using Jython], and any
other library people can think of. 

------------------------------------------------------

=====================
| 2. Quick Start    |
=====================

------------------------------------------------------

=====================
| 3. Examples       |
=====================

------------------------------------------------------

=====================
| 4. The Map File   |
=====================

------------------------------------------------------

=====================
| 5. The Editor     |
=====================

------------------------------------------------------

=====================
| 6. The API        |
=====================

A folder should have been included with this file.
The folder should be called API, and there should
be another file alongside this one, called:
"API.html"
Open this file to view the API

File:
  - Description of File
  - Variables
  - Functions
  - Class
    - Description of Class
    - Variables
    - Functions
==========================

__init__.py

buffer.py

hud.py

locals.py

parsing.py

screen.py

sprite.py

tools.py

version.py

world.py

------------------------------------------------------

=====================
| 7. Features To Be |
=====================

 - CREATE THE MAP EDITOR!!!
 - Clean up Code
 - Split drawing + logic / World Clock? [Possibly]
 - Main Menu/Loading Menu/In-Game-Menu
 - Fix hitmask collision on zoom
 - Allow for different collisions
 - Better FPS [Possible SDL issue? Prob not]
 - Comment Source
 - Add enemy, scenery, character sections to .map
 - Create HUD class for displaying data/
    fancy overlay [Will hurt FPS on SDL]
 - Add easy sound and music support
 - Add a GUI for menus and other things
 - Allow skinning of the GUI
 - Add multiplayer support
 - Port drawing to Jython, PyOpenGL

------------------------------------------------------

=====================
| 8. ChangeLog      |
=====================

The version changes each time a change is made to the
code. 

First Number | Second Number | Third Number
============================================
API Change/  | Major Bug Fix | Minor Bug Fix
Major Fix    |

|------------------------------|
|Date     | Version   | Change |
|------------------------------|
|5/15/12  | 3.0.0     | Restarted Project
|5/26/11  | 2.0.0     | 
|5/26/11  | 1.0.1     | updated some sprite code
|12/18/10 | 1.0.0     | Released on PyGame.org
|12/18/10 | 1.0.0     | Changed name from \
                CameraEngine to SIGL
|12/11/10 | PR 0.0.1  | Released on PyGame.org
|12/11/10 | N/A       | Hosted on Google Code
|12/--/10 | N/A       | Created Project

------------------------------------------------------

=====================
| 9. Copyright      |
=====================

Created by Alex Polosky [Lord Hondros]
 - alexpolosky@gmail.com

Feel free to use my Framework/Library for any of your
projects, just make sure to give credit to me for
the actual library.

Don't copy + paste my code and say it's yours. That's
just wrong.

You may, however, look over my code and develop your
own ideas for your coding. 

------------------------------------------------------

=====================
| 10. Where Did You |
|     Get This From?|
=====================
This project has only been released for download at
Google Codes

The official release can be found here:
http://code.google.com/p/pygame-camengine/

All of the releases have been released there. If you
want to see the official PyGame releases, they are
here:
http://pygame.org/project-SIGIL-1716-2989.html

If you obtained this from anywhere else, it is not
an official copy, and kindly let me know where you got
it from, so I can contact them and have them link my
site.
------------------------------------------------------
