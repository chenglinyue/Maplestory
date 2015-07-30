'''Author: Cheng Lin
Date: June 5th, 2012
Description: This program is a mini version of the 2D game Maplestory. 
It is a one player game and will be using the same images and similar
sprites as the original but the game will be implemented differently 
overall. The game will be both keyboard and mouse controlled. The left 
and right arrow keys will move the player left and right, respectively. 
The x key will allow the user to jump and the z key will allow the user
to attack. The objective of the game is to kill a bunch of monsters and 
to collect the gold coins that they will drop in random amounts; a NPC 
will be there to aid the player by restoring their HP. The game will 
end once all four stages are complete or when the player�s health points 
reach zero. '''

# I - Import and Initialize
import pygame, Sprites, random
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([1024, 670])

def game(cursor, gender):
    '''This function is the main game. It will take a cursor sprite and 
    a gender as parameters. The gender parameter will determine the sex 
    of the player'''
    # Display
    pygame.display.set_caption("Mini MapleStory :)")
     
    # Entities
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    
    #Create Sprite objects for the game
    boss = Sprites.BossMonster(screen)
    #The player will be either a male or female character depending on the
    #gender parameter
    player = Sprites.Player(screen, gender)
    effect = Sprites.Attack(screen)
    label = Sprites.Label(screen, 5000, 0, 1)
    npc = Sprites.NPC()
    maps = Sprites.Map(screen)
    border = Sprites.Border()
    #Create a text sprite that shows the changes in the amount of gold for the player
    tracker = Sprites.Button('',(screen.get_width()-100,30),24,(255,255,255),True)
    #Create a health point bar for the boss monster
    healthPointBar = Sprites.HPBar(screen)
    portal = Sprites.Portal(screen)
    reminder = Sprites.Reminder()
    
    #Create 8 monster sprites that will be recycled for each stage
    monsters = []
    for i in range(8):        
        monsters.append(Sprites.Monster(screen,random.randrange(-1,2)))
        
    #Create 8 gold sprites; one  associated with each monster
    golds = []
    for i in range(8):
        golds.append(Sprites.Gold(screen,False))    
    #Create a 9th gold sprite associated with the boss
    golds.append(Sprites.Gold(screen,True))

    #Create multiple damage sprites
    damages = []
    #The first 8 damage sprites will be assosiated with the 8 monsters
    for i in range(8):
        damages.append(Sprites.Damage(1))
    #The 9th damage sprite will be assosiated for the boss collisions with player 
    damages.append(Sprites.Damage(0))
    #The 10th damage sprite will be assosiated monster collisions with player
    damages.append(Sprites.Damage(0))
    #The 11th damage sprite will be player's attack on boss
    damages.append(Sprites.Damage(2))
        
    # Create Sprite Groups
    #Group all monsters, boss, golds, npc, damages, portal and player into a 
    #group to move them with the map
    mapMovementGroup = pygame.sprite.Group(monsters, player, golds, \
                                           npc, damages, boss, portal)
    
    #Group for resetting purposes after each stage
    resetGroup = pygame.sprite.Group\
               (healthPointBar, boss, maps, player, npc, label, monsters, portal)
    
    #Put all sprites into a group for easy updating
    allSprites = pygame.sprite.OrderedUpdates(maps, border, tracker, \
                healthPointBar, boss,\
                monsters,player, effect, damages,\
                golds, label, npc, portal, reminder, cursor)
    
    # Load sound effects
    #Load monster sound effects    
    monster1 = pygame.mixer.Sound('./Sound Effects/OrangeMushroomDie.wav')
    monster1.set_volume(0.4)
    monster2 = pygame.mixer.Sound('./Sound Effects/Leprechaun1Die.wav')
    monster2.set_volume(0.2)
    monster3 = pygame.mixer.Sound('./Sound Effects/JrBalrogDie.wav')
    monster3.set_volume(0.3)
    monster4 = pygame.mixer.Sound('./Sound Effects/WyvernDie.wav')
    monster4.set_volume(0.4)
    #Put the sound effects for the monster in a list for easy playing
    monster_sound_effects = [monster1,monster2,monster3,monster4]
    
    #Load sound effects of boss
    boss_sound_effects = []
    for i in range(1,5):
        boss_sound = pygame.mixer.Sound('./Sound Effects/boss'+str(i)+'.wav')
        boss_sound.set_volume(1.0)
        #Put the sound effects of the bosses in a list for easy playing
        boss_sound_effects.append(boss_sound)
    
    #Load sound effect for the attack
    attack_sound = pygame.mixer.Sound('./Sound Effects/DarkImpaleUse.wav')
    attack_sound.set_volume(0.15)            

    #Load other sound effects
    heal = pygame.mixer.Sound('./Sound Effects/Red Potion.wav')
    heal.set_volume(0.8)
    gold_sound = pygame.mixer.Sound('./Sound Effects/Gold.wav')
    gold_sound.set_volume(0.6)
    enter = pygame.mixer.Sound("./Sound Effects/GameIn.wav")
    enter.set_volume(0.5)
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
        
    #Load first background music 
    pygame.mixer.music.load('./Background music/music1.mp3')
    pygame.mixer.music.set_volume(0.3)  
    #Play the first background music until the next stage
    pygame.mixer.music.play(-1)    

    # ACTION (broken into ALTER steps)
     
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
        
    #Create a list of False boolean values for updating Gold and damage 
    #Sprite purposes
    false_list = [False] * 10
    gold_list = false_list[:]
    attack_list = false_list[:]    
    
    #Variable to keep track of whether the player is moving or not
    player_moving_right = False
    player_moving_left = False
    
    #Used for collision detection 
    counter = 0
    
    #Keep track of how much time has passed. 
    time = 0
    
    #Variable used for indexing the list of sound effects
    current_stage = 0
    #Variable to keep track whether or not to play sound effect
    play_sound = True
    #Keep track of whether the player won or lost
    game_over = False
    winner = False
  
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    # Loop
    while keepGoing:
     
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            #Check if player quit the game
            if event.type == pygame.QUIT:
                keepGoing = False
            #Check if the player pressed any game keys, if so handle them accordingly
            elif event.type == pygame.KEYDOWN:
                keyName = pygame.key.name(event.key)
                if keyName == 'x':
                    player.jump()
                    
                if keyName == 'left':
                    player.moving(-6)
                    player_moving_left = True
                    
                if keyName == 'right':
                    player.moving(6)
                    player_moving_right = True
                    
                if keyName == 'z':
                    #The following lines of code avoids the player from 
                    #spamming the attack key
                    if effect.finish():
                        player.attacking(player.attack_finished())
                        #Animate attack                             
                        effect.start(player.get_direction(),player.rect.center)
                        #Play sound effect
                        attack_sound.play()
                
                #Check if player entered the portal (clicked the up key)
                #If so, move onto the next stage
                if keyName == 'up' and player.rect.collidepoint(portal.rect.center):
                    #Play sound effect
                    enter.play()
                    if current_stage < 3:
                        #Move onto the next stage
                        gold_list = false_list[:]
                        play_sound = True
                        current_stage += 1
                        #Fadeout the current background music
                        pygame.mixer.music.fadeout(3000)
                        #Load next background music
                        pygame.mixer.music.load\
                              ('./Background music/music'+str(current_stage+1) + '.mp3')
                        pygame.mixer.music.set_volume(0.3)
                        #Play the new background music until the next stage
                        pygame.mixer.music.play(-1) 
                        
                        #Reset the HP bar, boss, map, player, npc, label, 
                        #portal and monsters
                        for sprite in resetGroup:
                            sprite.reset() 
                        #Reset the position of each gold
                        for gold in golds:
                            gold.reset((-100,-100), True)
                            
                    #Terminate loop when the player wins        
                    else:
                        keepGoing = False
                        winner = True
                        
                if keyName == 'space':
                    #If the player has enough gold, the following will occur:
                    if label.spend_gold():
                        #Recover the player's HP
                        player.recover()
                        #Play sound effect
                        heal.play()
                        label.set_health_points(5000)
                        #Show that 1000 gold was spent in exchange for recovery
                        tracker.set_text('-1000')
                        
            #Check if the player released keys on the keyboard        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.moving(0)   
                    player_moving_right =False
                    
                if event.key == pygame.K_LEFT:
                    player.moving(0)
                    player_moving_left = False
                    
            #Check for mouse events        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Play sound effect of mouse clicking
                click.play()
                cursor.click()
                #Check to see if the mouse clicked on the NPC
                if npc.rect.collidepoint(pygame.mouse.get_pos()):
                    #Play sound effect
                    mouse_over.play()
                    #Check to see if the player has enough gold to recover HP
                    if label.spend_gold():
                        #Recover the player's HP
                        player.recover()
                        #Play the sound effect of potion
                        heal.play()
                        label.set_health_points(5000)
                        #Show that 1000 gold was spent in exchange for recovery
                        tracker.set_text('-1000')
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                cursor.release()
                                    
        #Check for collisions between player and boss
        if player.rect.colliderect(boss.rect) and counter % 30 == 0:
            damages[8].update_damage(player.rect.center, player.take_boss_damage())
            label.set_health_points(player.get_health_points())
            
        #Check for collisions between player and monster
        #Using elif statement to avoid damaging the player twice in one frame
        elif pygame.sprite.spritecollide(player, monsters, False) and\
           counter % 30 == 0:
            damages[9].update_damage(player.rect.center, player.take_damage())
            label.set_health_points(player.get_health_points())
            
        #Check for collisions between boss and attack of player
        if boss.rect.colliderect(effect.rect) and not attack_list[8]:
            damage_boss = boss.take_damage()
            damages[10].update_damage(boss.rect.center, damage_boss)
            #Avoids multiple collisions within a second
            attack_list[8] = True
            #Update Boss's HP Bar
            healthPointBar.take_damage(damage_boss)
              
        #Check if boss is dead (HP <= 0)
        if boss.get_status():
            #Play sound effect while the monster is in its animation of dying
            boss_sound_effects[current_stage].play()

        #Check for collisions between attack of player and monsters
        #This way I can easily update other things like damage or gold because  
        #the monster, damage and gold sprites share a common index
        for index in range(len(monsters)):
            if monsters[index].rect.colliderect(effect.rect)\
               and not attack_list[index]:
                #Update damage
                damages[index].update_damage(monsters[index].get_position(), \
                                         monsters[index].take_damage())
                #Avoids multiple collisions within a second
                attack_list[index] = True
 
            #If the monster died, reset the position of the gold to the position
            #Of where the monster died
            if monsters[index].dead() and not gold_list[index]:
                #If the monster died, play sound effect
                monster_sound_effects[current_stage].play()
                #Position the gold where the monster died
                golds[index].reset(monsters[index].get_position(), False)
                #Change the item in the list of boolean variables to True
                #This avoids the gold from re-appearing 
                gold_list[index] = True
 
        #Check for collisions between player and gold
        for index in range(len(golds)):
            if player.rect.colliderect(golds[index].rect):
                gold_sound.play()
                value = golds[index].get_value()
                #Position the gold outside of the screen once the player reaches it
                golds[index].reset((-100,-100), True)
                label.set_gold(value)   
                #Show how much the gold was worth in the tracker
                tracker.set_text("+"+str(value))
                
        # Update the reminder sprite
        if boss.dead():
            #If the stage is clear, remind the player that they can move on
            reminder.show(1)
            #Have the portal appear in the game
            if play_sound:
                enter.play()
                play_sound = False
                #Drop gold
                golds[8].reset(boss.get_position(),False)
            portal.boss_killed() 
        #Check how much HP the player has, if it is under 1500 remind the player
        #that their HP is running low
        elif player.get_health_points() <=1500:
            reminder.show(0)   
        else:
            reminder.reset()

        #Move the map if the player reaches the centre of the screen
        if player.rect.centerx > screen.get_width()/2 and player_moving_right\
           and not maps.move(True):
            #move the player, monster, golds, damages and boss in the opposite 
            #direction if the map is moving and player are moving right
            for sprite in mapMovementGroup:
                sprite.map_moving(-6)
   
        elif player.rect.centerx < screen.get_width()/2 and player_moving_left\
             and not maps.move(False):
            #move the player, monster, damages, gold and 
            #boss if the map and player are moving left
            for sprite in mapMovementGroup:
                sprite.map_moving(6)
                
        #Check if player died
        if player.get_health_points() <= 0:
            keepGoing = False
            game_over = True
        
        #The purpose of the following lines of code is so that the monsters/boss
        #are not getting attacked 30 times a second, but rather every second 
        #when the attack and monster or boss are colliding
        if counter % 30 == 0:
            attack_list = false_list[:]
        
        #Add one to counter and time
        counter += 1   
        time += 1
            
        # Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
     
        pygame.display.flip()
        
    #If the player won or lost go to hall of fame
    if winner:
        return hallOfFame(True, label.get_gold(), time/30, cursor)
    elif game_over:
        return hallOfFame(False, label.get_gold(), time/30,cursor)
    #Otherwise, exit the game
    else:
        return 'quit'

