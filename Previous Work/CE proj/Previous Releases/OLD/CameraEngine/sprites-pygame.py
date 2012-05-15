class AbstractGroup(object):
    """A base for containers for sprites. It does everything
       needed to behave as a normal group. You can easily inherit
       a new group class from this, or the other groups below,
       if you want to add more features.

       Any AbstractGroup-derived sprite groups act like sequences,
       and support iteration, len, and so on."""

    # dummy val to identify sprite groups, and avoid infinite recursion.
    _spritegroup = True

    def __init__(self):
        self.spritedict = {}
        self.lostsprites = []

    def sprites(self):
        """sprites()
           get a list of sprites in the group

           Returns an object that can be looped over with a 'for' loop.
           (For now it is always a list, but newer version of Python
           could return different iterators.) You can also iterate directly
           over the sprite group."""
        return list(self.spritedict.keys())

    def add_internal(self, sprite):
        self.spritedict[sprite] = 0

    def remove_internal(self, sprite):
        r = self.spritedict[sprite]
        if r is not 0:
            self.lostsprites.append(r)
        del(self.spritedict[sprite])

    def has_internal(self, sprite):
        return sprite in self.spritedict

    def copy(self):
        """copy()
           copy a group with all the same sprites

           Returns a copy of the group that is the same class
           type, and has the same sprites in it."""
        return self.__class__(self.sprites())

    def __iter__(self):
        return iter(self.sprites())

    def __contains__(self, sprite):
        return self.has(sprite)

    def add(self, *sprites):
        """add(sprite, list, or group, ...)
           add sprite to group

           Add a sprite or sequence of sprites to a group."""
        for sprite in sprites:
            # It's possible that some sprite is also an iterator.
            # If this is the case, we should add the sprite itself,
            # and not the objects it iterates over.
            if isinstance(sprite, Sprite):
                if not self.has_internal(sprite):
                    self.add_internal(sprite)
                    sprite.add_internal(self)
            else:
                try:
                    # See if sprite is an iterator, like a list or sprite
                    # group.
                    for spr in sprite:
                        self.add(spr)
                except (TypeError, AttributeError):
                    # Not iterable, this is probably a sprite that happens
                    # to not subclass Sprite. Alternately, it could be an
                    # old-style sprite group.
                    if hasattr(sprite, '_spritegroup'):
                        for spr in sprite.sprites():
                            if not self.has_internal(spr):
                                self.add_internal(spr)
                                spr.add_internal(self)
                    elif not self.has_internal(sprite):
                        self.add_internal(sprite)
                        sprite.add_internal(self)

    def remove(self, *sprites):
        """remove(sprite, list, or group, ...)
           remove sprite from group

           Remove a sprite or sequence of sprites from a group."""
        # This function behaves essentially the same as Group.add.
        # Check for Spritehood, check for iterability, check for
        # old-style sprite group, and fall back to assuming
        # spritehood.
        for sprite in sprites:
            if isinstance(sprite, Sprite):
                if self.has_internal(sprite):
                    self.remove_internal(sprite)
                    sprite.remove_internal(self)
            else:
                try:
                    for spr in sprite: self.remove(spr)
                except (TypeError, AttributeError):
                    if hasattr(sprite, '_spritegroup'):
                        for spr in sprite.sprites():
                            if self.has_internal(spr):
                                self.remove_internal(spr)
                                spr.remove_internal(self)
                    elif self.has_internal(sprite):
                        self.remove_internal(sprite)
                        sprite.remove_internal(self)

    def has(self, *sprites):
        """has(sprite or group, ...)
           ask if group has a sprite or sprites

           Returns true if the given sprite or sprites are
           contained in the group. You can also use 'sprite in group'
           or 'subgroup in group'."""
        # Again, this follows the basic pattern of Group.add and
        # Group.remove.
        for sprite in sprites:
            if isinstance(sprite, Sprite):
                return self.has_internal(sprite)

            try:
                for spr in sprite:
                    if not self.has(spr):
                        return False
                return True
            except (TypeError, AttributeError):
                if hasattr(sprite, '_spritegroup'):
                    for spr in sprite.sprites():
                        if not self.has_internal(spr):
                            return False
                    return True
                else:
                    return self.has_internal(sprite)

    def update(self, *args):
        """update(*args)
           call update for all member sprites

           calls the update method for all sprites in the group.
           Passes all arguments on to the Sprite update function."""
        for s in self.sprites(): s.update(*args)

    def draw(self, surface):
        """draw(surface)
           draw all sprites onto the surface

           Draws all the sprites onto the given surface."""
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []

    def clear(self, surface, bgd):
        """clear(surface, bgd)
           erase the previous position of all sprites

           Clears the area of all drawn sprites. the bgd
           argument should be Surface which is the same
           dimensions as the surface. The bgd can also be
           a function which gets called with the passed
           surface and the area to be cleared."""
        try:
            bgd.__call__
        except AttributeError:
            pass
        else:
            for r in self.lostsprites:
                bgd(surface, r)
            for r in self.spritedict.values():
                if r is not 0: bgd(surface, r)
            return
        surface_blit = surface.blit
        for r in self.lostsprites:
            surface_blit(bgd, r, r)
        for r in self.spritedict.values():
            if r is not 0: surface_blit(bgd, r, r)

    def empty(self):
        """empty()
           remove all sprites

           Removes all the sprites from the group."""
        for s in self.sprites():
            self.remove_internal(s)
            s.remove_internal(self)

    def __nonzero__(self):
        return (len(self.sprites()) != 0)

    def __len__(self):
        """len(group)
           number of sprites in group

           Returns the number of sprites contained in the group."""
        return len(self.sprites())

    def __repr__(self):
        return "<%s(%d sprites)>" % (self.__class__.__name__, len(self))

class Group(AbstractGroup):
    """container class for many Sprites
    pygame.sprite.Group(*sprites): return Group

    A simple container for Sprite objects. This class can be inherited to
    create containers with more specific behaviors. The constructor takes any 
    number of Sprite arguments to add to the Group. The group supports the
    following standard Python operations:

        in      test if a Sprite is contained
        len     the number of Sprites contained
        bool test if any Sprites are contained
        iter    iterate through all the Sprites

    The Sprites in the Group are not ordered, so drawing and iterating the 
    Sprites is in no particular order.
    """
    
    def __init__(self, *sprites):
        AbstractGroup.__init__(self)
        self.add(*sprites)

RenderPlain = Group
RenderClear = Group

class RenderUpdates(Group):
    """Group class that tracks dirty updates
    pygame.sprite.RenderUpdates(*sprites): return RenderUpdates

    This class is derived from pygame.sprite.Group(). It has an extended draw()
    method that tracks the changed areas of the screen.
    """
    
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
