"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# Mitchell Lin ml887 and Alina Kim ak778
# 12/4/18
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    right: boolean, moves right = true, moves left = false
    aliensteps: int, counts number of times the aliens have moved
    rightmost = float or int, rightmost x position of the Aliens
    leftmost = float or int, leftmost x position of the Aliens
    paused = boolean, tells whether game is paused or not
    complete = boolean, true if game is over, false if not
    speed = float, taken from ALIEN_SPEED
    shoottime = time passed since a player bolt was fired.
    healthbars = 2d list of Alien healthbars showing HP left
    healthbarsneg = 2d list of Alien healthbars showing HP depleted
    _shiplives: list of Ship objects for lives indicator
    alienCooldown: int, number of steps aliens must move before they can fire again,
        randomized every time aliens shoot
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getComplete(self):
        """
        Getter for complete attribute
        Returns True if game is over and False if not
        """
        return self.complete #ADD MORE ATTRIBUTES

    def setComplete(self, complete):
        """
        Setter for complete attribute

        Parameter: complete is True if game is complete and False otherwise
        Precondition: complete is of type boolean
        """
        assert type(complete) == bool
        self.complete = complete #ADD MORE ATTRIBUTES

    def getPaused(self):
        """
        Getter for paused attribute
        Returns True if game is paused or False if game is not
        """
        return self.paused #ADD MORE ATTRIBUTES

    def setPaused(self, paused):
        """
        Setter for paused attribute

        Parameter: paused is True if game is paused and False if the game is not
        Precondition: paused is a boolean value
        """
        assert type(paused) == bool
        self.paused = paused #ADD MORE ATTRIBUTES

    def setAliens(self, arr):
        """
        Setter for _aliens attribute

        Parameter: arr gives a list of existing Alien objects (if any)
        Precondition: arr is either None or of type list
        """
        assert type(arr) == list or arr is None
        self._aliens = arr

    def getAliens(self):
        """
        Getter for _aliens attribute
        Returns array of Alien objects (if any)
        """
        return self._aliens

    def setAliensteps(self, steps):
        """
        Setter for aliensteps attribute

        Parameter: steps indicates number of times the aliens have moved
        Precondition: steps is of type int
        """
        assert type(steps) == int
        self.aliensteps = steps #ADD MORE ATTRIBUTES

    def getAliensteps(self):
        """
        Getter for aliensteps attribute
        Returns number of times the aliens have moved
        """
        return self.aliensteps #ADD MORE ATTRIBUTES

    def setShip(self, ship):
        """
        Setter for _ship attribute

        Parameter: ship is the Ship object the user controls
        Precondition: ship is of instance Ship
        """
        self._ship = ship

    def getShip(self):
        """
        Getter for _ship attribute
        Returns the Ship object the user controls
        """
        return self._ship

    def setDefense(self, line):
        """
        Setter for _dline attribute

        Parameter: line is the defensive line separating the ship and aliens
        Precondition: line is an instance of a GPath object
        """
        assert isinstance(line, GPath)
        self._dline = line

    def getDefense(self):
        """
        Getter for _dline attribute
        Returns the GPath object that is the defensive line separating the ship
        and aliens
        """
        return self._dline

    def setTime(self,time):
        """
        Setter for _time attribute

        Parameter: time represents the amount of time since the last Alien step
        Precondition: time is an int or float >= 0
        """
        assert type(time) == int or type(time) == float
        assert time >= 0
        self._time = time

    def getTime(self):
        """
        Getter for _time attribute
        Returns the amount of time since the last Alien "step"
        """
        return self._time

    def setRight(self, right):
        """
        Setter for right attribute

        Parameter: right is True if an object is moving right and False if
        moving left
        Precondition: right is of type boolean
        """
        assert type(right) == bool
        self.right = right #ADD MORE ATTRIBUTES

    def getRight(self):
        """
        Getter for right attribute
        Returns True if object is moving right and False if moving left
        """
        return self.right #ADD MORE ATTRIBUTES

    def setBolt(self, bolt):
        """
        Setter for _bolts attribute

        Parameter: bolt
        Precondition: bolt is an instance of GRectangle
        """
        self._bolts = bolt

    def getBolt(self):
        """
        Getter for _bolts attribute
        Returns list of bolt objects
        """
        return self._bolts

    def getLives(self):
        """
        Getter for _lives object
        Returns number of lives ship has left
        """
        return self._lives

    def setLives(self, lives):
        """
        Setter for _lives object

        Parameter: lives indicates number of lives ship has left
        Precondition: lives is an int >= 0 and <= SHIP_LIVES
        """
        assert type(lives) == int
        assert lives >= 0 and lives <= SHIP_LIVES
        self._lives = lives

    def getSpeed(self):
        """
        Getter for speed attribute
        Returns speed of aliens
        """
        return self.speed #ADD MORE ATTRIBUTES

    def setSpeed(self, speed):
        """
        Setter for speed attribute

        Parameter: speed indicates speed of aliens
        Precondition: speed is a float or int taken from SHIP_SPEED
        """
        assert type(speed) == float or type(speed) == int
        self.speed = speed #ADD MORE ATTRIBUTES

    def getAlienCooldown(self):
        """
        Getter for alienCooldown attribute
        Returns number of steps aliens must move before firing again
        """
        return self.alienCooldown #ADD MORE ATTRIBUTES

    def setAlienCooldown(self, count):
        """
        Setter for alienCooldown attribute

        Parameter: count indicates number of steps aliens must move before
        firing again
        Precondition: count is an int >= 0
        """
        assert type(count) == int
        assert count >= 0
        self.alienCooldown = count #ADD MORE ATTRIBUTES

    def getRightmost(self):
        """
        Getter for rightmost attribute
        Returns right-most x coordinate the aliens reach
        """
        return self.rightmost #ADD MORE ATTRIBUTES

    def setRightmost(self, rightmost):
        """
        Setter for rightmost attribute

        Parameter: rightmost indicates right-most x coordinate the aliens reach
        Precondition: rightmost is an int or float >= 0 and <= GAME_WIDTH
        """
        assert type(rightmost) == int or type(rightmost) == float
        assert rightmost >= 0 and rightmost <= GAME_WIDTH
        self.rightmost = rightmost #ADD MORE ATTRIBUTES

    def getLeftmost(self):
        """
        Getter for leftmost attribute
        Returns left-most x coordinate the aliens reach
        """
        return self.leftmost #ADD MORE ATTRIBUTES

    def setLeftmost(self, leftmost):
        """
        Setter for leftmost attribute

        Parameter: leftmost indicates left-most x coordinate the aliens reach
        Precondition: leftmost is an int or float >= 0 and <= GAME_WIDTH
        """
        assert type(leftmost) == int or type(leftmost) == float
        assert leftmost >= 0 and leftmost <= GAME_WIDTH
        self.leftmost = leftmost #ADD MORE ATTRIBUTES

    def getShipLives(self):
        """
        Getter for _shiplives attribute
        Returns list of ship objects to indicate ship lives left
        """
        return self._shiplives #ADD MORE ATTRIBUTES

    def setShipLives(self, shiplives):
        """
        Setter for _shiplives attribute

        Parameter: shiplives contains ship objects that indicate ship lives left
        Precondition: shiplives is a list
        """
        assert type(shiplives) == list
        self._shiplives = shiplives #ADD MORE ATTRIBUTES

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializer to create ships and aliens
        """
        self.Alienboltstart()
        self.shoottime = 0
        self.bolton = True
        self.setBolt([])
        self.setRight(True)
        self.setTime(0)
        self.alienInit()
        self.shipInit()
        self.defenseInit()
        self.setRightmost(0)
        self.setLeftmost(GAME_WIDTH)
        self.setLives(SHIP_LIVES)
        self.setPaused(False)
        self.setComplete(False)
        self.setSpeed(ALIEN_SPEED)
        list = []
        #self.setShipLives(list)
        for i in range(3):
            list.append(ShipLives(GAME_WIDTH-92 + \
            (i * 37),GAME_HEIGHT-50, 'ship.png'))
        self.setShipLives(list)
        self.healthbarInit()

    def healthbarInit(self):
        """
        Initializer for health bars of aliens
        """
        self.healthbars = []
        self.healthbarsneg = []
        for i in range(len(self.getAliens())):
            r = []
            p = []
            for j in range(len(self.getAliens()[i])):
                if not self.getAliens()[i][j] is None:
                    x = self.getAliens()[i][j].x
                    y = self.getAliens()[i][j].y
                    health = self.getAliens()[i][j].health
                    r.append(AlienHealthBar(x, y, health))
                    p.append(AlienHealthBarNeg(x, y, health))
            self.healthbars.append(r)
            self.healthbarsneg.append(p)

    def updateHealthbar(self):
        """
        Updates health bars of aliens
        """
        for i in range(len(self.getAliens())):
            for j in range(len(self.getAliens()[i])):
                if not self.getAliens()[i][j] is None:
                    x = self.getAliens()[i][j].x
                    y = self.getAliens()[i][j].y
                    health = self.getAliens()[i][j].health
                    self.healthbars[i][j].updatebar(x, y, health)
                    self.healthbarsneg[i][j].updatebar(x, y, health)

    def alienInit(self):
        """
        Helper function to initialize Alien objects
        """
        self.setAliensteps(0)
        self.setAliens([])
        aliens = []
        for i in range(ALIEN_ROWS):
            row = []
            j = ALIEN_ROWS - i
            if j == 0 and j == 1:
                image = ALIEN_IMAGES[2]
            else:
                if j % (len(ALIEN_IMAGES) * 2) == 1 or j % \
                (len(ALIEN_IMAGES) * 2) == 2:
                    image = ALIEN_IMAGES[0]
                elif j % 6 == 3 or j % 6 == 4:
                    image = ALIEN_IMAGES[1]
                else:
                    image = ALIEN_IMAGES[2]
            for j in range(ALIENS_IN_ROW):
                initialx = ALIEN_H_SEP + 0.5 * ALIEN_WIDTH
                initialy = GAME_HEIGHT - ALIEN_CEILING - 0.5 * ALIEN_HEIGHT
                xpos = initialx + j*(ALIEN_H_SEP + ALIEN_WIDTH)
                ypos = initialy - i*(ALIEN_V_SEP + ALIEN_HEIGHT)
                row.append(Alien(xpos, ypos, image))
            aliens.append(row)
        self.setAliens(aliens)

    def shipInit(self):
        """
        Helper function to initialize Ship object
        """
        initialx = GAME_WIDTH / 2
        initialy = SHIP_BOTTOM + SHIP_HEIGHT / 2
        self.setShip(Ship(initialx, initialy, 'ship.png'))

    def defenseInit(self):
        """
        Helper function to initialize defense line object
        """
        line = GPath(points=[0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE], \
        linewidth=2, linecolor=introcs.RGB(100,100,100))
        self.setDefense(line)

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, time):
        """
        Updates Ship, Alien, and Bolt objects with each frame
        """
        self.setTime(self.getTime() + time)
        self.updateShip(input)
        self.updateAliens()
        self.updateBolt()
        self.updateAlienColl()
        self.updateShipColl()
        self.updateAliensAlive()
        self.updateAliensLine()
        self.shoottime = self.shoottime+time
        if self.shoottime >= FIRE_RATE:
            self.bolton = True
        self.updateHealthbar()

    def updateAliensLine(self):
        """
        Helper function to update Alien objects
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if not self.getAliens()[i][j] is None:
                    if self.getAliens()[i][j].y <= DEFENSE_LINE +ALIEN_HEIGHT/2:
                        self.setLives(0)
                        self.setComplete(True)

    def updateAliensAlive(self):
        """
        Helper function to update Alien lives
        """
        p = 0
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if not self.getAliens()[i][j] is None:
                    p = p + 1
        if p == 0:
            self.setShip(None)
            self.setComplete(True)
        else:
            pass

    def updateAlienColl(self):
        """
        Helper function to update whether aliens have been hit by a laser bolt
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if not self.getAliens()[i][j] is None:
                    for r in range(len(self.getBolt())):
                        if not self.getBolt()[r] is None:
                            if (self.getBolt()[r].getPlayerbolt() == True and
                            self.getAliens()[i][j].collides(self.getBolt()[r])
                            == True):
                                return self.alienhit(i, j, r)

    def updateShipColl(self):
        """
        Helper function to update whether the ship has been hit by a laser bolt
        """
        if not self.getShip() is None:
            for r in range(len(self.getBolt())):
                if not self.getShip() is None:
                    boltpos = None
                    if self.getBolt()[r].getPlayerbolt() == False:
                        boltpos = r
                    if not boltpos is None:
                        if self.getShip().collides(self.getBolt()[boltpos]) \
                        == True:
                            self.setShip(None)
                            del self.getBolt()[boltpos]
                            self.setLives(self.getLives() - 1)
                            if not self.getLives() == 0:
                                self.setPaused(True)
                            else:
                                self.setComplete(True)
                            del self._shiplives[(len(self._shiplives)-1)]
                    else:
                        pass

    def alienhit(self, i, j, r):
        """
        Helper function to update alien health and speed when they are hit
        """
        self.getAliens()[i][j].health = (self.getAliens()[i][j].health -
        random.randint((DAMAGE_LOW), (DAMAGE_HIGH)))
        if self.getAliens()[i][j].health <= 0:
            self.getAliens()[i][j] = None
            self.healthbars[i][j] =None
            self.healthbarsneg[i][j] =None
            self.setSpeed(self.getSpeed()*ALIEN_SPEED_CHANGE)
        del self.getBolt()[r]

    def Alienboltstart(self):
        """
        Method to randomize cooldown before alien bolts
        """
        self.setAlienCooldown(random.randint(1, BOLT_RATE))

    def Alienboltfire(self):
        """
        Helper function to fire alien bolts
        """
        if self.getAliensteps() >= self.getAlienCooldown():
            isempty = []
            for i in range(ALIENS_IN_ROW):
                j = 0
                hasaliens = False
                while j < ALIEN_ROWS or sum  == False:
                    if not self.getAliens()[j][i] is None:
                        hasaliens = True
                    j = j+1
                isempty.append(hasaliens)
            rando = None
            while rando == None:
                r = random.randrange(0, ALIENS_IN_ROW)
                if isempty[r] == True:
                    rando = 1
            y = ALIEN_ROWS-1
            alienselect = self.getAliens()[y][r]
            while alienselect == None:
                alienselect = self.getAliens()[y][r]
                y = y-1
            if not ALIEN_ROWS-1 == y:
                y = y+1
            if not self.getAliens()[y][r] is None:
                p = Bolt(self.getAliens()[y][r].x, self.getAliens()[y][r].y, \
                False, introcs.RGB(255,165,15))
                self.getBolt().append(p)
            self.setAliensteps(0)
            self.Alienboltstart()

    def updateBolt(self):
        """
        Helper function to update Bolt objects
        """
        for i in range(len(self.getBolt())):
            self.getBolt()[i].updatepos()
        j = 0
        while j < len(self.getBolt()):
            if self.getBolt()[j].y >= GAME_HEIGHT or self.getBolt()[j].y <= 0:
                del self.getBolt()[j]
            else:
                j = j+1

    def boltInit(self):
        """
        Initializes Bolt objects
        """
        if not self.getShip() is None:
            if self.bolton == True:
                j = Bolt(self.getShip().x, SHIP_HEIGHT, True, \
                introcs.RGB(140,210,240))
                self.getBolt().append(j)
                self.bolton = False
                self.shoottime = 0

    def updateShip(self, input):
        """
        Helper function to update Ship object placement with each frame
        """
        if not self.getShip() is None:
            leftkey = input.is_key_down('left')
            rightkey = input.is_key_down('right')
            if leftkey and self.getShip().x > SHIP_WIDTH / 2:
                self.getShip().x =(self.getShip().x - SHIP_MOVEMENT)
            if rightkey and self.getShip().x < GAME_WIDTH - SHIP_WIDTH / 2:
                self.getShip().x = (self.getShip().x + SHIP_MOVEMENT)

    def updateAliens(self):
        """
        Helper function to update Alien object placement with each frame
        """
        if self.getTime() >= self.getSpeed():
            self.setTime(self.getTime() % self.getSpeed())
            self.setAliensteps(self.getAliensteps() + 1)
            self.Alienboltfire()
            if (self.getRightmost() > (GAME_WIDTH-(2*ALIEN_H_SEP))) and \
            self.getRight() == True:
                for i in range(ALIEN_ROWS):
                    for j in range(ALIENS_IN_ROW):
                        if not self.getAliens()[i][j] is None:
                            self.getAliens()[i][j].changey()
                self.setRight(False)
                self.setRightmost(0)
                self.setLeftmost(GAME_WIDTH)
            elif (self.getLeftmost() <= (ALIEN_H_SEP*2)) and \
            self.getRight() == False:
                for i in range(ALIEN_ROWS):
                    for j in range(ALIENS_IN_ROW):
                        if not self.getAliens()[i][j] is None:
                            self.getAliens()[i][j].changey()
                self.setRight(True)
                self.setRightmost(0)
                self.setLeftmost(GAME_WIDTH)
            else:
                self.move()

    def move(self):
        """
        Moves Aliens to the right or left based on right attribute, called by updateAliens()
        """
        for i in range(len(self.getAliens())):
            for j in range(len(self.getAliens()[i])):
                if not self.getAliens()[i][j] is None:
                    self.getAliens()[i][j].changex(self.getRight())
                    if self.getAliens()[i][j].x > self.getRightmost():
                        self.setRightmost(self.getAliens()[i][j].x)
                    if self.getAliens()[i][j].x < self.getLeftmost():
                        self.setLeftmost(self.getAliens()[i][j].x)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draw method to draw the ship, aliens, defensive line, and bolts
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if not self.getAliens()[i][j] is None:
                    self.getAliens()[i][j].draw(view)
                if not self.healthbars[i][j] is None:
                    self.healthbars[i][j].draw(view)
                    self.healthbarsneg[i][j].draw(view)
        if not self.getShip() is None:
            self.getShip().draw(view)
        self.getDefense().draw(view)
        if not self.getBolt() == []:
            for i in range(len(self.getBolt())):
                self.getBolt()[i].draw(view)
        for i in range(len(self.getShipLives())):
            self.getShipLives()[i].draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