def menu(cursor):
    '''This function defines a main menu screen for the game. It will take a 
    cursor sprite as a parameter'''
    # Display
    pygame.display.set_caption("MapleStory Selection Screen")
    
    #Entities
    background = pygame.image.load('./Backgrounds/HomeScreen.jpg').convert()
    screen.blit(background,(0,0))
    
    #Create buttons that will lead to different pages
    button1 = Sprites.Button('START !', (523, 172), 56, (150,150,170),False)
    button2 = Sprites.Button('Controls', (376, 357), 36,(150,150,170),False)
    button3 = Sprites.Button('About', (615, 360), 36,(150,150,170),False)
    button4 = Sprites.Button('Quit', (153, 403), 36, (150,150,170),False)
    #Put the buttons into a list for easy collision detections with the mouse
    buttonlist = [button1, button2,button3, button4]
    
    #Group the sprites 
    allSprites = pygame.sprite.OrderedUpdates(buttonlist, cursor)

    #Load sound effect
    enter = pygame.mixer.Sound("./Sound Effects/GameIn.wav")
    enter.set_volume(0.5)
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    page_flip = pygame.mixer.Sound("./Sound Effects/WorldSelect.wav")
    page_flip.set_volume(0.6)

    # ACTION
     
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
 
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # Loop
    while keepGoing:
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor.click()
                click.play()
                #If the user clicked the start button, return start to main()
                #To start the game
                if button1.rect.collidepoint(pygame.mouse.get_pos()):
                    enter.play()
                    return 'start'
                #If the user clicked the instructions button, return instructions
                elif button2.rect.collidepoint(pygame.mouse.get_pos()):
                    page_flip.play()
                    return 'instructions'
                #If the user clicked the about button, return about 
                elif button3.rect.collidepoint(pygame.mouse.get_pos()):
                    page_flip.play()
                    return 'about'
                #If the user clicked the quit button, exit the loop 
                elif button4.rect.collidepoint(pygame.mouse.get_pos()):
                    keepGoing = False
                
            elif event.type == pygame.MOUSEBUTTONUP:
                cursor.release()
                
            elif event.type == pygame.MOUSEMOTION:
                #Highlight the button that the mouse is hovering over
                for index in range(len(buttonlist)):          
                    if buttonlist[index].rect.collidepoint\
                       (pygame.mouse.get_pos()):
                        buttonlist[index].highlight()
                        mouse_over.play()
                    else:
                        buttonlist[index].normal()

        #Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    #Unhide mouse pointer
    pygame.mouse.set_visible(True)
    #return quit (quits the game)
    return 'quit'
    
