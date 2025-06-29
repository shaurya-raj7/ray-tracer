import pygame
from settings import *
import math
class Ray:
    def __init__(self,player,angle,screen,map):
        self.player = player 
        self.angle = angle
        self.screen = screen 
        self.map = map
        self.normalizeAngle()
        self.endpos = self.determineEndPos()
        self.distance = 0
        
    def render2D(self):
        
        self.angle = self.player.playerAngle
        pygame.draw.line(self.screen,PLAYER_COLOR,(self.player.playerX+ PLAYERSIZE/2,self.player.playerY+ PLAYERSIZE/2),self.endpos)
    
    def render3D(self):
        distance  = self.endpos[2]
        
        
    def normalizeAngle(self):
        self.angle= self.angle%math.tau
        if self.angle<0:
            self.angle = 2*math.pi + self.angle
        
          
    def determineEndPos(self):
        looking_up = True
        horx=0
        hory=0
    
        m=math.tan(self.angle) + 0.001
        
        
        
        #----- check horizontal collision--------
        
        #----check whether looking up or down
        looking_up = True if (self.angle> math.pi and self.angle<= 2 *math.pi) else False
        ao = -TILESIZE if looking_up else TILESIZE
        bo = -TILESIZE*m if looking_up else TILESIZE*m
        
       
            
        hory =  getCurrentTile(self.player.playerX,self.player.playerY)[1]*TILESIZE -1 if looking_up else (getCurrentTile(self.player.playerX,self.player.playerY))[1]*TILESIZE +TILESIZE
            

        horx = (hory-self.player.playerY+m*self.player.playerX)/m 
            
        while (hory <= HEIGHT and hory>=0) and (horx <= WIDTH and horx>= 0) :
            if self.map[int(hory)//TILESIZE][int(horx)// TILESIZE] == 1:
               
                    
                break
            else:
                hory += ao
                horx += bo
       
        
        
        hordistance = math.sqrt((self.player.playerX- horx)**2 + (self.player.playerY - hory)**2)
        
        
        looking_right = True if ((self.angle>0 and self.angle<= math.pi/2) or (self.angle> math.pi*3/2 and self.angle<= math.pi*2)) else False
        
        verx=0
        very=0
        xo = TILESIZE if looking_right else -TILESIZE
        yo = TILESIZE*m if looking_right else -TILESIZE*m
        
        #----- check vertical collision--------
        
        #----check whether looking right or left
        
        
        verx =  getCurrentTile(self.player.playerX,self.player.playerY+1)[0]*TILESIZE + TILESIZE  if looking_right else (getCurrentTile(self.player.playerX,self.player.playerY+1))[0]*TILESIZE -1
            
        very = m*(verx-self.player.playerX) + self.player.playerY
            
        while (very <= HEIGHT and very>=0) and (verx <= WIDTH and verx>= 0):
            if self.map[int(very)//TILESIZE][int(verx)// TILESIZE] == 1:
                    
                break
            else:
                verx += xo
                very += yo
        
                  
        
        
        verdistance = math.sqrt((self.player.playerX- verx)**2 + (self.player.playerY - very)**2)
        
        if hordistance <= verdistance:
            return (horx,hory)
            self.distance = hordistance
        else:
            return (verx,very,)
            self.distance = verdistance
            
       
        
        
        