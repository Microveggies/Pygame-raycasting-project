import pygame
import math
from utils import check_collision

class Player:
    def __init__(self, start_pos, speed):
        self.pos = start_pos
        self.angle = 0
        self.speed = speed
        self.health = 100
        self.ammo_in_magazine = 10
        self.ammo_reserves = 30
        self.max_magazine = 10

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Move forward
            new_x = self.pos[0] + self.speed * math.cos(self.angle)
            new_y = self.pos[1] + self.speed * math.sin(self.angle)
            if check_collision(new_x, new_y):
                self.pos[0] = new_x
                self.pos[1] = new_y
        if keys[pygame.K_s]:  # Move backward
            new_x = self.pos[0] - self.speed * math.cos(self.angle)
            new_y = self.pos[1] - self.speed * math.sin(self.angle)
            if check_collision(new_x, new_y):
                self.pos[0] = new_x
                self.pos[1] = new_y
        if keys[pygame.K_a]:  # Rotate left
            self.angle -= 0.05
        if keys[pygame.K_d]:  # Rotate right
            self.angle += 0.05

        # Normalize player_angle to be between -π and π
        self.angle = (self.angle + math.pi) % (2 * math.pi) - math.pi

    def reload(self):
        ammo_needed = self.max_magazine - self.ammo_in_magazine
        ammo_to_reload = min(ammo_needed, self.ammo_reserves)
        self.ammo_in_magazine += ammo_to_reload
        self.ammo_reserves -= ammo_to_reload
