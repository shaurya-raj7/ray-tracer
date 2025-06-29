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
        # Initialize with dummy values; these will be updated in render2D
        self.endpos_coords = (0, 0)
        self.distance = 0

    def render2D(self):
        
        # Re-calculate the ray's end position and distance for the current frame
        self.endpos_coords, self.distance = self.determineEndPos()
        # Draw the line using the updated end position
        pygame.draw.line(self.screen,PLAYER_COLOR,(self.player.playerX+ PLAYERSIZE/2,self.player.playerY+ PLAYERSIZE/2),self.endpos_coords)
        
   
        
        
    def render3D(self,intialpos):
        # The distance is now correctly updated and stored in self.distance
        # You can use self.distance here for 3D rendering
        # For example: wall_height = (TILESIZE / self.distance) * DISTANCE_TO_PROJECTION_PLANE
        self.endpos_coords, self.distance = self.determineEndPos()
        wall_height = TILESIZE/self.distance * distncetoprojection
        pygame.draw.rect(self.screen,PLAYER_COLOR,(intialpos,HEIGHT//2 - wall_height//2,RES,wall_height))
        
    def normalizeAngle(self):
        # Normalize the angle to be within [0, 2*pi)
        self.angle = self.angle % math.tau
        if self.angle < 0:
            self.angle = 2 * math.pi + self.angle

    def determineEndPos(self):
        # Small epsilon to handle floating point precision and near-zero/infinite slopes
        epsilon = 1e-6

        # Determine ray direction based on angle
        # Looking up if angle is between pi and 2*pi
        looking_up = (self.angle > math.pi and self.angle < 2 * math.pi)
        # Looking right if angle is between 0 and pi/2, or 3*pi/2 and 2*pi
        looking_right = (self.angle > 0 and self.angle < math.pi / 2) or \
                        (self.angle > 3 * math.pi / 2 and self.angle < 2 * math.pi)

        # --- Horizontal collision detection ---
        horx, hory = float('inf'), float('inf')
        hordistance = float('inf')

        # Check if the ray has a vertical component (not perfectly horizontal)
        if abs(math.sin(self.angle)) > epsilon:
            # Calculate the initial y-coordinate of the first horizontal grid line intersection
            if looking_up:
                # Go to the grid line just above the player's current tile row
                hory = getCurrentTile(self.player.playerX, self.player.playerY)[1] * TILESIZE - epsilon
            else: # looking down
                # Go to the grid line just below the player's current tile row
                hory = getCurrentTile(self.player.playerX, self.player.playerY)[1] * TILESIZE + TILESIZE + epsilon

            # Calculate the corresponding x-coordinate using the ray equation
            horx = self.player.playerX + (hory - self.player.playerY) / math.tan(self.angle)

            # Determine step sizes for subsequent horizontal grid lines
            delta_y = -TILESIZE if looking_up else TILESIZE
            delta_x = delta_y / math.tan(self.angle) # Maintain the slope

            # Horizontal ray traversal loop
            while True:
                # Adjust map Y-coordinate to check the tile in the direction of movement
                # If looking up, check the tile above the current grid line
                map_check_hory = hory - 1 if looking_up else hory
                current_tile_x, current_tile_y = getCurrentTile(horx, map_check_hory)

                # Check if current tile coordinates are within map bounds
                if not (0 <= current_tile_y < len(self.map) and 0 <= current_tile_x < len(self.map[0])):
                    break # Ray went off map boundaries

                # Check if current tile is a wall (value is 1)
                if self.map[current_tile_y][current_tile_x] == 1:
                    hordistance = math.sqrt((self.player.playerX - horx)**2 + (self.player.playerY - hory)**2)
                    break # Wall found

                # Move to the next horizontal grid line
                horx += delta_x
                hory += delta_y

                # Prevent infinite loops for very long rays (e.g., in open areas)
                # Use WIDTH*2 or HEIGHT*2 as a proxy for a reasonable max distance
                if abs(self.player.playerX - horx) > WIDTH * 2 or abs(self.player.playerY - hory) > HEIGHT * 2:
                    break


        # --- Vertical collision detection ---
        verx, very = float('inf'), float('inf')
        verdistance = float('inf')

        # Check if the ray has a horizontal component (not perfectly vertical)
        if abs(math.cos(self.angle)) > epsilon:
            # Calculate the initial x-coordinate of the first vertical grid line intersection
            if looking_right:
                # Go to the grid line just right of the player's current tile column
                verx = getCurrentTile(self.player.playerX, self.player.playerY)[0] * TILESIZE + TILESIZE + epsilon
            else: # looking left
                # Go to the grid line just left of the player's current tile column
                verx = getCurrentTile(self.player.playerX, self.player.playerY)[0] * TILESIZE - epsilon

            # Calculate the corresponding y-coordinate using the ray equation
            very = self.player.playerY + (verx - self.player.playerX) * math.tan(self.angle)

            # Determine step sizes for subsequent vertical grid lines
            delta_x = TILESIZE if looking_right else -TILESIZE
            delta_y = delta_x * math.tan(self.angle) # Maintain the slope

            # Vertical ray traversal loop
            while True:
                # Adjust map X-coordinate to check the tile in the direction of movement
                # If looking left, check the tile left of the current grid line
                map_check_verx = verx - 1 if not looking_right else verx
                current_tile_x, current_tile_y = getCurrentTile(map_check_verx, very)

                # Check if current tile coordinates are within map bounds
                if not (0 <= current_tile_y < len(self.map) and 0 <= current_tile_x < len(self.map[0])):
                    break # Ray went off map boundaries

                # Check if current tile is a wall (value is 1)
                if self.map[current_tile_y][current_tile_x] == 1:
                    verdistance = math.sqrt((self.player.playerX - verx)**2 + (self.player.playerY - very)**2)
                    break # Wall found

                # Move to the next vertical grid line
                verx += delta_x
                very += delta_y

                # Prevent infinite loops for very long rays
                if abs(self.player.playerX - verx) > WIDTH * 2 or abs(self.player.playerY - very) > HEIGHT * 2:
                    break

        # Compare distances and return the closest hit point and its distance
        if hordistance <= verdistance:
            self.distance = hordistance # Correctly set instance variable before returning
            return (horx, hory), hordistance
        else:
            self.distance = verdistance # Correctly set instance variable before returning
            return (verx, very), verdistance