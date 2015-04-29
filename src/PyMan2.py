#! /usr/bin/env python

import os, sys
import pygame
import math
from pygame.locals import *
from helpers import *
from random import randint

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self):
        """Initialize"""
        """set the number of torpedo's that should be on the board"""
        self.numTopedos = 5
        """set the number of mines"""
        self.numMines = 3
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        infoObject = pygame.display.Info()
        self.width = infoObject.current_w
        self.height = infoObject.current_h
        """self.width = 1600
        self.height = 900"""

        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))#, pygame.FULLSCREEN)
                                                          
    def MainLoop(self):
        """This is the Main Loop of the Game"""
        
        """Load All of our Sprites"""
        self.LoadSprites()
        """spawn the mines on random locations"""
        self.SpawnMines(self.numMines, self.snake1, self.snake2)
        """tell pygame to keep sending up keystrokes when they are
        held down"""
        pygame.key.set_repeat(500, 30)
        
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if (event.key == K_KP4):
                        self.snake1.rotate(10)
                    elif(event.key == K_KP6):
                        self.snake1.rotate(-10)
                    elif(event.key == K_KP8):
                        self.snake1.move(event.key)
                    elif(event.key == K_s):
                        self.snake2.rotate(10)
                    elif(event.key == K_f):
                        self.snake2.rotate(-10)
                    elif(event.key == K_e):
                        self.snake2.move(event.key)

                        
                """Check for collision between the submarine and the bullets"""
                amountTorp1 = self.collideWithTorpedo(self.snake1)
                amountTorp2 = self.collideWithTorpedo(self.snake2)

                """Check for collision between the submarine and the mines"""
                colsMines1 = self.collideWithMines(self.snake1)
                colsMines2 = self.collideWithMines(self.snake2)
                if(colsMines1):
                    self.GameoverRestart(1)
                elif(colsMines2):
                    self.GameoverRestart(2)
                elif(self.snake1.collideWithSubmarine(self.snake2)):
                    self.GameoverRestart(0)
                else:
                    self.RespawnTorpedos(amountTorp1+amountTorp2)
                    """Update the amount of pellets eaten"""
                    self.snake1.pellets += amountTorp1
                    self.snake2.pellets += amountTorp2

                    """Do the Drawing"""
                    self.screen.blit(self.background, (0, 0))
                    if pygame.font:
                        font = pygame.font.Font(None, 36)
                        text1 = font.render("Ammo player1 %s" % self.snake1.pellets
                                            , 1, (255, 0, 0))
                        text2 = font.render("Ammo player2 %s" % self.snake2.pellets
                                            , 1, (255, 0, 0))
                        textpos1 = text1.get_rect(centerx=self.background.get_width()/2)
                        textpos2 = text1.get_rect(centerx=self.background.get_width()/2)
                        self.screen.blit(text1, textpos1)
                        self.screen.blit(text2, textpos2)


                    """Display bounding boxes
                    self.DrawBoundingB(self.mine_sprites)
                    self.DrawBoundingB(self.snake_sprites)
                    self.DrawBoundingB(self.pellet_sprites)"""

                    self.pellet_sprites.draw(self.screen)
                    #self.mine_sprites.draw(self.screen)
                    self.snake_sprites.draw(self.screen)
                    pygame.display.flip()

    def DrawBoundingB(self, spritesGroup):
        for x in spritesGroup:
            pygame.draw.rect(self.screen, pygame.Color(255,255,255,1), x.rect)
                    
    def LoadSprites(self):
        """Load the sprites that we need"""
        self.snake_sprites = pygame.sprite.Group()

        self.snake1 = Snake()
        self.snake_sprites.add(pygame.sprite.RenderPlain(self.snake1))
        self.snake2 = Snake()
        self.snake_sprites.add(pygame.sprite.RenderPlain(self.snake2))

        self.snake1.rect.move_ip(0, self.height/2)
        self.snake2.rect.move_ip(self.width-self.snake2.rect.width, self.height/2)
        self.snake1.rotate(180)

        """Create the Pellet group"""
        self.pellet_sprites = pygame.sprite.Group()
        """Create all of the pellets and add them to the 
        pellet_sprites group"""

        for x in range(self.numTopedos):
            width = randint(0,self.width)
            height = randint(0,self.height)
            self.pellet_sprites.add(Pellet(pygame.Rect(width, height, 64, 64)))


    def RespawnTorpedos(self, num):
        for i in range(num):
            width = randint(0,self.width)
            height = randint(0,self.height)
            self.pellet_sprites.add(Pellet(pygame.Rect(width, height, 64, 64)))

    def SpawnMines(self, num, submarine1, submarine2):
        """Create the mines group"""
        self.mine_sprites = pygame.sprite.Group()

        for i in range(num):
            width = randint(0,self.width)
            height = randint(0,self.height)
            mine = Mine(pygame.Rect(width, height, 10, 10))
            collide = pygame.sprite.collide_rect(mine, submarine1)
            collide += pygame.sprite.collide_rect(mine, submarine2)
            while(collide):
                width = randint(0,self.width)
                height = randint(0,self.height)
                mine = Mine(pygame.Rect(width, height, 10, 10))
                collide = pygame.sprite.collide_rect(mine, submarine1)
                collide += pygame.sprite.collide_rect(mine, submarine2)

            self.mine_sprites.add(mine)

    def collideWithMines(self, snake):
        """check if there is a collision between mines and submarine"""
        for mine in self.mine_sprites:
            offset_x, offset_y = (mine.rect.left - snake.rect.left), (mine.rect.top - snake.rect.top)
            if (snake.hitmask.overlap(mine.hitmask, (offset_x, offset_y)) != None):
                return True
        return False

    def collideWithTorpedo(self, snake):
        """amount of picked up torpedo's"""
        amountTorp = 0
        for torpedo in self.pellet_sprites:
            offset_x, offset_y = (torpedo.rect.left - snake.rect.left), (torpedo.rect.top - snake.rect.top)
            if (snake.hitmask.overlap(torpedo.hitmask, (offset_x, offset_y)) != None):
                """remove torpedo"""
                self.pellet_sprites.remove(torpedo)
                amountTorp = amountTorp + 1

        return amountTorp


    def GameoverRestart(self, loser):
        """hit a mine -> gameover"""
        """make screen black"""
        self.screen.blit(self.background, (0, 0))
        if pygame.font:
            font = pygame.font.Font(None, 80)
            if(loser == 1):
                text = font.render('Game Over, player 2 won!!!', 1, (255, 0, 0))
            elif(loser == 2):
                text = font.render('Game Over, player 1 won!!!', 1, (255, 0, 0))
            elif(loser == 0):
                text = font.render('Crash! Both the submarines sank!', 1, (255, 0, 0))
            else:
                text = font.render('No winner, something went wrong', 1, (255, 0, 0))
            text2 = font.render('Press a button to continue', 1, (255, 0, 0))
            textpos = text.get_rect(centerx=self.background.get_width()/2)
            textpos.centery = self.background.get_height()/2 - (textpos.height + 5)
            textpos2 = text.get_rect(centerx=self.background.get_width()/2, centery=self.background.get_height()/2)
            self.screen.blit(text, textpos)
            self.screen.blit(text2, textpos2)
            pygame.display.flip()

        """wait a couple of seconds"""
        pygame.time.wait(300)

        """wait for a keypress to restart"""
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            """start a new game"""
            """Load All of our Sprites"""
            self.LoadSprites()
            """pawn the mines on random locations"""
            self.SpawnMines(self.numMines, self.snake1, self.snake2)





