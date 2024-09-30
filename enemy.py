import pygame
import math
from utils import check_collision, TILE_SIZE, game_map

class Enemy:
    def __init__(self, start_pos, speed, health, player):
        # Ensure the enemy spawns in a valid location and far enough from the player
        self.pos = self.find_valid_spawn(player)
        self.speed = speed
        self.health = health
        self.active = True
        self.damage = 5
        self.damage_interval = 60
        self.damage_timer = 0
        self.fov = math.pi / 4  # 90-degree field of vision

        # Debugging
        print(f"Enemy spawned at: {self.pos}")

    def find_valid_spawn(self, player):
        """Find a valid spawn point that is far enough from the player."""
        for y in range(len(game_map)):
            for x in range(len(game_map[0])):
                if game_map[y][x] == 0:  # 0 means open space
                    spawn_x = x * TILE_SIZE + TILE_SIZE // 2
                    spawn_y = y * TILE_SIZE + TILE_SIZE // 2
                    distance_to_player = math.hypot(spawn_x - player.pos[0], spawn_y - player.pos[1])

                    # Ensure the enemy spawns at least 100 units away from the player
                    if distance_to_player > 100:
                        return [spawn_x, spawn_y]

        # Fallback spawn if no valid space is found (shouldn't happen)
        print("No valid spawn point found. Falling back to default spawn.")
        return [TILE_SIZE * 2, TILE_SIZE * 2]

    def update(self, player):
        if self.active:
            # Check if the player is in the enemy's FOV and not blocked by walls
            if self.is_player_in_fov(player) and self.cast_ray_for_enemy(player):
                # Move towards the player
                dx = player.pos[0] - self.pos[0]
                dy = player.pos[1] - self.pos[1]
                distance_to_player = math.hypot(dx, dy)

                if distance_to_player > 20:  # If far from the player, move toward them
                    self.pos[0] += self.speed * (dx / distance_to_player)
                    self.pos[1] += self.speed * (dy / distance_to_player)
                else:
                    # Deal damage if close
                    if self.damage_timer == 0:
                        player.health -= self.damage
                        self.damage_timer = self.damage_interval
                        print(f"Enemy damaged player. Player health: {player.health}")
                    else:
                        self.damage_timer -= 1

    def is_player_in_fov(self, player):
        # Calculate angle to the player
        dx = player.pos[0] - self.pos[0]
        dy = player.pos[1] - self.pos[1]
        distance = math.hypot(dx, dy)

        if distance == 0:  # Avoid division by zero errors
            print("Error: Distance to player is zero!")
            return False

        angle_to_player = math.atan2(dy, dx) - self.get_angle()

        # Normalize angle to be within -π and π
        angle_to_player = (angle_to_player + math.pi) % (2 * math.pi) - math.pi

        # Check if player is within the enemy's FOV
        in_fov = abs(angle_to_player) < self.fov / 2
        print(f"Player in FOV: {in_fov}")
        return in_fov

    def get_angle(self):
        # Assuming the enemy faces along the x-axis
        return math.atan2(0, 1)

    def render(self, screen, player):
        if self.active:
            # Render the enemy only if it's within FOV and not blocked by walls
            dx = self.pos[0] - player.pos[0]
            dy = self.pos[1] - player.pos[1]
            distance_to_enemy = math.hypot(dx, dy)
            angle_to_enemy = math.atan2(dy, dx) - player.angle

            # Avoid division by zero errors
            if distance_to_enemy == 0:
                return

            # Only render the enemy if within the player's FOV
            if abs(angle_to_enemy) < math.pi / 3 and self.cast_ray_for_enemy(player):
                distance_to_enemy *= math.cos(angle_to_enemy)
                enemy_proj_height = TILE_SIZE * 300 / (distance_to_enemy + 0.0001)
                screen_x = (angle_to_enemy + math.pi / 3) * (screen.get_width() / (2 * math.pi / 3))

                pygame.draw.rect(screen, (0, 255, 0), (int(screen_x) - enemy_proj_height // 2,
                                                       screen.get_height() // 2 - enemy_proj_height // 2,
                                                       enemy_proj_height, enemy_proj_height))

    def cast_ray_for_enemy(self, player):
        """Cast a ray from the enemy to the player and check if walls block the view."""
        dx = player.pos[0] - self.pos[0]
        dy = player.pos[1] - self.pos[1]
        distance = math.hypot(dx, dy)

        if distance == 0:  # Avoid division by zero
            return False

        steps = int(distance // TILE_SIZE)

        for step in range(steps):
            check_x = self.pos[0] + (dx / steps) * step
            check_y = self.pos[1] + (dy / steps) * step
            map_x = int(check_x // TILE_SIZE)
            map_y = int(check_y // TILE_SIZE)

            if 0 <= map_x < len(game_map[0]) and 0 <= map_y < len(game_map):
                if game_map[map_y][map_x] == 1:
                    print("Ray blocked by wall.")
                    return False  # Wall blocks the view

        print("Ray to player is clear.")
        return True  # No walls block the view
