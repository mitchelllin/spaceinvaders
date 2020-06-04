"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

# Mitchell Lin ml887 and Alina Kim ak778
# 12/4/18
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        lastkeys:   the number of keys pressed last frame [int >= 0]
    """

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        # asserts preconditions are met
        #assert self.validGameSettings()

        #draws initial welcome screen
        #self._text = GLabel(text="Press 'S' to Play")
        #self._text.draw(self.view)

        # initializing instance variables
        self.setState(STATE_INACTIVE)
        self.setWave(None)
        self.setText(None)
        self.lastkeys = 0 #ADD MORE ATTRIBUTES

        # draws iniital welcome screen
        self.welcomeScreen()

    def welcomeScreen(self):
        """
        Creates the welcome screen

        This method creates a Glabel with the text 'press 'F' to start' when the
        state is STATE_INACTIVE, meaning it will show the text when the player
        first starts the game. It calls draw at the end.
        """
        # creates welcome screen if state is STATE_INACTIVE
        if self.getState() == STATE_INACTIVE:
            label = GLabel(text="press 'F' to start", x = GAME_WIDTH/2,
            y = GAME_HEIGHT/2, font_size = 50, font_name = 'arcade',
            linecolor = introcs.RGB(0,0,0))
            label.halign = 'center'
            label.valign = 'middle'
            self.setText(label)
        # welcome screen is None if state is not STATE_INACTIVE
        else:
            self.setText(None)
        # draws the welcome screen
        #self.getText().x = consts.GAME_WIDTH / 2
        #self.getText().y = consts.GAME_HEIGHT / 2
        self.draw()

    def pausedScreen(self):
        """
        Creates the paused screen

        This method creates a Glabel with the text 'press 'F' to resume' when the
        state is STATE_PAUSED, meaning the text will only show when a ship has
        been destroyed. It calls draw at the end.
        """
        # creates welcome screen if state is STATE_INACTIVE
        if self.getState() == STATE_PAUSED:
            label = GLabel(text="press 'F' to resume", x = GAME_WIDTH/2, y = 50,
            font_size = 50, font_name = 'arcade',linecolor = introcs.RGB(0,0,0))

            label.halign = 'center'
            label.valign = 'middle'
            self.setText(label)
        # welcome screen is None if state is not STATE_INACTIVE
        else:
            self.setText(None)
        # draws the welcome screen
        #self.getText().x = consts.GAME_WIDTH / 2
        #self.getText().y = consts.GAME_HEIGHT / 2
        self.draw()

    def winScreen(self):
        """
        Creates the win screen text

        This method creates a Glabel with the text 'Congratulations! You win!'
        when the state is STATE_COMPLETE, meaning the text will only show when
        the game ends. It calls draw at the end.
        """
        # creates welcome screen if state is STATE_INACTIVE
        if self.getState() == STATE_COMPLETE:
            label = GLabel(text="Congratulations! You win!", x = GAME_WIDTH/2,
            y = 50, font_size = 50, font_name = 'arcade',
            linecolor = introcs.RGB(0,0,0))
            label.halign = 'center'
            label.valign = 'middle'
            self.setText(label)
        # welcome screen is None if state is not STATE_INACTIVE
        else:
            self.setText(None)
        # draws the welcome screen
        #self.getText().x = consts.GAME_WIDTH / 2
        #self.getText().y = consts.GAME_HEIGHT / 2
        self.draw()

    def deathScreen(self):
        """
        Creates the death screen text

        This method creates a Glabel with the text 'You Lose! Get dunked on!'
        when the state is STATE_COMPLETE, meaning the text will only show when
        the game ends. It calls draw at the end.
        """
        # creates welcome screen if state is STATE_INACTIVE
        if self.getState() == STATE_COMPLETE:
            label = GLabel(text="You Lose! Get dunked on!", x = GAME_WIDTH/2,
            y = 50, font_size = 50, font_name = 'arcade',
            linecolor = introcs.RGB(0,0,0))
            label.halign = 'center'
            label.valign = 'middle'
            self.setText(label)
        # welcome screen is None if state is not STATE_INACTIVE
        else:
            self.setText(None)
        # draws the welcome screen
        #self.getText().x = consts.GAME_WIDTH / 2
        #self.getText().y = consts.GAME_HEIGHT / 2
        self.draw()

    def livesScreen(self):
        """
        Creates the lives text

        This method creates a Glabel with the text 'Lives:'
        when the state is STATE_ACTIVE or STATE_PAUSED, meaning the text will
        only show when the game is being played. It calls draw at the end.
        """
        # creates welcome screen if state is STATE_INACTIVE
        if self.getState() == STATE_ACTIVE or self.getState() == STATE_PAUSED \
        or self.getState() == STATE_COMPLETE:
            label = GLabel(text="Lives:", x = GAME_WIDTH-150,
            y = GAME_HEIGHT-55, font_size = 30, font_name = 'arcade',
            linecolor = introcs.RGB(0,0,0))
            label.halign = 'center'
            label.valign = 'middle'
            self.setText(label)
        # welcome screen is None if state is not STATE_INACTIVE
        else:
            self.setText(None)
        # draws the welcome screen
        #self.getText().x = consts.GAME_WIDTH / 2
        #self.getText().y = consts.GAME_HEIGHT / 2
        self.draw()

    def getState(self):
        """
        Getter for _state attribute
        """
        return self._state

    def setState(self, state):
        """
        Setter for _state attribute
        """
        assert self.isValidState(state)
        self._state = state

    def isValidState(self, state):
        """
        Tests whether state is valid
        """
        validStates = [STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
        STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        if not state in validStates:
            return False
        else:
            return True

    def getWave(self):
        """
        Getter for _wave attribute
        """
        return self._wave

    def setWave(self, wave):
        """
        Setter for _wave attribute
        """
        assert self.isWave(wave)
        self._wave = wave

    def isWave(self, wave):
        """
        Tests whether wave is valid
        """
        if wave is None or isinstance(wave, Wave):
            return True
        return False

    def getText(self):
        """
        Getter for _text attribute
        """
        return self._text

    def setText(self, text):
        """
        Setter for _text attribute
        """
        assert self.isLabel(text)
        self._text = text

    def isLabel(self, text):
        """
        Tests whether label is valid
        """
        if text is None or isinstance(text, GLabel):
            return True
        return False

    def validGameSettings(self):
        """
        Helper method to test whether instance attributes are valid for game
        initialization

        Returns True if all attributes are valid, False otherwise
        """
        if not isinstance(self.view, GView):
            return False
        if not isinstance(self.input, GInput):
            return False
        validStates = [STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
        STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        if not self.getState() in validStates:
            return False
        if not self.getWave() is None or isinstance(self.getWave(), Wave):
            return False
        if not self.getText() is None or isinstance(self.getText(), GLabel):
            return False
        return True

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        assert type(dt) == int or type(dt) == float

        # allows user to dismiss welcome screen
        if (self.getState() == STATE_INACTIVE):
            self.updateInactive()

        if self.getState() == STATE_NEWWAVE:
            self.updateNewWave()

        if not self.getWave() is None:
            if self.getWave().getPaused() == True:
                self.setState(STATE_PAUSED)
            if self.getWave().getComplete() == True:
                self.setState(STATE_COMPLETE)

        if self.getState() == STATE_PAUSED:
            self.updatePaused()

        if self.getState() == STATE_ACTIVE:
            self.updateActive(dt)

        if self.getState() == STATE_COMPLETE:
            self.updateComplete()

    def updateInactive(self):
        """
        Helper function to update when state is STATE_INACTIVE
        """
        change = self.input.key_count > 0 and self.lastkeys == 0 #ADD MORE ATTRIBUTES
        if change:
            keyPressed = self.input.is_key_down('f') or \
            self.input.is_key_down('F')
            if keyPressed:
                self.setState(STATE_NEWWAVE)
                self.welcomeScreen()
        self.lastkeys == self.input.key_count #ADD MORE ATTRIBUTES

    def updateNewWave(self):
        """
        Helper function to update when state is STATE_NEWWAVE
        """
        self.setWave(Wave())
        self.setState(STATE_ACTIVE)

    def updatePaused(self):
        """
        Helper function to update when state is STATE_PAUSED
        """
        self.pausedScreen()
        change = self.input.key_count > 0 and self.lastkeys == 0 #ADD MORE ATTRIBUTES
        if change:
            keyPressed = self.input.is_key_down('f') or \
            self.input.is_key_down('F')
            if keyPressed: #ADD MORE ATTRIBUTES
                self.setState(STATE_ACTIVE)
                self.getWave().setPaused(False)
                self.getWave().shipInit()
        self.lastkeys == self.input.key_count #ADD MORE ATTRIBUTES
        self.livesScreen()

    def updateActive(self, dt):
        """
        Helper function to update when state is STATE_ACTIVE
        """
        self.getWave().update(self.input, dt)
        self.boltshoot()
        self.livesScreen()

    def updateComplete(self):
        """
        Helper function to update when state is STATE_COMPLETE
        """
        self.livesScreen()
        if self.getWave().getLives() == 0:
            self.deathScreen()
        else:
            self.winScreen()

    def boltshoot(self):
        """
        Checks when the player shoots

        When spacebar is pressed, boltInit() in Wave will be called, causing the
        palyer to shoot a bolt
        """
        if self.input.is_key_down('spacebar'):
            self.getWave().boltInit()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        # IMPLEMENT ME
        """
        GRectangle(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
        width=GAME_WIDTH,height=GAME_HEIGHT,
        fillcolor=introcs.RGB(0,0,0)).draw(self.view)
        if self.getState() == STATE_INACTIVE:
            self.getText().draw(self.view)
        if self.getState() == STATE_PAUSED:
            self.getText().draw(self.view)
        if not self.getWave() is None:
            self.getWave().draw(self.view)
        if self.getState() == STATE_COMPLETE:
            self.getText().draw(self.view)
        if self.getState() == STATE_PAUSED or self.getState() == STATE_ACTIVE or self.getState() == STATE_COMPLETE:
            self.getText().draw(self.view)

        GRectangle(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
        width=GAME_WIDTH,height=GAME_HEIGHT,
        fillcolor=introcs.RGB(0,0,0)).draw(self.view)"""
        if not self.getText() is None:
            self.getText().draw(self.view)
        if not self.getWave() is None:
            self.getWave().draw(self.view)




    # HELPER METHODS FOR THE STATES GO HERE