class Snake(pygame.sprite.Sprite):
    """This is our snake that will move around the screen"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('images\submarine3.png',-1)
        self.pellets = 0
        """Set the number of Pixels to move each time"""
        self.x_dist = 8
        self.y_dist = 8
        self.angle = 0
        self.baseimage = self.image
        self.hitmask = pygame.mask.from_surface(self.image)

    def move(self, key):
        """Move your self in one of the 4 directions according to key"""
        """Key is the pyGame define for either up,down,left, or right key
        we will adjust outselfs in that direction"""
        xMove = 0
        yMove = 0

        if (key == K_KP8 or key == K_e):
            xMove = self.x_dist * math.sin(math.radians(self.angle-90))
            yMove = self.y_dist * math.cos(math.radians(self.angle-90))
        #self.rect = self.rect.move(xMove,yMove)
        self.rect.move_ip(xMove, yMove)
        self.refreshmask()

    def rotate(self, angle):
        """rotate an image while keeping its center"""
        self.angle = self.angle + angle
        rot_image = pygame.transform.rotate(self.baseimage, self.angle)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        self.image = rot_image
        self.rect = rot_rect
        self.refreshmask()

    def refreshmask(self):
        self.hitmask = pygame.mask.from_surface(self.image)


    def collideWithSubmarine(self, submarine):
        offset_x, offset_y = (self.rect.left - submarine.rect.left), (self.rect.top - submarine.rect.top)
        if (submarine.hitmask.overlap(self.hitmask, (offset_x, offset_y)) != None):
            return True
        return False

class Pellet(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('images\\torpedo4.png',-1)
        if rect != None:
            self.rect = self.image.get_rect(center=rect.center)
        else:
            self.rect = self.image.get_rect()

        self.hitmask = pygame.mask.from_surface(self.image)

class Mine(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('images\\pong.png',-1)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        if rect != None:
            self.rect = self.image.get_rect(center=rect.center)
        else:
            self.rect = self.image.get_rect()

        self.hitmask = pygame.mask.from_surface(self.image)




if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
       
