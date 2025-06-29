import pygame
from settings import *
import math
from ray import Ray
class RayCaster:
    def __init__(self,player,screen):
        self.rays=[]
        self.player = player
        self.screen = screen
        
    def castRays(self):
        self.rays = []
        angle = self.player.playerAngle -  FOV/2 
        for i in range(NUMRAYS):
            self.rays.append(Ray(self.player,angle,self.screen,map))
            angle += FOV/NUMRAYS
        for ray in self.rays:
            ray.render2D()   
            
    
    
    
        