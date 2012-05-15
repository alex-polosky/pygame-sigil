from locals import *
from locals import _pygame, _os, _stderr, _funny

def filePath(path):
    if "/" in path:
        path = path.split("/")
    elif "\\" in path:
        path = path.split("\\")
    if type(path) is type([]):
        return _os.path.join(*path)
    else:
        return _os.path.join(path)

IMAGES = {}
def loadImage(filename):
    if filename not in IMAGES:
        print( "Loading image: " + filename + '\n')
        if ('.' in filename):
            IMAGES[filename] = _pygame.image.load(
                filePath(filename)
                ).convert()
        else:
            IMAGES[filename] = createRect(WIDTH, HEIGHT, COLORS[filename])
    return IMAGES[filename]

def loadImage_alpha(filename):
    if filename not in IMAGES:
        print ("Loading image: " + filename + '\n')
        IMAGES[filename] = _pygame.image.load(
            filePath(filename)).convert_alpha()
    return IMAGES[filename]

def createRect(width, height,
               color=(255,255,255)):
    image = _pygame.Surface((width, height))
    _pygame.draw.rect(image,
                 color,
                 (0, 0, width, height))
    return image.subsurface(image.get_rect())

def gridBackground(width, height,
                   space=50,
                   color=(0, 0, 0), gridcolor=(20, 255, 255)):
    bg = _pygame.surface.Surface((width, height))
    bg.fill(color)
    for x in range(0, 800, space):
        r = _pygame.rect.Rect(x-1, 0, 2, 600)
        _pygame.draw.rect(bg, gridcolor, r)
    for y in range(0, 600, space):
        r = _pygame.rect.Rect(0, y-1, 800, 2)
        _pygame.draw.rect(bg, gridcolor, r)
    return bg

SOUNDS = {}
SND_VOLUME = 1.0
def playMusic(filename, loop=0, volume=1.0):
    print ("Playing music: " + filename + '\n')
    #_pygame.mixer.music.load(filePath(filename))
    _pygame.mixer.music.load(filename)
    _pygame.mixer.music.set_volume(volume*SND_VOLUME)
    _pygame.mixer.music.play(loop)
    
def loadSound(filename, volume=1.0):
    if filename not in SOUNDS:
        print ("Loading sound: " + filename + '\n')
        SOUNDS[filename] = _pygame.mixer.Sound(filePath(filename))
        SOUNDS[filename].set_volume(SND_VOLUME*volume)

def playSound(filename, volume=1.0):
    if filename not in SOUNDS:
        SOUNDS[filename] = _pygame.mixer.Sound(filepath(filename))
        SOUNDS[filename].set_volume(SND_VOLUME*volume)
    SOUNDS[filename].play()

def setSoundVolume(volume):
    global SND_VOLUME
    print ("Setting sound volume")
    if (
        (volume <= 1.0)
        and
        (volume >= 0)
        ):
        SND_VOLUME = volume
        for x in SOUNDS:
            SOUNDS[x].set_volume(SND_VOLUME*SOUNDS[x].get_volume())
        _pygame.mixer.music.set_volume(
            _pygame.mixer.music.get_volume()*SND_VOLUME
            )
    else:
        raise BaseException("volume must be in range(0.0, 1.0)")
