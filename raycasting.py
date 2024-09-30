import pygame
import math
from utils import TILE_SIZE, game_map

def cast_rays(screen, player):
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    NUM_RAYS = 240
    DELTA_ANGLE = FOV / NUM_RAYS
    MAX_DEPTH = 300
    DISTANCE_PROJ_PLANE = (screen.get_width() // 2) / math.tan(HALF_FOV)

    for ray in range(NUM_RAYS):
        ray_angle = player.angle - HALF_FOV + ray * DELTA_ANGLE
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        for depth in range(MAX_DEPTH):
            target_x = player.pos[0] + depth * cos_a
            target_y = player.pos[1] + depth * sin_a
            map_x = int(target_x // TILE_SIZE)
            map_y = int(target_y // TILE_SIZE)

            if 0 <= map_x < len(game_map[0]) and 0 <= map_y < len(game_map):
                if game_map[map_y][map_x] == 1:
                    depth *= math.cos(player.angle - ray_angle)
                    proj_height = TILE_SIZE * DISTANCE_PROJ_PLANE / (depth + 0.0001)
                    color = 255 / (1 + depth * depth * 0.0001)
                    pygame.draw.rect(screen, (color, color, color),
                                     (ray * (screen.get_width() // NUM_RAYS), screen.get_height() // 2 - proj_height // 2,
                                      screen.get_width() // NUM_RAYS, proj_height))
                    break

def cast_ray_for_enemy(enemy, player):
    """Cast a ray from the enemy to the player and check if walls block the view."""
    dx = player.pos[0] - enemy.pos[0]
    dy = player.pos[1] - enemy.pos[1]
    distance = math.hypot(dx, dy)

    steps = int(distance // TILE_SIZE)

    for step in range(steps):
        check_x = enemy.pos[0] + (dx / steps) * step
        check_y = enemy.pos[1] + (dy / steps) * step
        map_x = int(check_x // TILE_SIZE)
        map_y = int(check_y // TILE_SIZE)

        if 0 <= map_x < len(game_map[0]) and 0 <= map_y < len(game_map):
            if game_map[map_y][map_x] == 1:
                return False  # Wall blocks the view

    return True  # No walls block the view