def about(cursor):
    '''This function creates a page for the game that provides background
    information about the game. It will take a cursor sprite as a parameter'''
    # D - Display configuration
    pygame.display.set_caption("About MapleStory")
     
    # E - Entities
    background = pygame.image.load('./Backgrounds/AboutScreen.jpg').convert()
    screen.blit(background, (0,0))
    
    #Create a back_button that will lead back to the main menu of the game
    back_button = Sprites.Button('Back to Menu', (800,360),29,(61,61,70),False)
    
    #Group the back button and cursor sprites
    allSprites = pygame.sprite.Group(back_button, cursor)
    
    #Load sound effect
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    page_flip = pygame.mixer.Sound("./Sound Effects/WorldSelect.wav")
    page_flip.set_volume(0.6)
     
    # A - Action (broken into ALTER steps)
     
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
     
    # L - Loop
    while keepGoing:
     
        # T - Timer to set frame rate
        clock.tick(30)
     
        # E - Event handling
        for event in pygame.event.get():
            #Check if the player quit the game
            if event.type == pygame.QUIT:
                keepGoing = False
            
            #Check for mouse events
            elif event.type == pygame.MOUSEMOTION:
                #If the mouse is hovering over the backbutton, change the
                #colour of the back button (highlight)
                if back_button.rect.collidepoint(pygame.mouse.get_pos()):
                    back_button.highlight()
                    mouse_over.play()
                else:
                    #Return the colour of the text on the back button back to
                    #normal once the mouse is no longer colliding with it
                    back_button.normal()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor.click()
                click.play()
                #If the player clicked the back button, return to the menu
                if back_button.rect.collidepoint(pygame.mouse.get_pos()):
                    page_flip.play()
                    return 'menu'
                
            elif event.type == pygame.MOUSEBUTTONUP:
                cursor.release()

        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
        
    #Unhide mouse pointer
    pygame.mouse.set_visible(True)
    return 'quit'

