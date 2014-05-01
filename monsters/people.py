import base
import stats
import items
import dialogue
import context
import spells
import invocations
import effects
import animobs
import targetarea
import aibrain
import random
import animals
import undead

#  *******************************
#  ***   ENCOUNTER  LEVEL  1   ***
#  *******************************

class Hurthling( base.Monster ):
    name = "Hurthling"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 8, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 10,
        stats.NATURAL_DEFENSE: 5 }
    SPRITENAME = "monster_people.png"
    FRAME = 5
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.HURTHISH
    GP_VALUE = 5
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_THIEF )
    ENC_LEVEL = 1

    ATTACK = items.Attack( (1,4,0), element = stats.RESIST_PIERCING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 1, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  2   ***
#  *******************************

class NoviceWarrior( base.Monster ):
    name = "Novice Warrior"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 10 }
    SPRITENAME = "monster_people.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.HURTHISH
    GP_VALUE = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED,
     context.MTY_HUMANOID, context.MTY_FIGHTER )
    ENC_LEVEL = 2

    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )


#  *******************************
#  ***   ENCOUNTER  LEVEL  3   ***
#  *******************************

class NovicePriest( base.Monster ):
    name = "Novice Priest"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 13, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 13, stats.PIETY: 15, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 10
    GP_VALUE = 15
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_SOLAR,
     context.MTY_HUMANOID, context.MTY_PRIEST )
    ENC_LEVEL = 3
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (NoviceWarrior,)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.waterspells.FREEZE_FOE, spells.airspells.SILENCE,
        spells.airspells.SHOUT, spells.solarspells.MINOR_CURE )
    TREASURE = ( items.scrolls.Rank1Scroll, items.scrolls.Rank2Scroll )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )
        if random.randint(1,10) == 1:
            self.contents.append( random.choice( self.TREASURE )() )

class NoviceMage( base.Monster ):
    name = "Novice Mage"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 10, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 15, stats.PIETY: 13, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 21
    TEMPLATES = ()
    MOVE_POINTS = 10
    GP_VALUE = 15
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_MAGE )
    ENC_LEVEL = 3
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (NovicePriest,NoviceWarrior)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.firespells.FIRE_BOLT, spells.magespells.LIGHTNING_BOLT,
        spells.magespells.FIRE_ARC, spells.lunarspells.SLEEP )
    TREASURE = ( items.scrolls.Rank1Scroll, items.scrolls.Rank2Scroll )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 3, self ) )
        if random.randint(1,10) == 1:
            self.contents.append( random.choice( self.TREASURE )() )



#  *******************************
#  ***   ENCOUNTER  LEVEL  4   ***
#  *******************************

class NoviceDruid( base.Monster ):
    name = "Novice Druid"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 13, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 14, stats.PIETY: 14, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 8
    TEMPLATES = ()
    MOVE_POINTS = 10
    GP_VALUE = 20
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_SOLAR, context.DES_EARTH, context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_PRIEST, context.GEN_NATURE )
    ENC_LEVEL = 4
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (animals.Wolf,animals.BlackBear)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.solarspells.MINOR_CURE, spells.firespells.BLINDING_FLASH,
        spells.earthspells.ACID_BOLT )
    TREASURE = ( items.scrolls.Rank1Scroll, items.scrolls.Rank2Scroll )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )
        self.levels.append( base.Spellcaster( 2, self ) )
        if random.randint(1,10) == 1:
            self.contents.append( random.choice( self.TREASURE )() )


#  *******************************
#  ***   ENCOUNTER  LEVEL  5   ***
#  *******************************

class Necromancer( base.Monster ):
    name = "Necromancer"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 15, stats.PIETY: 13, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 23
    TEMPLATES = ()
    MOVE_POINTS = 10
    GP_VALUE = 25
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_MAGE, context.GEN_UNDEAD )
    ENC_LEVEL = 5
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (undead.Ghoul,undead.SkeletonWithMorningstar)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.lunarspells.SLEEP, spells.necrospells.ACID_CLOUD,
        spells.necrospells.TOUCH_OF_DEATH, spells.waterspells.WINTER_WIND )
    TREASURE = ( items.scrolls.Rank2Scroll, items.scrolls.Rank3Scroll )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 5, self ) )
        if random.randint(1,10) == 1:
            self.contents.append( random.choice( self.TREASURE )() )

#  *******************************
#  ***   ENCOUNTER  LEVEL  6   ***
#  *******************************

class Priest( base.Monster ):
    name = "Priest"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 14, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 13, stats.PIETY: 16, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 10
    GP_VALUE = 30
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_SOLAR,
     context.MTY_HUMANOID, context.MTY_PRIEST )
    ENC_LEVEL = 6
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (NoviceWarrior,NovicePriest)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.waterspells.FREEZE_FOE, spells.airspells.SILENCE,
        spells.priestspells.HEALING_LIGHT, spells.solarspells.SUNRAY,
        spells.waterspells.REGENERATION, spells.airspells.THUNDER_STRIKE )
    TREASURE = ( items.scrolls.Rank2Scroll, items.scrolls.Rank3Scroll )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )
        if random.randint(1,10) == 1:
            self.contents.append( random.choice( self.TREASURE )() )


#  *******************************
#  ***   ENCOUNTER  LEVEL  7   ***
#  *******************************

class Conjuoror( base.Monster ):
    name = "Conjuoror"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 16, stats.PIETY: 14, stats.CHARISMA: 12 }
    SPRITENAME = "monster_spellcasters.png"
    FRAME = 10
    TEMPLATES = ()
    MOVE_POINTS = 10
    GP_VALUE = 35
    HABITAT = ( context.HAB_EVERY, context.HAB_BUILDING, context.SET_EVERY,
     context.DES_CIVILIZED, context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_MAGE )
    ENC_LEVEL = 7
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (NovicePriest,NoviceWarrior)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.magespells.LIGHTNING_BOLT, spells.lunarspells.SLEEP,
        spells.lunarspells.HELLBLAST, spells.firespells.EXPLOSION,
        spells.firespells.PYROTECHNICS
         )
    TREASURE = ( items.scrolls.Rank3Scroll, items.scrolls.Rank4Scroll )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 7, self ) )
        if random.randint(1,10) == 1:
            self.contents.append( random.choice( self.TREASURE )() )


#  *******************************
#  ***   ENCOUNTER  LEVEL  8   ***
#  *******************************


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

