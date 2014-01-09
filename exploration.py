import maps
import pfov
import pygwrap
import pygame
import hotmaps
import charsheet
import items
import dialogue
import animobs
import characters
import random
import teams
import combat
import stats


# Commands should be callable objects which take the explorer and return a value.
# If untrue, the command stops.

class MoveTo( object ):
    """A command for moving to a particular point."""
    def __init__( self, scene, pos ):
        """Move the party to pos."""
        self.dest = pos
        self.tries = 300
        self.hmap = hotmaps.PointMap( scene, pos )

    def is_later_model( self, party, pc, npc ):
        return ( pc in party ) and ( npc in party ) \
            and party.index( pc ) < party.index( npc )

    def smart_downhill_dir( self, exp, pc ):
        """Return the best direction for the PC to move in."""
        best_d = None
        random.shuffle( self.hmap.DELTA8 )
        heat = self.hmap.map[pc.pos[0]][pc.pos[1]]
        for d in self.hmap.DELTA8:
            x2 = d[0] + pc.pos[0]
            y2 = d[1] + pc.pos[1]
            if exp.scene.on_the_map(x2,y2) and ( self.hmap.map[x2][y2] < heat ):
                target = exp.scene.get_character_at_spot( (x2,y2) )
                if not target:
                    heat = self.hmap.map[x2][y2]
                    best_d = d
                elif ( x2 == self.dest[0] ) and ( y2 == self.dest[1] ):
                    heat = 0
                    best_d = d
                elif self.is_later_model( exp.camp.party, pc, target ):
                    heat = self.hmap.map[x2][y2]
                    best_d = d
        return best_d


    def __call__( self, exp ):
        pc = exp.camp.first_living_pc()
        self.tries += -1
        if (not pc) or ( self.dest == pc.pos ) or ( self.tries < 1 ) or not exp.scene.on_the_map( *self.dest ):
            return False
        else:
            first = True
            keep_going = True
            tiles_in_sight = set()
            for pc in exp.camp.party:
                if pc.is_alright() and exp.scene.on_the_map( *pc.pos ):
                    d = self.smart_downhill_dir( exp, pc )
                    if d:
                        p2 = ( pc.pos[0] + d[0] , pc.pos[1] + d[1] )
                        target = exp.scene.get_character_at_spot( p2 )

                        if exp.scene.map[p2[0]][p2[1]].blocks_walking():
                            # There's an obstacle in the way.
                            if first:
                                exp.bump_tile( p2 )
                                keep_going = False
                        elif ( not target ) or self.is_later_model( exp.camp.party, pc, target ):
                            if target:
                                target.pos = pc.pos
                            pc.pos = p2
                            pcview = exp.scene.update_pc_position( pc )
                            tiles_in_sight.update( pcview.tiles )
                        elif first:
                            exp.bump_model( target )
                            keep_going = False
                    elif first:
                        keep_going = False
                    first = False
            # Now that all of the pcs have moved, check the tiles_in_sight for
            # hidden models.
            awareness = exp.camp.party_stat( stats.AWARENESS, stats.INTELLIGENCE )
            for m in exp.scene.contents:
                if isinstance( m, characters.Character ) and m.hidden and m.pos in tiles_in_sight and \
                  awareness > m.get_stat( stats.STEALTH ) + m.get_stat_bonus(stats.REFLEXES):
                    m.hidden = False

            return keep_going

class InvExchange( object ):
    # The party will exchange inventory with a list.
    def __init__( self, party, ilist, predraw, caption="/ to switch menus" ):
        self.party = []
        for p in party:
            if p.is_alright():
                self.party.append( p )
        self.predraw = predraw
        self.ilist = ilist
        self.caption = caption

    def __call__( self, screen ):
        """Perform the required inventory exchanges."""
        pcn = 0
        use_left_menu = False
        myredraw = charsheet.InvExchangeRedrawer( screen=screen, caption=self.caption, predraw=self.predraw )
        keep_going = True

        while keep_going:
            lmenu = charsheet.LeftMenu( screen )
            rmenu = charsheet.RightMenu( screen )
            pc = self.party[ pcn ]

            myredraw.menu = rmenu
            myredraw.pc = pc
            if use_left_menu:
                myredraw.off_menu = rmenu
            else:
                myredraw.off_menu = lmenu

            lmenu.predraw = myredraw
            lmenu.quick_keys[ pygame.K_LEFT ] = -1
            lmenu.quick_keys[ pygame.K_RIGHT ] = 1
            lmenu.quick_keys[ "/" ] = 2

            rmenu.predraw = myredraw
            rmenu.quick_keys[ pygame.K_LEFT ] = -1
            rmenu.quick_keys[ pygame.K_RIGHT ] = 1
            rmenu.quick_keys[ "/" ] = 2

            for it in pc.inventory:
                lmenu.add_item( str( it ), it )
            for it in self.ilist:
                rmenu.add_item( str( it ), it )
            lmenu.sort()
            rmenu.sort()
            lmenu.add_alpha_keys()
            rmenu.add_alpha_keys()
            lmenu.add_item( "Cancel", False )
            rmenu.add_item( "Cancel", False )

            if use_left_menu:
                it = lmenu.query()
            else:
                it = rmenu.query()

            if it is -1:
                pcn = ( pcn + len( self.party ) - 1 ) % len( self.party )
            elif it is 1:
                pcn = ( pcn + 1 ) % len( self.party )
            elif it is 2:
                use_left_menu = not use_left_menu
            elif it:
                # An item was selected. Transfer.
                if use_left_menu:
                    pc.inventory.unequip( it )
                    if not it.equipped:
                        pc.inventory.remove( it )
                        self.ilist.append( it )
                elif pc.can_take_item( it ) and pc.is_alright():
                    self.ilist.remove( it )
                    pc.inventory.append( it )
            else:
                keep_going = False
        return self.ilist