def instructions(cursor):
    '''This function creates an instruction screen for the game. It will take
    a cursor sprite as a parameter.'''
    # Display
    pygame.display.set_caption("Instructions")
    
    # Entities
    background = pygame.image.load('./Backgrounds/InstructionScreen.jpg').convert()
    screen.blit(background,(0,0))

    #Create a back button that leads to the menu
    back_button = Sprites.Button('Back to Menu', (860,580),29,(61,61,70),False)
    
    #Create a player that the user can practice with before starting the game
    player = Sprites.Player(screen, 1)

    #Group the sprites
    allSprites = pygame.sprite.OrderedUpdates(back_button, cursor, player)
    
    #Load sound effect
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    page_flip = pygame.mixer.Sound("./Sound Effects/WorldSelect.wav")
    page_flip.set_volume(0.6)
    
    # ACTION
     
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
 
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # Loop
    while keepGoing:
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
            #Checking if the user clicked the backbutton    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor.click()
                click.play()
                if back_button.rect.collidepoint(pygame.mouse.get_pos()):
                    page_flip.play()
                    #Return to main menu
                    return 'menu'
                
            elif event.type == pygame.MOUSEBUTTONUP:
                cursor.release()
                
            #Check to see if the cursor is colliding with the back button
            #If so, highlight the text on the button
            elif event.type == pygame.MOUSEMOTION:     
                if back_button.rect.collidepoint(pygame.mouse.get_pos()):
                    back_button.highlight()
                    mouse_over.play()
                else:
                    back_button.normal()
                    
            #Change the animation of the player
            elif event.type == pygame.KEYDOWN:
                keyName = pygame.key.name(event.key)
                if keyName == 'x':
                    player.jump()
                if keyName == 'left':
                    player.moving(-5)
                if keyName == 'right':
                    player.moving(+5)
                if keyName == 'z':
                    player.attacking(True)
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.moving(0)
                if event.key == pygame.K_LEFT:
                    player.moving(0)

        #Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()
         
    #Unhide mouse pointer
    pygame.mouse.set_visible(True)
    return 'quit'
    
