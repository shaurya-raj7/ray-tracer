import pygame
from settings import *
from player import Player
import sys
from raycaster import RayCaster
import math
from ray import Ray



class Game:
    def __init__(self):
        pygame.init()
        self.Screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.FPS = FPS
        self.player = Player(self.Screen,map)
        self.rayCaster = RayCaster(self.player,self.Screen)
        #self.ray = Ray(self.player,math.pi/6,self.Screen,map)
       
        
        
    def run(self):
        while self.running:
            
            #-----inputs------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                
            
            
            self.update()
            
         
           
    def update(self):
        
        
        
        self.Screen.fill((BG_COLOR)) 
        
        for i in range(12):
            for j in range (18):
                Color = (0,0,0) if map[i][j] == 1 else (240,240,240)
                pygame.draw.rect(self.Screen,Color,(j*TILESIZE , i* TILESIZE,TILESIZE-1,TILESIZE-1))
        
        
            
        
        self.player.render()
        self.rayCaster.castRays()
        
       # self.ray.render2D()
        
        dt = self.clock.tick(self.FPS)/1000
        
        pygame.display.update()
        self.player.update(dt)



game = Game()
game.run()