"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object. So technically Bolt, which has a velocity,
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you
add new features to your game, such as power-ups.  If you are unsure about whether to
make a new class or not, please ask on Piazza.

# Mitchell Lin ml887 and Alina Kim ak778
# 12/4/18
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, xpos, ypos, image):
        super().__init__(x=xpos, y=ypos, width= SHIP_WIDTH, \
        height=SHIP_HEIGHT, source = image)
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        x = bolt.getx()
        y = bolt.gety()
        if self.contains((x+BOLT_WIDTH/2,y+BOLT_HEIGHT/2)):
            return True
        if self.contains((x+BOLT_WIDTH/2,y-BOLT_HEIGHT/2)):
            return True
        if self.contains((x-BOLT_WIDTH/2,y+BOLT_HEIGHT/2)):
            return True
        if self.contains((x-BOLT_WIDTH/2,y-BOLT_HEIGHT/2)):
            return True
        return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _x: previous x position of the alien
    _y: previous y position of the alien
    _source: records the source image of the alien
    health: extension health is an integer that represents alien health
    """
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    #def setx(self, x):
    #    self._x = x
    #def getx(self):
    #    return self._x

    #def sety(self, y):
    #    self._y = y
    #def gety(self):
    #    return self._y

    #def setsource(self, source):
    #    self._source = source
    #def getsource(self):
    #    return self._source
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, xpos, ypos, image):
        super().__init__(x=xpos, y=ypos, width=ALIEN_WIDTH, \
        height=ALIEN_HEIGHT, source=image)
        self.health = 100 #ADD MORE ATTRIBUTES
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        x = bolt.getx()
        y = bolt.gety()
        if self.contains((x+BOLT_WIDTH/2,y+BOLT_HEIGHT/2)):
            return True
        if self.contains((x+BOLT_WIDTH/2,y-BOLT_HEIGHT/2)):
            return True
        if self.contains((x-BOLT_WIDTH/2,y+BOLT_HEIGHT/2)):
            return True
        if self.contains((x-BOLT_WIDTH/2,y-BOLT_HEIGHT/2)):
            return True
        return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def changex(self, right):
        if right == True:
            #super().__init__(x=ALIEN_H_WALK+self.x, y=self.y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT, source=self._source)
            #self.setx(ALIEN_H_WALK+self.x)
            self.x = self.x + ALIEN_H_WALK
        else:
            #super().__init__(x=-ALIEN_H_WALK+self.x, y=self.y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT, source=self._source)
            #self.setx(-ALIEN_H_WALK+self.x)
            self.x = self.x - ALIEN_H_WALK

    def changey(self):
        #super().__init__(x=self.x, y=-ALIEN_V_WALK+self.y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT, source=self._source)
        self.y = self.y - ALIEN_V_WALK


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need getters for
    them.  However, it is possible to write this assignment with no setters for the
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.

    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a
    helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    playerbolt: true if bolt is from the player, false if created by enemies
        invariant: is a bool
    """
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getx(self):
        """
        getter for the x value for Bolt
        """
        return self.x

    def gety(self):
        """
        getter for the y value for Bolt
        """
        return self.y

    def getPlayerbolt(self):
        """
        getter for the _playerbolt attribute for Bolt
        """
        return self.playerbolt

    def setPlayerbolt(self, bolt):
        """
        getter for the _playerbolt attribute for Bolt
        """
        self.playerbolt = bolt

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, xpos, ypos, playerbolt, color ):
        """
        Initializer for the bolt class

        Creates a bolt object with positions xpos, ypos, and with playerbolt as
        a boolean to distinguish whether the bolt was created by a player or
        an Alien.

        Parameter xpos: initial x position of the bolt to set
        Precondition: xpos is a float corresponding to the Alien or Ship x value

        Parameter ypos: initial y position of the bolt to set
        Precondition: ypos is a float corresponding to the Alien or Ship y value

        Parameter playerbolt: boolean that distinguishes between player and Alien bolts.
        if playerbolt is True, the bolt is from the Ship.
        if playerbolt is False, the bolt is from an Alien.
        Precondition: playerbolt is a bool
        """
        assert type(playerbolt) == bool
        super().__init__(x=xpos, y=ypos, width=BOLT_WIDTH,
        height=BOLT_HEIGHT, fillcolor=color)
        self._velocity = (BOLT_SPEED)
        self.setPlayerbolt(playerbolt)

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def updatepos(self):
        """
        Updates the position of the bolt

        When called, the y position of the bolt will change according to playerbolt.
        If playerbolt is True, the y position will increase by _velocity.
        If playerbolt is False, the y position will decrease by _velocity
        """
        if self.getPlayerbolt() == True:
            self.y += self._velocity
        else:
            self.y -= self._velocity

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE

class ShipLives(GImage):
    """
    A class to represent the lives as ship images
    """
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, xpos, ypos, image):
        super().__init__(x=xpos, y=ypos, width= 32, height=32, source = image)
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS


class AlienHealthBar(GRectangle):
    pass
    def __init__(self, xpos, ypos, health):
        super().__init__(x=xpos, y=ypos-(ALIEN_HEIGHT/2), width=health/2.5, \
        height=5, fillcolor = introcs.RGB(60,250,20))

    def updatebar(self, xpos, ypos, health):
        self.x = xpos - 20  + (health/5)
        self.y = ypos-(ALIEN_HEIGHT/2)
        if not health <=0:
            self.width = health/2.5


class AlienHealthBarNeg(GRectangle):
    pass
    def __init__(self, xpos, ypos, health):
        super().__init__(x=xpos, y=ypos-(ALIEN_HEIGHT/2), width=health/2.5, \
        height=5, fillcolor = introcs.RGB(237,40,50))

    def updatebar(self, xpos, ypos, health):
        self.x = xpos + 12.5 - (25-health/2.5)/2
        self.y = ypos-(ALIEN_HEIGHT/2)
        if not health <=0:
            self.width = (100.1-health)/2.5