def selection(cursor):
    '''This function creates a page for the game that allows the user to choose 
    the sex of their character. It will take a cursor sprite as a parameter'''
    # D - Display configuration
    pygame.display.set_caption("Character Selection")
     
    # E - Entities
    background = pygame.image.load\
               ('./Backgrounds/CharacterSelection.jpg').convert()
    screen.blit(background, (0,0))
    
    #Load sound effects
    enter = pygame.mixer.Sound("./Sound Effects/AWizetWelcome.wav")
    enter.set_volume(0.7)
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    
    #Create two buttons
    male_button = Sprites.Button('Male', (312,407),29,(61,61,70),False)
    female_button = Sprites.Button('Female', (775,408),29,(61,61,70),False)
    
    #Group the buttons and cursor sprites
    allSprites = pygame.sprite.Group(male_button, female_button, cursor)
    

    # A - Action (broken into ALTER steps)
     
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
     
        # L - Loop
    while keepGoing:
     
        # T - Timer to set frame rate
        clock.tick(30)
     
        # E - Event handling
        for event in pygame.event.get():
            #Check if the user quit the progam
            if event.type == pygame.QUIT:
                keepGoing = False
             
            #Check if the mouse is colliding with the buttons
            #If so highglight the text of the button
            elif event.type == pygame.MOUSEMOTION:
                if male_button.rect.collidepoint(pygame.mouse.get_pos()):
                    male_button.highlight()
                    mouse_over.play()
                else:
                    male_button.normal()
                    
                if female_button.rect.collidepoint(pygame.mouse.get_pos()):
                    female_button.highlight()
                    mouse_over.play()
                else:
                    female_button.normal()
            #Check if the player clicked the buttons       
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor.click()
                click.play()
                if male_button.rect.collidepoint(pygame.mouse.get_pos()):
                    #Fadeout music
                    pygame.mixer.music.fadeout(8000)
                    enter.play()
                    #Return 2 so that the main game will know to load
                    #The images of the male character
                    return 2
                elif female_button.rect.collidepoint(pygame.mouse.get_pos()):
                    #Fadeout music
                    pygame.mixer.music.fadeout(8000)
                    enter.play()
                    #Return 1 so that the main game will know to load
                    #The images of the female character
                    return 1
                
            elif event.type == pygame.MOUSEBUTTONUP:
                cursor.release()

        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
        
    #Unhide mouse pointer
    pygame.mouse.set_visible(True)    
    return 'quit'
        
