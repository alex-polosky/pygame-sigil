import pygame as _pygame
import os as _os

def filePath(path):
    if "/" in path:
        path = path.split("/")
    elif "\\" in path:
        path = path.split("\\")
    if type(path) is type([]):
        return os.path.join(*path)
    else:
        return os.path.join(path)

IMAGES = {}
def loadImage(filename):
    if filename not in IMAGES:
        IMAGES[filename] = pygame.image.load(
            filepath(filename)).convert_alpha()
    return IMAGES[filename]

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
    pygame.mixer.music.load(filepath(filename))
    pygame.mixer.music.set_volume(volume*SND_VOLUME)
    pygame.mixer.music.play(loop)
    
def loadSound(filename, volume=1.0):
    if filename not in SOUNDS:
        SOUNDS[filename] = pygame.mixer.Sound(filePath(filename))
        SOUNDS[filename].set_volume(SND_VOLUME*volume)

def playSound(filename, volume=1.0):
    if filename not in SOUNDS:
        SOUNDS[filename] = pygame.mixer.Sound(filepath(filename))
        SOUNDS[filename].set_volume(SND_VOLUME*volume)
    SOUNDS[filename].play()

def setSoundVolume(volume):
    global SND_VOLUME
    if (
        (volume <= 1.0)
        and
        (volume >= 0)
        ):
        SND_VOLUME = volume
        for x in SOUNDS:
            SOUNDS[x].set_volume(SND_VOLUME*SOUNDS[x].get_volume())
        pygame.mixer.music.set_volume(
            pygame.mixer.music.get_volume()*SND_VOLUME
            )
    else:
        raise BaseException, "volume must be in range(0.0, 1.0)"