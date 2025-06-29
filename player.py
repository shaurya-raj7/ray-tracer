import pygame
from settings import *
import math

class Player():
    def __init__(self,Screen,map):
        self.playerX = WIDTH//2- 50
        self.playerY = HEIGHT//2  - 50
        self.tempx = self.playerX
        self.tempy = self.playerY
        self.playerAngle = math.pi/6
        self.Screen = Screen
        self.playerSpeed = 100
        self.playerAngularSpeed = math.pi / 10
        self.map = map
     
        
    def render(self):
        pygame.draw.rect(self.Screen,PLAYER_COLOR,(self.playerX,self.playerY,PLAYERSIZE,PLAYERSIZE))
       
        
        
    def update(self,dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.tempy -= self.playerSpeed*dt
        elif keys[pygame.K_s]:
            self.tempy += self.playerSpeed*dt
        elif keys[pygame.K_a]:
            self.tempx -= self.playerSpeed*dt
        elif keys[pygame.K_d]:
            self.tempx += self.playerSpeed*dt
        
        self.playerAngle += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])* dt* self.playerAngularSpeed 
        self.playerAngle = self.playerAngle% math.tau
        if self.playerAngle<= 0 :
            self.playerAngle = math.tau + self.playerAngle
        
       

       
            
        
        self.playerX = int(self.tempx)
        self.playerY = int(self.tempy)
        
        
        
    
        
            
        
