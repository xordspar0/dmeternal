import base
import stats
import items
import dialogue
import context

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************

class GiantBat( base.Monster ):
    name = "Giant Bat"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 6, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 1, stats.PIETY: 9, stats.CHARISMA: 8 }
    SPRITENAME = "monster_animals.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.DES_LUNAR, context.MTY_BEAST, \
     context.GEN_NATURE )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )

class GiantRat( base.Monster ):
    name = "Giant Rat"
    statline = { stats.STRENGTH: 8, stats.TOUGHNESS: 8, stats.REFLEXES: 15, \
        stats.INTELLIGENCE: 4, stats.PIETY: 9, stats.CHARISMA: 3 }
    SPRITENAME = "monster_animals.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.DES_LUNAR, context.MTY_BEAST, \
     context.GEN_NATURE )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )

class DireNewt( base.Monster ):
    name = "Dire Newt"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 9, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 1, stats.PIETY: 2, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 5
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 8
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.DES_WATER, context.MTY_BEAST, \
     context.GEN_NATURE )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 1, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

class MadDog( base.Monster ):
    name = "Mad Dog"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 8, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 9, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 7
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_EVERY, context.MTY_BEAST, context.GEN_CHAOS )
    ENC_LEVEL = 2

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )

class CaveAnt( base.Monster ):
    name = "Cave Ant"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 1, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 9
    TEMPLATES = (stats.BUG,)
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.DES_EARTH, context.MTY_BEAST, \
     context.GEN_NATURE )
    ENC_LEVEL = 2

    ATTACK = items.Attack( (1,6,1), element = stats.RESIST_ACID )

    def init_monster( self ):
        self.levels.append( base.Beast( 2, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

class Wolf( base.Monster ):
    name = "Wolf"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 4, stats.PIETY: 11, stats.CHARISMA: 12 }
    SPRITENAME = "monster_animals.png"
    FRAME = 11
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 3

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )

class GiantFrog( base.Monster ):
    name = "Giant Frog"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 15, stats.REFLEXES: 11, \
        stats.INTELLIGENCE: 1, stats.PIETY: 5, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 13
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_CAVE, context.DES_WATER, context.MTY_BEAST, \
     context.GEN_NATURE )
    ENC_LEVEL = 3

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 3, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

class BlackBear( base.Monster ):
    name = "Black Bear"
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 16, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 3, stats.PIETY: 8, stats.CHARISMA: 6 }
    SPRITENAME = "monster_animals.png"
    FRAME = 14
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 4

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )

    def init_monster( self ):
        self.levels.append( base.Beast( 4, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class DireWolf( base.Monster ):
    name = "Dire Wolf"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 13, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 5, stats.PIETY: 9, stats.CHARISMA: 12 }
    SPRITENAME = "monster_animals.png"
    FRAME = 12
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.MTY_BEAST, context.GEN_NATURE, \
     context.GEN_GOBLIN )
    ENC_LEVEL = 5

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 5, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

class Lion( base.Monster ):
    name = "Lion"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 10, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 3, stats.PIETY: 10, stats.CHARISMA: 9 }
    SPRITENAME = "monster_animals.png"
    FRAME = 17
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.DES_SOLAR, context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 6

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )

    def init_monster( self ):
        self.levels.append( base.Beast( 6, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

class GrizzlyBear( base.Monster ):
    name = "Grizzly Bear"
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 18, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 3, stats.PIETY: 8, stats.CHARISMA: 6 }
    SPRITENAME = "monster_animals.png"
    FRAME = 15
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 7

    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )

    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )

class GiantEagle( base.Monster ):
    name = "Giant Eagle"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 12, stats.PIETY: 14, stats.CHARISMA: 13 }
    SPRITENAME = "monster_animals.png"
    FRAME = 21
    TEMPLATES = ()
    MOVE_POINTS = 16
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.MTY_BEAST, context.GEN_NATURE,
     context.DES_AIR, context.DES_SOLAR )
    ENC_LEVEL = 7

    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 7, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************

class GreatStag( base.Monster ):
    name = "Great Stag"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 15, stats.REFLEXES: 17, \
        stats.INTELLIGENCE: 3, stats.PIETY: 19, stats.CHARISMA: 16 }
    SPRITENAME = "monster_animals.png"
    FRAME = 20
    TEMPLATES = ()
    MOVE_POINTS = 14
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.HAB_FOREST, context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 8

    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 8, self ) )

class Crocodile( base.Monster ):
    name = "Crocodile"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 18, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 1, stats.PIETY: 10, stats.CHARISMA: 1 }
    SPRITENAME = "monster_animals.png"
    FRAME = 24
    TEMPLATES = (stats.REPTILE,)
    MOVE_POINTS = 8
    VOICE = None
    GP_VALUE = 0
    HABITAT = ( context.DES_WATER, context.MTY_BEAST, context.GEN_NATURE )
    ENC_LEVEL = 8

    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Beast( 9, self ) )

#  *******************************
#  ***   ENCOUNTER  LEVEL  9   ***
#  *******************************


#  ********************************
#  ***   ENCOUNTER  LEVEL  10   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  11   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  12   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  13   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  14   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  15   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  16   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  17   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  18   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  19   ***
#  ********************************

#  ********************************
#  ***   ENCOUNTER  LEVEL  20   ***
#  ********************************

