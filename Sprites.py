'''Author: Cheng Lin
Date: June 5th 2012
Description: This is the module that contains all the classes
for the Maplestory game.'''

import pygame, random
                
class Player(pygame.sprite.Sprite):
    '''This class will create a main player for the game'''
    def __init__(self,screen, integer):
        '''This initializer method will take a screen and gender as 
        parameters to know which list of sprites to load. If the integer is 1
        a female character will be created, if integer is 2, a male character 
        is created. This method will load all the images of the player as well 
        as set its rect attribute. It will initialize the player on the bottom 
        left of the screen, initialize the player's health points to 
        5000 and assign the image attribute to the first frame of the player 
        in the resting_right list of images.'''
        
        #Call parent's initializer method
        pygame.sprite.Sprite.__init__(self)        
        
        #Create a list of images of the player resting facing right
        self.__resting_right = []
        for i in range(5):
            self.__temp_image = pygame.image.load\
                ('./Player'+str(integer)+'/stand2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((0,255,0))
            self.__resting_right.append(self.__temp_image)
                        
        #Create a list of images of the player resting facing left
        self.__resting_left = []
        for i in range(5):
            self.__temp_image = pygame.image.load\
                ('./Player'+str(integer)+'/stand1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((0,255,0))
            self.__resting_left.append(self.__temp_image)
            
        #Create a list of images of the player moving right
        self.__walking_right = []
        for i in range(4):
            self.__temp_image = pygame.image.load\
                ('./Player'+str(integer)+'/walk2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((0,255,0))
            self.__walking_right.append(self.__temp_image)
        
        #Create a list of images of the player moving left    
        self.__walking_left = []
        for i in range(4):
            self.__temp_image = pygame.image.load\
                ('./Player'+str(integer)+'/walk1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((0,255,0))
            self.__walking_left.append(self.__temp_image)
            
        #Create a list of images of the player attacking and facing right
        self.__attacking_right = []
        for i in range(3):
            self.__temp_image = pygame.image.load\
                ('./Player'+str(integer)+'/swing2_' + str(i) +".png").convert()
            self.__temp_image.set_colorkey((0,255,0))
            self.__attacking_right.append(self.__temp_image)
            
        #Create a list of images of the player attacking and facing left
        self.__attacking_left = []
        for i in range(3):
            self.__temp_image = pygame.image.load\
                ('./Player'+str(integer)+'/swing1_' + str(i) +".png").convert()
            self.__temp_image.set_colorkey((0,255,0))
            self.__attacking_left.append(self.__temp_image)      
            
        #Load images of player jumping    
        self.__jumping_right = pygame.image.load\
            ('./Player'+str(integer)+'/jump2_0.png').convert()
        self.__jumping_right.set_colorkey((0,255,0))
        
        self.__jumping_left = pygame.image.load\
            ('./Player'+str(integer)+'/jump_0.png').convert() 
        self.__jumping_left.set_colorkey((0,255,0))
        
        #Set the image attribute for our Player sprite
        self.image = self.__resting_right[0]
        
        #Set the rect attribute for our Player sprite
        self.rect = self.image.get_rect()
        #Place the player on the bottom left of the screen
        self.rect.left = 20
        self.rect.bottom = screen.get_height() - 72     
        
        #Initialize health points to 5000
        self.__health_points = 5000
        
        #X and Y vectors for player
        self.__dy = -17.5
        self.__dx = 0
        
        #This attribute will be used for animation purposes. 
        #It is used to control the rate at which the image updates
        self.__counter = 0
        #Attribute to index the above lists of images
        self.__index = 1
        
        # BOOLEAN VARIABLES FOR ANIMATION PURPOSES 
        #Instead of having one boolean variable and assigning 'string' values
        #To it, multiple will be needed because in the update method
        #multiple of these boolean variables will need to be checked
        self.__jumping = False
        self.__facing_right = True
        self.__walking = False
        self.__resting = True
        self.__attacking = False
        self.__attack_finish = True
        
        #Variable to keep track of screen
        self.__screen = screen 
        
        #This boolean variable will be used to move the player with the map
        self.__map_moving = False
        self.__move = 0
    
    def get_health_points(self):
        '''This method will return the number in the __health_points attribute'''
        return self.__health_points
    
    def get_direction(self):
        '''This method returns the integer 2 if the player is facing 
        right and 1 if facing left'''
        if self.__facing_right:
            return 2
        else:
            return 1
        
    def recover(self):
        '''This method recovers the player's __health_points to 5000.
         This method returns nothing'''
        self.__health_points = 5000

    def jump(self):
        '''This method will allow the player to jump by setting __jumping to
        True and __resting to False-- but only if the player is not already 
        in mid-air. This method returns nothing'''
        #If statement needed so that the player cannot jump while already
        #In mid-air
        if not self.__jumping:
            self.__dy = -17.5
            self.__jumping = True
            self.__resting = False
            self.rect.bottom = self.__screen.get_height() - 79
        
    def attacking(self, finish):
        '''This method will allow the player to attack if they are not jumping
        by set __attacking to True, __resting to False, and
        __attack_finish to False. This method returns nothing'''
        #If the player jumps and attacks, transitions will not be smooth
        #because multiple keys cannot be pressed. Only show attack animation if
        #the player is not jumping
        if not self.__jumping:
            #Set index to -1 for smooth updating
            self.__index = -1
            #Set counter to 3
            self.__counter = 3
            self.__attacking = True
            self.__resting = False  
            self.__attack_finish = False
        
    def attack_finished(self):
        '''This method returns True if the attack is finished animating, False
        if otherwise. This prevents the user from spamming the attack key'''
        if self.__attack_finish:
            return True
        return False

    def moving(self, integer):
        '''This method takes a single integer value as a parameter and assigns 
        it to self.__dx. It also assigns self.__walking attribute to True unless
        the user released the left or right arrow key on the keyboard. It 
        updates the self.__facing_right attribute according to the integer 
        parameter. This method returns nothing'''
        #Set __resting to False so it doesn't update the resting animation
        self.__resting = False        
        #Set __walking to True for updating the walking animation
        self.__walking = True
        #Set X vector direction to the integer parameter
        self.__dx = integer  
        if integer >0:
            #If the integer is greater than 0, this means that the player is
            #moving right
            self.__facing_right = True
            #Assign new image to image attribute
            self.image = self.__walking_right[0]   
            
        elif integer <0:
            #If the integer is less than 0, this means that the player is
            #moving left
            self.__facing_right = False 
            #Assign new image to image attribute
            self.image = self.__walking_left[0]
            
        else:
            #If the integer is 0 the player released the left or right arrowkey
            self.__walking = False
            self.__resting = True        
            #Set the new image attribute
            if self.__facing_right:
                self.image = self.__resting_right[0]
            else:          
                self.image = self.__resting_left[0] 
                
    def reset(self):
        '''This method will reset the position of the player to the
        bottom left of the screen. This method returns nothing'''
        self.rect.left = 20
        self.rect.bottom = self.__screen.get_height() - 72   
                
    def take_damage(self):
        '''This method will choose a random number between 100 to 400 and 
        subtract the number from __health_points. This method returns the 
        number in the __take_damage attribute after the assignment.'''
        self.__take_damage = random.randrange(100,401)
        self.__health_points -= self.__take_damage
        return self.__take_damage

    def take_boss_damage(self):
        '''This method will choose a random number between 500 to 999 and 
        subtract the number from __health_points. This method returns the 
        number in self.__take_damage'''
        self.__take_damage = random.randrange(500,1000)
        self.__health_points -= self.__take_damage
        return self.__take_damage
    
    def map_moving(self, integer):
        '''This method will move the player in a certain direction that 
        depends on the integer parameter. This is so that the player does
        not continually move when the map is moving. This method returns nothing'''
        #Set map_moving to True
        self.__map_moving = True
        #Assign the vector of the movement of the map to integer
        self.__move = integer
    
    def update(self):
        '''This method will be responsible for repositioning the image on the 
        screen as well as iterating through the list of images according to 
        different Boolean variables, ultimately, causing the animations to 
        occur. It will also check if the player has reached the end of the 
        screen or if the map is moving. If the map is moving, the player will
        be moved the opposite direction of the map.'''
        # Add one to counter
        self.__counter += 1        

        #Make the player move
        if self.__walking and not self.__attacking:  
            if ((self.rect.left > 0) and (self.__dx < 0)) or\
           ((self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
                self.rect.centerx += self.__dx  
            #Change image attribute to animation of player walking    
            if self.__facing_right and not self.__jumping and self.__counter %4 ==0: 
                try:                    
                    # Add one to refresh variables            
                    self.__index += 1
                    self.image = self.__walking_right[self.__index]
                #If there is an IndexError, the animation ended
                except IndexError:
                    #Reset the __index attribute to 0 to reset animation
                    self.__index = 0        
            elif not self.__facing_right and not self.__jumping and self.__counter %4 ==0:
                try:                    
                    # Add one to refresh variables            
                    self.__index += 1
                    self.image = self.__walking_left[self.__index]
                except IndexError:
                    self.__index = 0
                             
        #Make the player jump
        if self.__jumping: 
            #Update image attribute to image of jumping player
            if self.__facing_right:
                self.image = self.__jumping_right
            elif not self.__facing_right:
                self.image = self.__jumping_left
                
            if self.rect.bottom <= self.__screen.get_height() - 72:
                self.rect.bottom += self.__dy
                #Decellerates on the way up and accelerates on the way down
                self.__dy += 1.75
            else:
                #Update image and attributes once the player reaches the ground
                self.rect.bottom = self.__screen.get_height()-72
                self.__jumping = False 
                if self.__facing_right:
                    self.image = self.__resting_right[0]
                else:
                    self.image = self.__resting_left[0]
                self.__resting = True         

        #Animate player at rest
        if self.__resting and not self.__walking:
            if self.__facing_right and self.__counter %12 == 0:
                try:                    
                    # Add one to refresh variables            
                    self.__index += 1
                    self.image = self.__resting_right[self.__index]
                except IndexError:
                    self.__index = 0             
            elif not self.__facing_right and self.__counter %12 == 0:
                try:                    
                    # Add one to refresh variables            
                    self.__index += 1
                    self.image = self.__resting_left[self.__index]
                except IndexError:
                    self.__index = 0                           
                    
        #Animate player attacking
        if self.__attacking:
            #Change image attribute to animation of player attacking    
            if self.__facing_right and self.__counter % 4 == 0: 
                try:                    
                    #Add one to refresh variables            
                    self.__index += 1
                    self.image = self.__attacking_right[self.__index]
                except IndexError:
                    #Once an index error occurs, the attack animation is finished 
                    #Set the attack_finish attribute to True so the player can
                    #attack again. 
                    self.__attack_finish = True
                    self.__attacking = False
                    #Update the player's image For smooth transition between frames
                    if self.__walking:                        
                        self.image = self.__walking_right[0]
                    else:
                        self.__resting= True
                        self.image = self.__resting_right[0]
                        
            if not self.__facing_right and self.__counter %4== 0:
                try:                    
                    # Add one to refresh variables            
                    self.__index += 1
                    self.image = self.__attacking_left[self.__index]
                except IndexError:
                    self.__attack_finish = True
                    self.__attacking = False
                    #For smooth transition between frames
                    if self.__walking:
                        self.image = self.__walking_left[0]
                    else:
                        self.__resting = True  
                        self.image = self.__resting_left[0]
       
        #Check if map is moving, if it is move the player the opposite direction
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False

class Monster(pygame.sprite.Sprite):
    '''This class will define a single monster for our game'''
    def __init__(self,screen,integer):
        '''This initializer method will create a monster on a random part of
        the screen on the floor of the map. It will take a screen and integer as 
        parameters and initialize its health_points to 3000 and its dx to 1/0/
        -1 (So not all of the monsters will move in the same direction); this 
        will be dependent on the integer parameter. It will set the image 
        attribute to the first image of the monster either moving left or 
        right or standing; also depending on the integer value. '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)   
        
        #Create a list of images of the first monster depending on the integer parameter
        self.__moving1 = []
        for i in range(3):
            self.__temp_image = pygame.image.load\
                ('./Monster1/move'+str(integer+1)+'_' + str(i) + '.png')\
                .convert()
            self.__temp_image.set_colorkey((0,255,0))
            self.__moving1.append(self.__temp_image)
            
        #Load a list of images of the first monster dying
        self.__dying1 = []
        for i in range(3):
            self.__temp_image = pygame.image.load('./Monster1/die'+\
                str(integer+1)+'_' +\
                str(i) + '.png').convert()
            self.__temp_image.set_colorkey((0,255,0))
            self.__dying1.append(self.__temp_image)
        
        #Create lists of images for the second monster   
        if integer != 0:
            self.__moving2 = []
            for i in range(25):
                self.__temp_image = pygame.image.load('./Monster2/stand'+\
                    str(integer+1)+'_' + str(i) + '.png').convert()
                self.__temp_image.set_colorkey((255,171,166))
                self.__moving2.append(self.__temp_image)
        else:
            self.__moving2 = []
            for i in range(8):
                self.__temp_image = pygame.image.load('./Monster2/attack'+\
                    str(integer+1)+'_' + str(i) + '.png').convert()
                self.__temp_image.set_colorkey((255,171,166))
                self.__moving2.append(self.__temp_image)

        #Load a list of images of the second monster dying
        self.__dying2 = []
        for i in range(17):
            self.__temp_image = pygame.image.load('./Monster2/die'+\
                    str(integer+1)+'_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,171,166))
            self.__dying2.append(self.__temp_image)
            
        #Create a list of images of the third monster depending on the integer parameter
        if integer == 0: 
            self.__moving3 = []
            for i in range(16):
                self.__temp_image = pygame.image.load('./Monster3/attack'+\
                    str(integer+1)+'_' + str(i) + '.png').convert()
                self.__temp_image.set_colorkey((150,150,150))
                self.__moving3.append(self.__temp_image)
        else:
            self.__moving3 = []
            for i in range(5):
                self.__temp_image = pygame.image.load('./Monster3/move'+\
                    str(integer+1)+'_' + str(i) + '.png').convert()
                self.__temp_image.set_colorkey((150,150,150))
                self.__moving3.append(self.__temp_image)
        
        #Load a list of images of the third monster dying
        self.__dying3 = []
        for i in range(3):
            self.__temp_image = pygame.image.load('./Monster3/die'+\
                str(integer+1)+'_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150,150,150))
            self.__dying3.append(self.__temp_image)
            
        #The fourth monster will be moving and flying in both left and right
        #Directions unlike the previous monsters
        #Load a list of images of the fourth monster attacking and flying left
        self.__attacking_left4 = []
        for i in range(36):
            self.__temp_image = pygame.image.load\
                ('./Monster4/attack1_'+str(i) +'.png').convert()
            self.__temp_image.set_colorkey((200,200,255))
            self.__attacking_left4.append(self.__temp_image)
            
        #Load a list of images of the fourth monster attacking and flying right
        self.__attacking_right4 = []
        for i in range(36):
            self.__temp_image = pygame.image.load\
                ('./Monster4/attack2_'+str(i) +'.png').convert()
            self.__temp_image.set_colorkey((200,200,255))
            self.__attacking_right4.append(self.__temp_image)  
            
        #Load a list of images of the fourth monster dying and facing left
        self.__dying_left4 = []
        for i in range(5):
            self.__temp_image = pygame.image.load\
                ('./Monster4/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((200,200,255))
            self.__dying_left4.append(self.__temp_image)          
            
        #Load a list of images of the fourth monster dying and facing right
        self.__dying_right4 = []
        for i in range(5):
            self.__temp_image = pygame.image.load\
                ('./Monster4/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((200,200,255))
            self.__dying_right4.append(self.__temp_image)     
        
        # Set the image attribute for our Monster sprite 
        self.__moving = self.__moving1
        self.__dying = self.__dying1
        self.image = self.__moving[0]

        #This instance variable will hold a list of dimensions of the game maps
        self.__map_dimensions = [1775,1700,1683,1975]
        
        #Set the rect attribute for our Monster sprite
        self.rect = self.image.get_rect()
        #Place the monster randomly on the floor of map
        self.rect.right = random.randrange(250, self.__map_dimensions[0])
        
        #The image of the monster at rest needs to be positioned a bit lower
        #due to unusual dimensions
        if integer == 0:
            self.rect.bottom = screen.get_height() - 60
        else:
            self.rect.bottom = screen.get_height() - 70
        
        #Initialize health points of monster
        self.__health_points = 3000
                
        #Initialize damage taken to 0
        self.__take_damage = 0
        
        #Attributes for dying animations
        self.__dead = False
        self.__finished = False
        
        #Attribute used to keep track of the direction of monster 
        #(Used for fourth monster only)
        self.__going_left = True
        
        #Keep track of screen
        self.__screen = screen
        
        #Keep track of current monster
        self.__current_monster = 1
               
        #This attribute will be used for animation purposes. 
        #It is used to control the rate at which the image updates
        self.__counter = 0
        
        #List of counters for updating the monster frames/animations. This is 
        #because different monsters will animate its frames at different speeds
        
        #List for moving animations
        self.__counter_list1 = [6,4,6,3]
        #List for dying animations
        self.__counter_list2 = [4,3,10,6]
        
        #Attribute to index the above lists. A random index will be selected
        #So not all monsters are animating the exact same frames at the same time
        self.__index = random.randrange(0,3)
        self.__dying_index = -1  
        #X vector of monster
        self.__dx = integer

        #Attributes used to move the monster with the map
        self.__map_moving = False
        self.__move = 0
    
    def take_damage(self):
        '''This method will choose a random number between 200 to 1000 and 
        subtracts the number from __health_points. This method returns the 
        number in self.__take_damage'''
        self.__take_damage = random.randrange(200,1000)
        self.__health_points -= self.__take_damage
        return self.__take_damage
    
    def reset(self):
        '''This method will update the image lists that are assosiated with
        the image attribute. It will also set a new integer value to the
        health points of the monster and update the boolean variables 
        of the monster. This method returns nothing'''
        #Add one to current monster
        self.__current_monster += 1
        
        #Update Boolean Variables
        self.__finished = False
        self.__dead = False
        #Update next dying animation index
        self.__dying_index = -1

        if self.__current_monster == 2:
            #Update image attribute
            self.__moving = self.__moving2
            self.__dying = self.__dying2

            #Select a random index o not all monsters animate the same frames
            #at the same time
            if self.__dx != 0:
                self.__index = random.randrange(0,25)
            else:
                self.__index = random.randrange(0,8)
            
            #Give the monster a bit more HP than the previous monster
            self.__health_points = 4000

        elif self.__current_monster == 3:
            #Update image attribute
            self.__moving = self.__moving3
            self.__dying = self.__dying3

            #So not all monsters are animating the same frames at the same time
            if self.__dx == 0:
                self.__index = random.randrange(0,16)
            else:
                self.__index = random.randrange(0,5)
            #Give the monster a bit more HP than the previous
            self.__health_points = 5000
            
        elif self.__current_monster == 4:
            #The fourth boss will behave more so like a boss monster
            #It will fly as well as move in two directions. 
            #Choose a random direction that the fourth monster will be travelling
            go_left = random.randrange(2)
            if go_left == 0:
                self.__going_left = True
                self.__dx = -1
            else:
                self.__going_left = False
                self.__dx = 1
                
            #Update image attribute    
            if self.__going_left:
                self.__moving = self.__attacking_left4
                self.__dying = self.__dying_left4
            else:
                self.__moving = self.__attacking_right4
                self.__dying = self.__dying_right4

            #So not all monsters are animating the same frames at the same time
            self.__index = random.randrange(0,36)
            self.__dying_index = -1
            
            #Make the fourth monster fly
            self.__dy = -1
            
            #Give the monster a bit more HP than the previous
            self.__health_points = 7000
            
        #Set the new image and rect attribute for our new monster 
        self.image = self.__moving[0]
        self.rect = self.image.get_rect()
        
        #Place the monster randomly on the screen 
        self.rect.right = random.randrange\
            (250, self.__map_dimensions[self.__current_monster-1])
        #Place the 4th monster randomly in the air
        if self.__current_monster ==4:
            self.rect.top = random.randrange(0,self.__screen.get_height()-300)
        elif self.__current_monster == 2:
            #The second monster has unusual dimensions if it is standing on
            #the ground so adjustments need to be made
            if self.__dx == 0:
                self.rect.bottom = self.__screen.get_height()-60
            else:
                self.rect.bottom = self.__screen.get_height()-70
        else:
            self.rect.bottom = self.__screen.get_height()-70
        
    def get_position(self):
        '''This method returns the position of the monster before it is moved
        off the screen (dead)'''
        return self.__position
 
    def dead(self):
        '''This method will check if the monster died and the animation has
        finished. It will return True if so'''
        if self.__finished:    
            return True
        return False   
    
    def map_moving(self, integer):
        '''This method will move the monster in a certain direcction that 
        depends on the integer parameter. This is so that the monster does
        not contually move when the map is moving. This method returns nothing'''
        #Set map_moving to True
        self.__map_moving = True
        #Assign the vector of the movement of the map to integer
        self.__move = integer
 
    def update(self):
        '''This method will be responsible for repositioning the image on the 
        screen as well as iterating through lists of images according to 
        different Boolean variables, ultimately, causing the animations to occur.
        It will also check if the monster has reached the end of the screen.
        If the monster died, it will move it outside of the screen where it 
        will not be hit by the player'''           
        #Check if monster ran out of health points        
        if self.__health_points <=0:
            self.__dead = True
            
        #Check if the monster animation finished dying
        if self.__finished:
            #Move the image outside of the screen on the other side of attack sprite
            self.rect.center= (1500,0)
            
        #Animate the monster
        if self.__counter % self.__counter_list1[self.__current_monster-1] == 0 \
           and not self.__dead: 
            if self.__current_monster != 4:
                try:
                    self.__index += 1
                    self.image = self.__moving[self.__index]
                except IndexError:
                    #If there is an index error, that meansthe animation reached
                    #its end, reset the index to 0 for animation to continue
                    self.__index = 0              
                #Checking to see if the monster reached the end of the screen
                #If not, continue to move the monster
                if self.rect.left > 0 and self.__dx <0:
                    self.rect.left += 3 *self.__dx  
                elif self.rect.right < self.__screen.get_width() and self.__dx >0:
                    self.rect.left += 3 * self.__dx    
                
            else:
                #The fourth and final monster will behave more like a boss monster
                #It will reverse directions if it hits the top/bottom, or ends
                #of the map
                try:
                    self.__index += 1
                    if self.__going_left:
                        self.image = self.__attacking_left4[self.__index]
                    else: 
                        self.image = self.__attacking_right4[self.__index]
                except IndexError:
                    self.__index = 0
                
                # hecking to see if the 4th monster reached the end of the screen
                if ((self.rect.left > 0) and (self.__dx < 0)) or\
               ((self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
                    self.rect.left += 3* self.__dx
                #If so reverse the x direction
                else:
                    self.__dx = self.__dx * -1  
                    self.__going_left = not self.__going_left
                    
                #Check to see if the fourth monster reached top of screen
                if ((self.rect.top > 0) and (self.__dy > 0)) or\
               ((self.rect.bottom < self.__screen.get_height() - 70) and (self.__dy < 0)):
                    self.rect.top -= 3*self.__dy
                #If yes, reverse the y direction. 
                else:
                    self.__dy = -self.__dy

        #If monster died, change animation to it dying
        if self.__counter %self.__counter_list2[self.__current_monster-1] == 0\
           and self.__dead:
            try:
                self.__dying_index += 1  
                if self.__current_monster !=4:
                    self.image = self.__dying[self.__dying_index]
                else:
                    if self.__going_left:                
                        self.image = self.__dying_left4[self.__dying_index]   
                    else:
                        self.image = self.__dying_right4[self.__dying_index]  
            except IndexError:
                #There will be an indexerror when the animation of the monster
                #finished
                self.__finished = True
                self.__dead = False
                
        #Check if map is moving, if it is move the monster the opposite way
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False
                                
        if not self.__finished:
            #Store the position of the monster before it dies and gets
            #moved off the screen
            self.__position = self.rect.center

        self.__counter += 1  

class BossMonster(pygame.sprite.Sprite):
    '''This class will define a single boss monster for the game'''   
    def __init__(self, screen):
        '''This initializer method will create a boss monster at the bottom right 
        of the screen. It will take a screen as a parameter and initialize 
        its health_points to 50000 and __dx to -1.5 It will set the image
        attribute to the first image of the boss moving left.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)     
        
        #Create a list of images of the First Boss moving left
        self.__going_left1 = []
        for i in range(11):
            self.__temp_image = pygame.image.load\
                ('./Boss1/attack1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,255,166))
            self.__going_left1.append(self.__temp_image)
            
        #Create a list of images of the First Boss moving right
        self.__going_right1 = []
        for i in range(11):
            self.__temp_image = pygame.image.load\
                ('./Boss1/attack2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,255,166))
            self.__going_right1.append(self.__temp_image)
            
        #Create lists of images of the First Boss dying
        self.__dying_left1 = []
        for i in range(6):
            self.__temp_image = pygame.image.load\
                ('./Boss1/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,255,166))
            self.__dying_left1.append(self.__temp_image)   
            
        self.__dying_right1 = []    
        for i in range(6):
            self.__temp_image = pygame.image.load\
                ('./Boss1/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,255,166))
            self.__dying_right1.append(self.__temp_image)   
        
        #Create a list of images of the Second boss moving left
        self.__going_left2 = []
        for i in range(11):
            self.__temp_image = pygame.image.load\
                ('./Boss2/attack2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,186,92))
            self.__going_left2.append(self.__temp_image)
            
        #Create a list of images of the Second boss moving right
        self.__going_right2 = []
        for i in range(11):
            self.__temp_image = pygame.image.load\
                ('./Boss2/attack1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,186,92))
            self.__going_right2.append(self.__temp_image)
            
        #Create lists of images of the Second boss dying
        self.__dying_left2 = []
        for i in range(21):
            self.__temp_image = pygame.image.load\
                ('./Boss2/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,224,255))
            self.__dying_left2.append(self.__temp_image)   
            
        self.__dying_right2 = []    
        for i in range(21):
            self.__temp_image = pygame.image.load\
                ('./Boss2/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,224,255))
            self.__dying_right2.append(self.__temp_image)    
        
        #Create a list of images of the Third Boss moving left
        self.__going_left3 = []
        for i in range(16):
            self.__temp_image = pygame.image.load\
                ('./Boss3/attack1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150,150,150))
            self.__going_left3.append(self.__temp_image)
            
        #Create a list of images of the Third Boss moving right
        self.__going_right3 = []
        for i in range(16):
            self.__temp_image = pygame.image.load\
                ('./Boss3/attack2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150,150,150))
            self.__going_right3.append(self.__temp_image)
            
        #Create lists of images of the Third Boss dying
        self.__dying_left3 = []
        for i in range(10):
            self.__temp_image = pygame.image.load\
                ('./Boss3/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150,150,150))
            self.__dying_left3.append(self.__temp_image)   
            
        self.__dying_right3 = []    
        for i in range(10):
            self.__temp_image = pygame.image.load\
                ('./Boss3/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150,150,150))
            self.__dying_right3.append(self.__temp_image)      
            
        #Create a list of images of the Fourth Boss moving left
        self.__going_left4 = []
        for i in range(29):
            self.__temp_image = pygame.image.load\
                ('./Boss4/attack1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,255,166))
            self.__going_left4.append(self.__temp_image)
            
        #Create a list of images of the Fourth Boss moving right
        self.__going_right4 = []
        for i in range(29):
            self.__temp_image = pygame.image.load\
                ('./Boss4/attack2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,255,166))
            self.__going_right4.append(self.__temp_image)
            
        #Create lists of images of the Fourth Boss dying
        self.__dying_left4 = []
        for i in range(11):
            self.__temp_image = pygame.image.load\
                ('./Boss4/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,255,217))
            self.__dying_left4.append(self.__temp_image)   
            
        self.__dying_right4 = []    
        for i in range(11):
            self.__temp_image = pygame.image.load\
                ('./Boss4/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255,255,217))
            self.__dying_right4.append(self.__temp_image)    

        # Set the image attribute for our Boss Monster sprite
        self.__going_left = self.__going_left1
        self.__going_right = self.__going_right1
        self.__dying_left = self.__dying_left1
        self.__dying_right = self.__dying_right1
        self.image = self.__going_left[0]
        
        #This instance variable will hold a list of dimensions of the game maps
        self.__map_dimensions = [1775,1700,1683,1975]
         
        # Set the rect attribute for our Boss Monster sprite
        self.rect = self.image.get_rect()
        #Place the Boss on the bottom right of the map
        self.rect.bottomright = (self.__map_dimensions[0],\
                                screen.get_height() - 70)

        # Initialize health points to 70000
        self.__health_points = 70000
                
        #Initialize damage taken to 0
        self.__take_damage = 0
        
        #Boolean variables for dying animation
        self.__finished = False
        self.__dead = False
        #Initialize Boss to go left
        self.__direction_left = True       
               
        #This attribute will be used for animation purposes. 
        #It is used to control the rate at which the image updates
        self.__counter = 0
        
        #Attribute to index the above lists
        self.__index = 1
        self.__dying_index = 0
        
        #X vector of monster
        self.__dx = -9
        #Y vector of monster (The first boss will not fly)
        self.__dy = 0
        
        #Keep track of which boss the player is currently fighting
        self.__current_boss = 1
        
        #Variable to keep track of screen
        self.__screen = screen 
        
        #Used for returning purposes
        self.__return = True
        
        #This boolean variable will be used to move the monster with the map
        self.__map_moving = False
        self.__move = 0
        
        #List of positions that are used for the bottom rect of the boss
        #during dying animations
        self.__dying_position = [screen.get_height(),screen.get_height()-50,\
                screen.get_height() - 100, screen.get_height()-10]
        
        #List of counters for updating the boss frames/animations. This is 
        #because different bosses will animate its frames at different speeds
        #List for moving animations
        self.__counter_list1 = [4,3,4,4]
        #List for dying frames
        self.__counter_list2 = [11,6,5,8]
            
    def take_damage(self):
        '''This method will choose a random number between 1000 to 5000 and 
        subtract the number from __health_points. This method returns the 
        assigned random number.'''
        self.__take_damage = random.randrange(1000,5000)
        self.__health_points -=self.__take_damage
        return self.__take_damage
        
    def dead(self):
        '''This method will check if the boss died. It will return True if so'''
        if self.__finished:  
            return True
        return False   
    
    def get_status(self):
        '''This method will return True if the monster's HP is less than or equal
        to zero'''
        if self.__dead and self.__return:
            self.__return = False
            return True
        return False
    
    def get_position(self):
        '''This method returns the position of the boss before it is moved
        off the screen (dead)'''
        return self.__position
    
    def reset(self):
        '''This method will update the lists that will be assosiated with
        the image attribute. It will also set a new integer value to the
        health points attribute. Boolean variables will also be updated'''      
        #Update Boolean Variables
        self.__finished = False
        self.__dead = False
        self.__return = True
        self.__direction_left = True 
        
        #Reset index attributes 
        self.__index = 0
        self.__dying_index = 0
        
        #Add one to current boss
        self.__current_boss += 1
        
        #Update bosses accordingly 
        if self.__current_boss == 2:
            #Add a bit more HP to the next boss
            self.__health_points = 80000
            # Set new image attribute for our Boss Monster sprite
            self.__going_left = self.__going_left2
            self.__going_right = self.__going_right2
            self.__dying_left = self.__dying_left2
            self.__dying_right = self.__dying_right2

            #Set new x and y vectors
            self.__dx = -7
            self.__dy = 0
            
        elif self.__current_boss == 3:
            #Add a bit more HP to the next boss
            self.__health_points = 90000
            # Set new image attribute for our Boss Monster sprite
            self.__going_left = self.__going_left3
            self.__going_right = self.__going_right3
            self.__dying_left = self.__dying_left3
            self.__dying_right = self.__dying_right3
            
            #Make the boss fly to increase difficulty
            self.__dy = 4
            self.__dx = -6
 
        elif self.__current_boss == 4:
            # Add a bit more HP to the next boss
            self.__health_points = 100000
            # Set new image attribute for our Boss Monster sprite
            self.__going_left = self.__going_left4
            self.__going_right = self.__going_right4
            self.__dying_left = self.__dying_left4
            self.__dying_right = self.__dying_right4
            
            #Make the boss fly to increase difficulty
            self.__dy = 4
            self.__dx = -9
            
        #Set the new image and rect attributes for our Boss Monster sprite
        #Reset the boss on the ground of the map and at the far right
        #of the map
        self.image = self.__going_left[0]
        self.rect = self.image.get_rect()
        self.rect.bottomright = (self.__map_dimensions[self.__current_boss-1],\
                                 self.__screen.get_height()-60)
            
    def map_moving(self, integer):
        '''This method will move the monster in a certain direcction that 
        depends on the integer parameter. This is so that the monster does
        not continually move when the map is moving.'''
        #Set map_moving to True
        self.__map_moving = True
        #Assign the vector of the movement of the map to the integer parameter
        self.__move = integer
            
    def update(self):       
        '''This method will be responsible for repositioning the sprite on the 
        screen as well as iterating through the list of images, causing the 
        animations to occur. It will also check if the boss has reached the 
        end of the screen, and if so, it will reverse its direction.'''         
        #Check if boss monster ran out of health points        
        if self.__health_points <=0:
            #If so, the monster is dead; assign dead attribute to True
            self.__dead = True
            
        #Animate the boss
        if self.__counter % self.__counter_list1[self.__current_boss-1] == 0 \
           and not self.__dead: 
            try:
                if self.__direction_left:
                    self.image = self.__going_left[self.__index]
                else: 
                    self.image = self.__going_right[self.__index]
            except IndexError:
                #If there is an IndexError, that means that the animation reached
                #the end, so reset index to 0 to restart the animation
                self.__index = 0
            self.__index += 1  
            
            #Checking to see if the monster reached the end of the map
            if ((self.rect.left > 0) and (self.__dx < 0)) or\
               ((self.rect.right < self.__screen.get_width()) \
                and (self.__dx > 0)):
                self.rect.left += self.__dx

            #If so reverse the x direction
            else:
                self.__dx = self.__dx * -1  
                self.__direction_left = not self.__direction_left
                
            #Check to see if the monster reached top of screen
            if ((self.rect.top > 0) and (self.__dy > 0)) or\
           ((self.rect.bottom < self.__screen.get_height()-70) and (self.__dy < 0)):
                self.rect.top -= self.__dy
            #If yes, then reverse the y direction. 
            else:
                self.__dy = -self.__dy
                
        #Checking to see if monster died, if so, animate dying frames      
        if self.__counter % self.__counter_list2[self.__current_boss-1] == 0 \
           and self.__dead:
            self.__dying_index += 1
            #Tweaking rect position
            self.rect.bottom = self.__dying_position[self.__current_boss-1]
            try:
                if self.__direction_left:                
                    self.image = self.__dying_left[self.__dying_index]   
                else:
                    self.image = self.__dying_right[self.__dying_index]         
            except IndexError:
                #If there is an IndexError, that means that the animation
                #of the boss dying has finished
                self.__finished = True
                
        #Check if map is moving, if it is move the boss the opposite way
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False       
 
        if not self.__finished:
            #Store the position of the boss before it dies and gets
            #moved off the screen
            self.__position = self.rect.center
        else:
            #If the boss died, place it out of the screen
            self.rect.center = (-700,-100)
          
        #Add one to counter
        self.__counter += 1  
            
class Map(pygame.sprite.Sprite):
    '''This class creates a series of custom maps that will move according
    to the position of the player'''
    def __init__(self, screen):
        '''This function will load 4 maps and set the image attribute to the
        first map. It takes a screen as a parameter'''
        #Call the parent sprite
        pygame.sprite.Sprite.__init__(self)
        
        #Load the images of the maps and put them in a list
        self.__list_of_images = []
        for i in range(1,5):
            self.__temp_image = pygame.image.load\
                ('./Maps/Map_' + str(i) + '.jpg').convert()
            self.__list_of_images.append(self.__temp_image)
            
        #Set the image to the first image
        self.image = self.__list_of_images[0]
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        
        #Variable to keep track of the current map
        self.__map = 0
        #Variable to keep track of screen
        self.__screen = screen
        
        #Variables to keep track of whether should move or not
        self.__move = 'none'
        self.__reach_end = True
        
    def reset(self):
        '''This method sets the image attribute to the following map and
        assigns the following map image to the image attribute'''
        self.__map += 1
        if self.__map < 4:
            #Set the new image of the map
            self.image = self.__list_of_images[self.__map]
            #Get the new rect attributes
            self.rect = self.image.get_rect()
            
    def move(self, go_right):
        '''This map moves the map in accordance to the player. It takes
        a boolean variable as a parameter and sets the move attribute to 
        'left' or 'right' depending on this parameter. This method will 
        return True if map reached the end of the screen. Otherwise, it 
        will return False'''
        #Set a new value to __move attribute 
        if go_right:
            self.__move = 'right'
        else:
            self.__move = 'left'
        #If the end of the map is reached, return True    
        if self.__reach_end:
            return True
        #Otherwise, return False
        return False

    def update(self):
        '''This method updates the map image by moving it according to the
        move and reach end attributes''' 
        #Move the map accordingly (until it reaches its end)
        if self.__move == 'right' and \
           self.rect.right >= self.__screen.get_width()+5:
            self.rect.right -= 6
            self.__reach_end = False
        
        elif self.__move == 'left'  and self.rect.left <=-5:
            self.rect.left += 6 
            self.__reach_end = False
            
        else:
            self.__reach_end = True
                
        self.__move = 'none'

class Gold(pygame.sprite.Sprite):
    def __init__(self, screen, boss):
        '''This initializer method will create a coin object and set its image 
        and rect. It will take a screen and boss boolean variable as parmeters
        and position the gold outside of the screen. The boss parameter will
        determine the image to load as well as the value of the gold'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)   
        
        #Set the gold's image attribute
        if not boss:
            self.image = pygame.image.load('./OtherImages/gold.gif').convert()
        else:
            self.image = pygame.image.load('./OtherImages/gold_sack.gif').convert()
        
        #Set the rect attributes
        self.rect = self.image.get_rect()
        
        #Position the gold outside the screen
        self.rect.center = (-100,-100)
        
        #Set the value of the gold to 0
        self.__value = 0
        
        #Keep track of the screen and boss parameters
        self.__boss = boss
        self.__screen = screen
        
        #This boolean variable will be used to move the gold with the map
        self.__map_moving = False
        self.__move = 0
        
    def reset(self, position, set_position):
        '''This method updates the gold sprite. The set_position parameter will
        hold either True or False. If it is True, that means that the gold and
        player rects collided, if this is the case, the image will be positioned
        off the screen. If False, it will assign a new, random value to the gold 
        and position the coin on the screen in accordance with the position 
        parameter which will be the position of where the monster died.'''
        # Update the gold's rect attribute
        if not set_position:            
            # Assign a new value to the gold
            if not self.__boss:
                self.__value = random.randrange(100,301)
            else:
                self.__value = random.randrange(500,1201)
            #Extract the x vector of the position parameter and place the
            #Coin 85 pixels less than the screen's height and at the 
            #extracted x-vector
            self.rect.center = (position[0], self.__screen.get_height()-85)
            
        else:
            self.__value = 0
            self.rect.center = (-100,-100)
            
    def map_moving(self, integer):
        '''This method will move the gold in a certain direcction that 
        depends on the integer parameter. This is so that the gold does not 
        stay in place even when when the map is moving. The gold will be moved
        in the opposite direction of the map's movements. This method returns
        nothing'''
        #Set map_moving to True
        self.__map_moving = True
        #Assign the vector of the movement of the map to integer
        self.__move = integer
                    
    def get_value(self):
        '''This method will return the value of the gold.'''
        return self.__value
    
    def update(self):
        '''This method will check if map is moving, if it is, move the gold 
        in the opposite direction of the map'''
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False
        
class Damage(pygame.sprite.Sprite):
    '''This class will display numbers that represent the amout of damage dealt
    on the player, monster, or boss'''   
    def __init__(self, attack_who):
        '''This class will create a custom font object. The attack_who parameter 
        will determine the colour of the text and the damage will be placed 
        initially outside the screen'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)   
        
        #Create a custom font object
        self.__font = pygame.font.Font('./Fonts/DAMAGE.ttf', 48)

        #List of colours that will be used for the damage sprite
        #The colour used will be determined by the attack_who parameter
        self.__list = [(255,106,106),(255,50,50),(225,0,54)]
        self.__colour = self.__list[attack_who]
        self.__damage = self.__font.render('0', 1, self.__colour)
        
        #Set image and rect attributes
        self.image = self.__damage
        self.rect = self.image.get_rect()
        #Place the damage outside the screen
        self.rect.center = (-200,-200)
        
        #Used to time how long the damage will stay visible
        self.__counter = 0
        
        #This boolean variable will be used to move the damage with the map
        self.__map_moving = False
        self.__move = 0
        
    def update_damage(self, position, damage):
        '''This method will take the amount of damage dealt and the position 
        of the player/monster/boss as parameters. The damage will be placed
        just on top of the player/boss/monster. This method will also render 
        the text to the number in the damage parameter.'''
        #Render font and assign it to the image attribute
        #Message will be customized according to parameters
        self.__damage = self.__font.render(str(damage), 1, self.__colour)
        self.image = self.__damage
        #Position the damage just above the player/monster/boss
        self.rect.midbottom = (position[0], position[1] - 20)    
        #Reset counter to 0
        self.__counter = 0

    def map_moving(self, integer):
        '''This method will move the damage in a certain direction that 
        depends on the integer parameter. This is so that the damage does not 
        stay in place even when when the map is moving. The damage will be 
        moved in the opposite direction of the map's movements. Thie method
        returns nothing'''
        #Set map_moving to True
        self.__map_moving = True
        #Assign the vector of the movement of the map to integer
        self.__move = integer
                
    def update(self):
        '''This method will position the image of the damage outside the
        screen when enough time has passed so the damage will be unseen.
        It will also check to see if the map is moving, if it is, the 
        damage will be moved in the opposite direction of the map'''
        self.__counter += 1
        if self.__counter % 40 == 0:
            #Place damage outside screen
            self.rect.center = (-200,-200)
            
        #Check if map is moving, if it is move the damage text in the opposite 
        #direction
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False
                 
class HPBar(pygame.sprite.Sprite):
    '''This class creates an HP bar to show how the reamining HP of the
    boss monster'''
    def __init__(self, screen):
        '''This method will create a red rectangle used as the HP bar for the 
        Boss monster. This method will position the HP bar just under the Border 
        sprite. This method will take a screen as a parmater'''
        #Call the parent sprite
        pygame.sprite.Sprite.__init__(self)
        
        #Set the image attribute to a red rectangle the length of the screen
        self.__hpBar = pygame.Surface((screen.get_width(), 7)).convert()
        self.__hpBar.fill((225,0,81))
        self.image = self.__hpBar
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,50)
        
        #List of maximum Health Points of the Bosses
        self.__list = [70000,80000,90000,100000]
        
        #Set the maximum health_points of the first boss
        self.__health = self.__list[0]
        
        #Keep track of width of bar
        self.__new_width = screen.get_width()
        #Keep track of screen
        self.__screen = screen
        #Keep track of boss number
        self.__current_boss = 0
        
    def reset(self):
        '''This function will add one to the current boss attribute and set
        the new maximum health of the monster. This function will also reset 
        the health bar to full HP, meaning back to the width of the screen'''
        self.__current_boss += 1
        #Set the new maximum health of boss
        self.__health = self.__list[self.__current_boss]
        #Reset the width of the bar
        self.__new_width = self.__screen.get_width()
        self.__hpBar = pygame.Surface((self.__new_width , 7)).convert()
        self.__hpBar.fill((225,0,81))
        
    def take_damage(self,damage):
        '''This function will resize the size of the HP Bar according to how
        much damage was dealt on the boss'''
        #Working with ratios to determine the new width of the HP Bar based on
        #How much damage was dealt on the boss
        self.__new_width = self.__new_width * (self.__health - damage) /self.__health
        #Can't have negative width
        if self.__new_width<= 0:
            self.__new_width = 0
        self.__health -= damage
        self.__hpBar = pygame.Surface((self.__new_width, 7)).convert()
        self.__hpBar.fill((225,0,81))
        
    def update(self):
        '''This method will update the image of the HP Bar'''
        self.image = self.__hpBar

class Attack(pygame.sprite.Sprite):
    '''This class will show the animation of the players attack '''
    def __init__(self,screen):
        '''This method takes a screen as a parameter. The frames for the
        animation will be loaded here and the image attribute will be assigned 
        the first image of the attack_right lists of images.
        The sprite will be positioned outside the screen where it will not 
        interfere with other sprites'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self) 
        
        #Create lists of images to hold the attack animations
        self.__attack_left = []
        for i in range(12):
            self.__temp_image = pygame.image.load('./Skill/effect.1'+\
                                                  '_' + str(i) + '.png')
            self.__attack_left.append(self.__temp_image)
            
        self.__attack_right = []
        for i in range(12):
            self.__temp_image = pygame.image.load('./Skill/effect.2'+\
                                                  '_' + str(i) + '.png')
            self.__attack_right.append(self.__temp_image)

        #Set image attributes
        self.image = self.__attack_right[0]
        #Get the rect attributes
        self.rect = self.image.get_rect()
        #Set the center of the rect outside the screen so that 
        #it will not come in contact with any other sprites in the game
        self.rect.center = (-400,0)        

        #Attribute to index the above lists
        self.__index = 0  
        
        #Initialize self.__integer to 0
        self.__integer = 0
        
        #Keep track of the screen
        self.__screen = screen

        #This attribute will keep track of whether the animation is 
        #finished or not
        self.__finished = True
 
    def finish(self):
        '''This method will be called when the animation is over. It will return
        True when the animation is finished, False otherwise. This avoids the 
        player from spamming their attack'''
        if self.__finished:
            return True
        return False
    
    def start(self, integer, position):
        '''This method takes takes an integer and position as parameters. 
        The integer will be either 1 or 2, if it is 1 this means that the 
        player is attacking and facing left. If it is 2 the player is facing
        right. It will assign the position of the attack to the 
        position of the attack. This method returns nothing''' 
        #If the integer is 1, the player is facing left
        if integer == 1:
            self.__index = -1
            self.__integer = 1
            #Position the effect where the player is
            self.__position = position

        #If the integer is 2, the player is facing right
        elif integer == 2:
            self.__index = 0
            #Assign value to self.__integer to be used in update
            self.__integer = 2
            #Position effect where player is 
            self.__position = position 
            
        self.__finished = False

    def update(self):
        '''This method will update the image attribute causing it to animate.'''
        # Animate the effect
        #If the integer attribute holds a 1, the player is attacking left
        if self.__integer == 1:
            try:
                self.__index += 1
                self.image = self.__attack_left[self.__index]
                #Place the effect to where the player is located
                self.rect.midright = (self.__position[0]+50, self.__position[1] - 25)
            #When there is an index error, the effect is finished
            except IndexError:
                self.__finished = True     
                #Set the center of the rect to outside of screen so that
                #it no longer comes in contact with any other sprites in the game
                self.rect.center = (-400,0)
                
        #If the integer attribute holds a 2, the player is attacking right  
        elif self.__integer == 2:
            try:
                self.__index += 1
                self.image = self.__attack_right[self.__index]
                #Place the effect to where the player is located
                self.rect.midleft = (self.__position[0] -50, self.__position[1] - 25)
            #When there is an index error, the effect is finished
            except IndexError:
                self.__finished= True     
                #Place the attack outside the screen
                self.rect.center = (-400,0)

class Label(pygame.sprite.Sprite):
    '''This class will define a label to display the amount of HP the 
    player has, the amount of gold the player collected, and the current stage'''
    def __init__(self, screen, health, amount, stage_num):
        '''This initializer method will take 4 parameters: 
        a screen, health_points to know the amount of HP the player has 
        remaining, value to know how much the value of gold the player picked
        up, and stage_num to know the current stage number. It will 
        initialize the label to the center-top of the screen'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)     
        
        #Create a custom font object
        self.__font = pygame.font.Font('./Fonts/Handwritten.ttf', 32)
        
        #Create atttributes for health points, amount of gold, and stage
        self.__health_points = health
        self.__amount = amount
        self.__stage = stage_num
        
        #Keep track of screen 
        self.__screen = screen
        
        #Set the message that will be displayed in the label
        self.__message = \
            'HP: %d                   STAGE: %d                   GOLD: %d   '% \
            (self.__health_points, self.__stage, self.__amount)
        self.image = self.__font.render(self.__message, 1, (245,255,255))
        #Set the image and rect attributes
        self.rect = self.image.get_rect()
        #Place the label on the top of the screen
        self.rect.center = (self.__screen.get_width()/2, 30)
        
    def set_health_points(self,health):
        '''This method takes an integer (health) as a parameter and will set 
        the __health_points attribute to the health paramaeter.'''
        self.__health_points = health
        
    def set_gold(self,value):
        '''This method takes a value (integer) as a parameter and will add
        the parameter to the __amount attribute'''
        self.__amount += value
        
    def get_gold(self):
        '''This method will return the amount of gold the player collected'''
        return self.__amount
        
    def reset(self):
        '''This method will add 1 to the __stage attribute '''
        self.__stage += 1
        
    def spend_gold(self):
        '''This method subtracts 1000 gold from __amount. If the user does not 
        have enough gold, do not allow action to take place. This method 
        returns True if the user has enough, False, if not.'''
        #If the user has enough gold, spend 1000 gold and return True
        if self.__amount >= 1000:
            self.__amount -= 1000   
            return True
        #Otherwise, return False
        return False
             
    def update(self):
        '''This method will update the text in the label'''
        self.__message = \
            'HP: %d                   STAGE: %d                   GOLD: %d   '% \
            (self.__health_points, self.__stage, self.__amount)
        self.image = self.__font.render(self.__message, 1, (245,255,255))

class NPC(pygame.sprite.Sprite):
    '''This class will create a NPC for the game'''
    def __init__(self):
        '''This initializer method will create the NPC for the game, by
        setting its image and rect attributes'''
        #Call the parent sprite's init method
        pygame.sprite.Sprite.__init__(self) 
        
        #Load a list of images for animation
        self.__npc_images = []
        for i in range(12):
            self.__temp_image = pygame.image.load\
                ('./npc/npc' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((0,255,0))
            self.__npc_images.append(self.__temp_image)
            
        #Initialize the image attribute to the first image of the list
        self.image = self.__npc_images[0]
            
        #Set the rect attributes
        self.rect = self.image.get_rect()
        self.rect.midbottom = (250,300)            
        
        #Variables for animation purposes
        self.__index = 0
        self.__counter = 0
        
        #This boolean variable will be used to move the NPC with the map
        self.__map_moving = False
        self.__move = 0
 
    def map_moving(self, integer):
        '''This method will move the NPC in a certain direction that 
        depends on the integer parameter. This is so that the npc is off 
        the screen when the map moves a certain vector.'''
        #Set map_moving to True
        self.__map_moving = True
        #Assign the vector of the movement of the map to integer
        self.__move = integer
        
    def reset(self):
        '''This method will reset the position of the NPC to the far
        left of the screen'''
        self.rect.midbottom = (250,300)    
    
    def update(self):
        '''This method will update the animation of the npc and check if the
        map is moving.'''
        #Animate the frames
        self.__counter += 1
        if self.__counter % 10 == 0:
            self.__index += 1
            #Check if the index exceeded the length of list
            if self.__index >= 12:
                self.__index = 0
            self.image = self.__npc_images[self.__index]
            
        #Check if map is moving, if it is move the NPC the opposite way
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False
   
class Mouse(pygame.sprite.Sprite):
    '''This class will define a custom cursor for the game!'''
    def __init__(self):
        '''This method will create the mouse cursor and position it at the
        center of the screen'''
        #Call the parent sprite's init method
        pygame.sprite.Sprite.__init__(self) 
        
        #Load the images that will be used for the cursor
        self.__normal = pygame.image.load('./OtherImages/normal.gif').convert()
        self.__normal.set_colorkey((0,255,0))
        self.__click = pygame.image.load('./OtherImages/click.gif').convert()
        self.__click.set_colorkey((0,255,0))
        
        #Set the image attribute to the normal cursor
        self.image = self.__normal
        
        #Get the image's rect attributes
        self.rect = self.image.get_rect()
        
        #Position the mouse in the center of the screen
        self.rect.center = (624,335)
        
    def click(self):
        '''This method will change the mouse to the to an image of the mouse 
        clicking.'''
        self.image = self.__click
        
    def release(self):
        '''This method will change the mouse image back to normal''' 
        self.image = self.__normal
        
    def update(self):
        '''This method moves the center of the image to where the mouse is.'''
        self.rect.center = pygame.mouse.get_pos()    
  
class Button(pygame.sprite.Sprite):
    '''This class creates buttons'''
    def __init__(self, text, position, size, colour, track):
        '''This method will create a custom font object. It will take text, a
        position, size of font, colour, and a boolean variable to keep track
        of whether or not the text will reset after around 2 seconds as 
        parameters. The text will be set according to the string value within 
        the text parameter. It will position the button according to the 
        position parameter, the size of the text will depend on the size 
        parameter, the colour of the text will depend on the colour parameter, 
        and the track parameter is needed to determine whether or not the text
        will be reset to an empty string. This is because this class is 
        recycled for two purposes.'''
        #Call the parent sprite's init method
        pygame.sprite.Sprite.__init__(self) 
        
        #Create a custom font object
        self.__font = pygame.font.Font('./Fonts/Handwritten.ttf', size)
        
        #Set the image and rect attributes of the button
        self.image = self.__font.render(text, 1, colour)
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        #Keep track of message 
        self.__message = text
        #Keep track of colour
        self.__colour = colour
        
        #Boolean variable to keep track of whether the button and mouse rects
        #are colliding 
        self.__collide = False
        
        #Used for refreshing text purposes
        self.__counter = 0
        #This boolean variable will be used to keep track of whether or not
        #the sprite is going to reset the message to an empty string
        self.__tracker = track
        
    def highlight(self):
        '''This method causes the text to change colour by setting __collide 
        to True'''
        self.__collide = True
    
    def normal(self):
        '''This method causes the text to return to normal by setting 
        __collide to False'''
        self.__collide = False
        
    def set_text(self,text):
        '''This method sets the message to the text parameter'''
        self.__message = text

    def update(self):
        '''This method updates the text of the button'''
        if self.__collide:           
            self.image = self.__font.render(self.__message, 1, (255,195,205))
        else:
            self.image = self.__font.render(self.__message, 1, self.__colour)
        
        #Add 1 to counter
        self.__counter += 1
        #If the sprite needs to refresh the message, set the message to an
        #empty String after around 2.5 seconds
        if self.__counter % 75 == 0 and self.__tracker:
            self.__message = ''
  
class Border(pygame.sprite.Sprite):
    '''This class creates a border for the game'''
    def __init__(self):
        '''This function will load an image of the border and position it on the
        top of the screen'''
        #Call the parent sprite
        pygame.sprite.Sprite.__init__(self)
        
        #Set the image attribute
        self.image = pygame.image.load('./OtherImages/border.jpg').convert()
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        
class Portal(pygame.sprite.Sprite):
    '''This class will show a portal for the game that the player can enter to
    advance to the next stage.'''
    def __init__(self,screen):
        '''This method takes screen as a parameter. A list of animations
        of the portal will be loaded here and the portal will be assigned
        the first image of the in the list to its image attribute. 
        It will be positioned outside the screen where it will not interfere
        with other sprites.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self) 
        
        #Create list of images of the portal
        self.__list = []
        for i in range(6):
            self.__temp_image = pygame.image.load('./Portal/0_'+ str(i) + '.png')
            self.__list.append(self.__temp_image)

        #Set image attributes
        self.image = self.__list[0]
        #Get the rect attributes
        self.rect = self.image.get_rect()
        #Set the center of the rect outside the screen so that 
        #it does not come into contact with any other sprites in the game
        self.rect.center = (0,-300)        

        #Attribute to index the above lists
        self.__index = 0  
        
        #Control the rate at which the animation of the portal updates
        self.__counter = 0
                
        #Keep track of the screen
        self.__screen = screen

        #This attribute will keep track of whether or not the portal needs to
        #reposition itself
        self.__reset = True

        #Y vector of the portal
        self.__dy = 0
        
        #This boolean variable will be used to move the portal with the map
        self.__map_moving = False
        self.__move = 0

    def boss_killed(self):
        '''This method will reset the portal effect. It set __dy to 15 so that
        the portal will move down the screen when this method is called.
        It will place the portal at the right end of the screen. This method 
        returns nothing''' 
        if self.__reset:
            self.__dy = 15
            self.rect.centerx = self.__screen.get_width() - 180
            self.__reset = False
        
    def reset(self):
        '''This method will move the portal off the screen and set its reset
        attribute to true. This method returns nothing'''
        self.rect.center = (0,-300)   
        self.__reset = True
        self.__dy = 0
        
    def map_moving(self, integer):
        '''This method will move the portal in a certain direction that 
        depends on the integer parameter. This is so that the portal moves
        alongside with the map. This method returns nothing'''
        #Set map_moving to True
        self.__map_moving = True
        #Assign the vector of the movement of the map to integer
        self.__move = integer

    def update(self):
        '''This method will update the image attribute causing it to animate.
        It will also move the portal down the screen if necessary. If the
        map is moving, the portal will be moved the opposite direction'''
        #Check if the portal reached the bottom of the screen
        self.__counter += 1
        if self.rect.bottom <= self.__screen.get_height() - 79:
            self.rect.bottom += self.__dy
            
        # Animate the effect    
        if self.__counter % 6 == 0:
            try:
                self.image = self.__list[self.__index]
                self.__index += 1
            #When there is an index error, that means the animation ended
            except IndexError:
                #Reset the animation
                self.__index = 0
                
        #Check if map is moving, if it is move the portal the opposite direction
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False
        
class Reminder(pygame.sprite.Sprite):
    '''This class creates a series of reminder message for the game that will 
    change depending on the current status of the game'''
    def __init__(self):
        '''This function will create a font object for the game and position
        it outside the screen.'''
        #Call the parent sprite
        pygame.sprite.Sprite.__init__(self)
        
        #Create a custom font object
        self.__font = pygame.font.Font('./Fonts/Handwritten.ttf', 22)
        
        #Create a list containing two messages
        self.__messages = \
            ['Your HP is running low. If you have 1000 gold or more, click the NPC or spacebar', \
             'You cleared the stage! Enter the portal to advance to the next stage']
        
        #Set the image attribute
        self.message = self.__messages[0]
        self.image = self.__font.render\
            (self.__messages[0], 1, (177,177,177))
        
        #Variable used to index the list of messages
        self.__index = 0
        
        #Set the rect attribute
        self.rect = self.image.get_rect()
        
        #Position the reminder outside the screen
        self.rect.bottom = 0
        
        #Attribute to keep track of whether or not the reminder should
        #be seen on the screen
        self.__show = False
        
    def show(self,index):
        '''This method will reposition the reminder on the screen by
        setting the __show attribute to True. It will take an index
        as a parameter to know which reminder to show''' 
        self.__index = index
        self.__show = True
        
    def reset(self):
        '''This method will change the __show attribute to False '''
        self.__show = False

    def update(self):
        '''This method will check whether or not the message should
        be shown, if so it will position the text on the screen. Otherwise
        the text will be placed off the screen'''
        if self.__show:
            self.rect.midtop = (542,59)
            self.image = self.__font.render\
                (self.__messages[self.__index], 1, (0,0,0))
        else:
            #Position the reminder outside the screens
            self.rect.bottom = 0
