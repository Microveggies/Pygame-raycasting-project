import pygame
import math
from utils import TILE_SIZE, check_collision, game_map

class BulletManager:
    def __init__(self):
        self.bullets = []
        self.bullet_speed = 10
        self.bullet_size = 5

    def shoot_bullet(self, player):
        if player.ammo_in_magazine > 0:
            bullet_pos = list(player.pos)  # Spawn bullet at player's current position
            bullet_angle = player.angle
            self.bullets.append({'pos': bullet_pos, 'angle': bullet_angle})
            player.ammo_in_magazine -= 1

    def update_bullets(self, player, enemy, screen):
        for bullet in self.bullets[:]:
            bullet_angle = bullet['angle']
            sin_a = math.sin(bullet_angle)
            cos_a = math.cos(bullet_angle)

            # Move the bullet in its trajectory
            bullet['pos'][0] += self.bullet_speed * cos_a
            bullet['pos'][1] += self.bullet_speed * sin_a

            # Check for collision with walls
            bullet_x = int(bullet['pos'][0] // TILE_SIZE)
            bullet_y = int(bullet['pos'][1] // TILE_SIZE)

            if 0 <= bullet_x < len(game_map[0]) and 0 <= bullet_y < len(game_map):
                if game_map[bullet_y][bullet_x] == 1:
                    self.bullets.remove(bullet)
                    continue

            # Check for collision with the enemy
            dx = bullet['pos'][0] - enemy.pos[0]
            dy = bullet['pos'][1] - enemy.pos[1]
            if math.hypot(dx, dy) < 20 and enemy.active:
                enemy.health -= 10
                self.bullets.remove(bullet)
                if enemy.health <= 0:
                    enemy.active = False
                continue

            # Render the bullet in 3D space
            self.render_bullet_3d(screen, player, bullet)

    def render_bullet_3d(self, screen, player, bullet):
        dx = bullet['pos'][0] - player.pos[0]
        dy = bullet['pos'][1] - player.pos[1]
        distance_to_bullet = math.hypot(dx, dy)
        angle_to_bullet = math.atan2(dy, dx) - player.angle

        # Normalize the angle to be between -π and π
        angle_to_bullet = (angle_to_bullet + math.pi) % (2 * math.pi) - math.pi

        # Render the bullet only if it is within the player's FOV
        if abs(angle_to_bullet) < math.pi / 3:
            # Remove fisheye effect
            distance_to_bullet *= math.cos(angle_to_bullet)

            # Calculate the projection height for the bullet
            bullet_proj_height = TILE_SIZE * 300 / (distance_to_bullet + 0.0001)

            # Calculate the screen position for the bullet
            screen_x = (angle_to_bullet + math.pi / 3) * (screen.get_width() / (2 * math.pi / 3))

            # Render the bullet as a red rectangle
            pygame.draw.rect(screen, (255, 0, 0), (int(screen_x) - bullet_proj_height // 2,
                                                   screen.get_height() // 2 - bullet_proj_height // 2,
                                                   bullet_proj_height, bullet_proj_height))