# Rubicon Hiscock had her entire body tattooed by a cloister of Gothic monks, and in this way she became illuminated.

class Explorer( object ):
    # The object which is exploration of a scene. OO just got existential.

    def __init__( self, screen, camp ):
        self.screen = screen
        self.camp = camp
        self.scene = camp.scene
        self.view = maps.SceneView( camp.scene )
        self.time = 0

        # Update the view of all party members.
        for pc in camp.party:
            x,y = pc.pos
            pfov.PCPointOfView( camp.scene, x, y, 15 )

        # Hide any monsters who can manage it.
        for m in self.scene.contents:
            if isinstance( m, characters.Character ) and m.can_use_stealth() and m.is_hostile( camp ):
                m.hidden = True

        # Focus on the first PC.
        x,y = camp.first_living_pc().pos
        self.view.focus( screen, x, y )

    def invoke_effect( self, effect, originator, area_of_effect, opening_anim = None, delay_point=None ):
        all_anims = list()
        if opening_anim:
            all_anims.append( opening_anim )
            anims = opening_anim.children
        else:
            anims = all_anims
        delay = 1
        for p in area_of_effect:
            if delay_point:
                delay = self.scene.distance( p, delay_point ) * 2 + 1
            effect( self.camp, originator, p, anims, delay )
        animobs.handle_anim_sequence( self.screen, self.view, all_anims )

        # Remove dead models from the map.
        for m in self.scene.contents[:]:
            if isinstance( m, characters.Character ) and not m.is_alright():
                self.scene.contents.remove( m )
                # Drop all held items.
                for i in m.inventory[:]:
                    m.inventory.remove(i)
                    i.pos = m.pos
                    i.equipped = False
                    self.scene.contents.append( i )

    def invoke_enchantments( self, chara ):
        """If this character has any effect enchantments, handle them."""
        aoe = chara.pos
        for enc in chara.condition:
            if enc.fx:
                self.invoke_effect( enc.fx, chara, aoe )
                if not chara.is_alright():
                    break

    def alert( self, txt ):
        mydest = pygame.Rect( self.screen.get_width() // 2 - 200, self.screen.get_height()//2 - 100, 400, 200 )
        mytext = pygwrap.render_text( pygwrap.SMALLFONT, txt, 400 )
        mydest = mytext.get_rect( center = (self.screen.get_width() // 2, self.screen.get_height()//2) )

        while True:
            ev = pygame.event.wait()
            if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
                break
            elif ev.type == pygwrap.TIMEREVENT:
                self.view( self.screen )
                pygwrap.default_border.render( self.screen, mydest )
                self.screen.blit( mytext, mydest )
                pygame.display.flip()

    def bump_tile( self, pos ):
        pass

    def bump_model( self, target ):
        # Do the animation first.
        pc = self.camp.party_spokesperson()

        anims = [ animobs.SpeakHello(pos=pc.pos), animobs.SpeakHello(pos=target.pos)]
        animobs.handle_anim_sequence( self.screen, self.view, anims )

        offers = [ dialogue.O1, dialogue.O2 ]
        convo = dialogue.build_conversation( dialogue.CUE_HELLO , offers )
        dialogue.converse( self, pc, target, convo )

    def pick_up( self, loc ):
        """Party will pick up items at this location."""
        ilist = []
        for it in self.scene.contents[:]:
            if isinstance( it , items.Item ) and ( it.pos == loc ):
                self.scene.contents.remove( it )
                ilist.append( it )
        if ilist:
            ie = InvExchange( self.camp.party, ilist, self.view )
            ilist = ie( self.screen )
            for it in ilist:
                it.pos = loc
                self.scene.contents.append( it )
            self.view.regenerate_avatars( self.camp.party )

    def equip_item( self, it, pc, redraw ):
        pc.inventory.equip( it )

    def unequip_item( self, it, pc, redraw ):
        pc.inventory.unequip( it )

    def drop_item( self, it, pc, redraw ):
        pc.inventory.unequip( it )
        if not it.equipped:
            pc.inventory.remove( it )
            it.pos = pc.pos
            self.scene.contents.append( it )

    def trade_item( self, it, pc, redraw ):
        """Trade this item to another character."""
        mymenu = charsheet.RightMenu( self.screen, predraw = redraw )
        for opc in self.camp.party:
            if opc != pc and opc.is_alright():
                mymenu.add_item( str( opc ) , opc )
        mymenu.add_item( "Cancel" , False )
        mymenu.add_alpha_keys()

        opc = mymenu.query()
        if opc:
            pc.inventory.unequip( it )
            if not it.equipped:
                if opc.can_take_item( it ):
                    pc.inventory.remove( it )
                    opc.inventory.append( it )
                else:
                    self.alert( "{0} can't carry any more.".format( str( opc ) ) )


    def equip_or_whatevs( self, it, pc, myredraw ):
        """Equip, trade, drop, or whatever this item."""
        mymenu = charsheet.RightMenu( self.screen, predraw = myredraw )
        if it.equipped:
            mymenu.add_item( "Unequip Item", self.unequip_item )
        elif pc.can_equip( it ):
            mymenu.add_item( "Equip Item", self.equip_item )
        mymenu.add_item( "Trade Item", self.trade_item )
        mymenu.add_item( "Drop Item", self.drop_item )
        mymenu.add_item( "Exit", False )
        mymenu.add_alpha_keys()

        n = mymenu.query()

        if n:
            n( it, pc, myredraw )
            myredraw.csheet.regenerate_avatar()
            self.view.regenerate_avatars( self.camp.party )


    def view_party( self, n, can_switch=True ):
        if n >= len( self.camp.party ):
            n = 0
        pc = self.camp.party[ n ]
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=charsheet.CharacterSheet(pc, screen=self.screen, camp=self.camp), screen=self.screen, predraw=self.view, caption="View Party" )

        while keep_going:
            mymenu = charsheet.RightMenu( self.screen, predraw = myredraw )
            for i in pc.inventory:
                if i.equipped:
                    mymenu.add_item( "*" + str( i ) , i )
                else:
                    mymenu.add_item( str( i ) , i )
            mymenu.sort()
            mymenu.add_alpha_keys()
            mymenu.add_item( "Exit", False )
            myredraw.menu = mymenu
            if can_switch:
                mymenu.quick_keys[ pygame.K_LEFT ] = -1
                mymenu.quick_keys[ pygame.K_RIGHT ] = 1

            it = mymenu.query()
            if it is -1:
                n = ( n + len( self.camp.party ) - 1 ) % len( self.camp.party )
                pc = self.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=self.screen, camp=self.camp)
            elif it is 1:
                n = ( n + 1 ) % len( self.camp.party )
                pc = self.camp.party[n]
                myredraw.csheet = charsheet.CharacterSheet(pc, screen=self.screen, camp=self.camp)

            elif it:
                # An item was selected. Deal with it.
                self.equip_or_whatevs( it, pc, myredraw )

            else:
                keep_going = False

    def monster_inactive( self, mon ):
        return mon not in self.camp.party and (( not self.camp.fight ) or mon not in self.camp.fight.active)

    def update_monsters( self ):
        for m in self.scene.contents:
            if isinstance( m, characters.Character ) and self.monster_inactive(m):
                # First handle movement.
                if m.get_move() and ( ((self.time + hash(m)) % 35 == 1 ) or self.camp.fight ):
                    rdel = random.choice( self.scene.DELTA8 )
                    nupos = ( m.pos[0] + rdel[0], m.pos[1] + rdel[1] )

                    if self.scene.on_the_map(nupos[0],nupos[1]) and not self.scene.map[nupos[0]][nupos[1]].blocks_walking() and not self.scene.get_character_at_spot(nupos):
                        if m.team and m.team.home:
                            if m.team.home.collidepoint( nupos ):
                                m.pos = nupos
                        else:
                            m.pos = nupos

                    # Monsters that can hide may hide.
                    if m.can_use_stealth() and m.is_hostile( self.camp ) and random.randint(1,6) == 1:
                        m.hidden = True

                # Next, check visibility to PC.
                if m.team and m.team.on_guard():
                    pov = pfov.PointOfView( self.scene, m.pos[0], m.pos[1], 5 )
                    in_sight = False
                    for pc in self.camp.party:
                        if pc.pos in pov.tiles and pc in self.scene.contents:
                            in_sight = True
                            break
                    if in_sight:
                        react = m.get_reaction( self.camp )
                        if react < teams.FRIENDLY_THRESHOLD:
                            if react < teams.ENEMY_THRESHOLD:
                                anims = [ animobs.SpeakAttack(m.pos,loop=16), ]
                                animobs.handle_anim_sequence( self.screen, self.view, anims )
                                self.camp.activate_monster( m )
                                break
                            else:
                                anims = [ animobs.SpeakAngry(m.pos,loop=16), ]
                                animobs.handle_anim_sequence( self.screen, self.view, anims )

    def keep_exploring( self ):
        return self.camp.first_living_pc() and self.no_quit and not pygwrap.GOT_QUIT

    def go( self ):
        self.no_quit = True
        self.order = None

        # Do one view first, just to prep the model map and mouse tile.
        self.view( self.screen )
        pygame.display.flip()

        while self.keep_exploring():
            if self.camp.fight:
                self.order = None
                self.camp.fight.go( self )
                if pygwrap.GOT_QUIT or not self.camp.fight.no_quit:
                    self.no_quit = False
                    break
                self.camp.fight = None

            # Get input and process it.
            gdi = pygwrap.wait_event()

            if gdi.type == pygwrap.TIMEREVENT:
                self.view( self.screen )
                pygame.display.flip()

                self.time += 1

                if self.order:
                    if not self.order( self ):
                        self.order = None

                self.update_monsters()

            elif not self.order:
                # Set the mouse cursor on the map.
                self.view.overlays.clear()
                self.view.overlays[ self.view.mouse_tile ] = maps.OVERLAY_CURSOR

                if gdi.type == pygame.KEYDOWN:
                    if gdi.unicode == u"1":
                        self.view_party(0)
                    elif gdi.unicode == u"2":
                        self.view_party(1)
                    elif gdi.unicode == u"3":
                        self.view_party(2)
                    elif gdi.unicode == u"4":
                        self.view_party(3)
                    elif gdi.unicode == u"Q":
                        self.no_quit = False
                    elif gdi.unicode == u"a":
                        self.alert( "This is a test of the alert system. Let me know how it turns out." )
                    elif gdi.unicode == u"c":
                        self.view.focus( self.screen, *self.camp.first_living_pc().pos )

                elif gdi.type == pygame.QUIT:
                    self.no_quit = False
                elif gdi.type == pygame.MOUSEBUTTONUP:
                    if gdi.button == 1:
                        # Left mouse button.
                        if ( self.view.mouse_tile != self.camp.first_living_pc().pos ) and self.scene.on_the_map( *self.view.mouse_tile ):
                            self.order = MoveTo( self.scene, self.view.mouse_tile )
                            self.view.overlays.clear()
                        else:
                            self.pick_up( self.view.mouse_tile )
                    else:
                        # If YouTube comments were as good as these comments, we'd all have ponies by now.
                        animobpos = self.view.mouse_tile
#                        ao_pro = animobs.GreenSpray(self.camp.first_living_pc().pos,self.view.mouse_tile )
#                        anims = [ ao_pro, ]
#
#                        area = pfov.PointOfView( self.scene, animobpos[0], animobpos[1], 5 )
#                        for a in area.tiles:
#                            ao = animobs.GreenCloud( pos=a, delay=self.scene.distance(a,animobpos ) * 2 + 1 )
#                            ao.y_off = -25 + 5 * ( abs( a[0]-animobpos[0] ) + abs( a[1]-animobpos[1] ) )
#                            ao_pro.children.append( ao )
#                        for a in self.scene.contents:
#                            if a.pos in area.tiles:
#                                ao = animobs.Caption( str(random.randint(5,27)), a.pos, delay=self.scene.distance(a.pos,animobpos ) * 2 + 1 )
#                                ao = animobs.Caption( "Aiee!", a.pos )
#                                ao_pro.children.append( ao )
#
#                        animobs.handle_anim_sequence( self.screen, self.view, anims )

                        animobpos = self.view.mouse_tile
                        pcpos = self.camp.first_living_pc().pos
                        anims = list()

#                        area = pfov.Cone( self.scene, pcpos, animobpos ).tiles
                        area = animobs.get_line( pcpos[0], pcpos[1], animobpos[0], animobpos[1] )
                        area.remove( pcpos )
                        for a in area:
                            ao = animobs.Steam( pos=a, delay=self.scene.distance(a,pcpos ) + 1 )
                            anims.append( ao )
                        for a in self.scene.contents:
                            if a.pos in area:
                                ao = animobs.Caption( str(random.randint(5,27)), a.pos, delay=self.scene.distance(a.pos,pcpos ) + 1 )
                                anims.append( ao )

                        animobs.handle_anim_sequence( self.screen, self.view, anims )