def hallOfFame(winner, gold_collected, new_time, cursor):
    '''This function displays an end game screen. It takes a winner boolean
    variable, gold_collected, and new_time as parameters. It will show how 
    much gold the player collected and how long it took for them to finish the
    adventure/how long they lasted. It will also take a cursor sprite as a 
    parameter'''
    
    # D - Display configuration
    pygame.display.set_caption("Hall of Fame")
     
    # E - Entities
    background = pygame.image.load('./Backgrounds/HallofFame.jpg').convert()
    screen.blit(background, (0,0))
    
    #Open and read the hall of fame file
    hall_of_fame = open('HallofFame.txt', 'r')
    fastest, most_gold = hall_of_fame.readline().strip().split()
    fastest = int(fastest)
    most_gold = int(most_gold)
    
    #Check if the player won or lost
    if winner:
        text = 'Brave explorer, thank you for saving maple Island!' 
        text2 = 'You finished your adventure in %ds and with %d gold!' %\
             (new_time, gold_collected)
        #If the player won, check if they set a new high score
        if new_time < fastest:
            fastest = new_time
        if gold_collected > most_gold:
            most_gold = gold_collected
            
        #Rewrite the hall of fame
        hall_of_fame = open('HallofFame.txt', 'w')
        hall_of_fame.write(str(fastest) + ' ' + str(most_gold))
        hall_of_fame.close()
        
    else:
        text = 'Thank you for your attempt to save Maple Island.'
        text2 = 'You managed to collect %d gold, and survived for %ds'%\
              (gold_collected,new_time)

    #Create labels to display the player's score
    label1 = Sprites.Button(text, (514,200),23,(61,61,70),False)
    label2 = Sprites.Button(text2, (514,250), 23, (61,61,70),False)
    
    #Display the fastest time
    label3 = Sprites.Button("Fastest time: %ss" % fastest,\
                              (514,350),26,(61,61,70),False)
    
    #Display the most gold ever collected
    label4 = Sprites.Button("Most gold collected: %d" % most_gold,\
                              (514,400), 26, (61,61,70), False)    
    
    #Create buttons 
    menu_button = Sprites.Button('Back to Menu', (824,620),29,(31,31,40),False)
    
    #Group the labels, button and cursor sprites
    allSprites = pygame.sprite.OrderedUpdates(menu_button, label1, \
                                     label2, label3, label4, cursor)
    
    #Load sound effect
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)

    #Play backgorund music
    pygame.mixer.music.load('./Background music/HallofFame.mp3')
    pygame.mixer.music.set_volume(0.3)  
    #Play the first background music until the next stage
    pygame.mixer.music.play(-1)  

    # A - Action (broken into ALTER steps)
     
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
     
        # L - Loop
    while keepGoing:
     
        # T - Timer to set frame rate
        clock.tick(30)
     
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            
            #Check if mouse is overlapping with the menu button
            #if so highlight the text
            elif event.type == pygame.MOUSEMOTION:
                if menu_button.rect.collidepoint(pygame.mouse.get_pos()):
                    menu_button.highlight()
                    mouse_over.play()
                else:
                    menu_button.normal()
            
            #Check if the player clicked the menu button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor.click()
                click.play()
                #If so, return to the menu
                if menu_button.rect.collidepoint(pygame.mouse.get_pos()):
                    return 'menu'
                
            elif event.type == pygame.MOUSEBUTTONUP:
                cursor.release()

        # R - Refresh display 
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()   
        
    #Unhide mouse pointer
    pygame.mouse.set_visible(True)    
    return 'quit'        

def main():
    '''This function defines the 'mainline logic' for our game.'''
    # Create a custom cursor
    #The purpose of creating the cursor here is because it is used in all the
    #different screens of the game
    cursor = Sprites.Mouse()
    
    #Initialize finish to False
    finish = False
    
    while finish != 'quit':
        #Load Background Music
        pygame.mixer.music.load("./Background music/WelcometoMapleStory.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        
        #Call the main menu
        finish = menu(cursor)
        #If the user clicks the about button in the main menu, go to that page
        if finish == 'about':
            #If the user clicks the back button, return to main menu
            finish = about(cursor) 
            if finish == 'menu':
                finish = menu(cursor)
        #If user clicks the controls button, go to the instructions page        
        if finish == 'instructions':
            #If the user clicks the back button, return to menu
            finish  = instructions(cursor) 
            if finish == 'menu':
                finish = menu(cursor)   
        #If the user clicked the start button, go to the selection screen
        if finish == 'start':
            #Choose the gender of their player
            finish = selection(cursor)
            if finish in [1,2]:
                #Pass in an integer to the main game.
                #The integer will be used to identify the sex of the player
                finish = game(cursor, finish)
                
    pygame.quit()
    
# Call the main function
main()