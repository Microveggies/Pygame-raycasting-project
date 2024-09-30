import pygame

TILE_SIZE = 64

# Simple map grid (1 = wall, 0 = open space)
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

def check_collision(new_x, new_y):
    map_x = int(new_x // TILE_SIZE)
    map_y = int(new_y // TILE_SIZE)

    if 0 <= map_x < len(game_map[0]) and 0 <= map_y < len(game_map):
        return game_map[map_y][map_x] == 0
    return False

def draw_hud(screen, player, reloading, reload_percentage):
    font = pygame.font.SysFont("Arial", 24)
    ammo_text = font.render(f"Ammo: {player.ammo_in_magazine}/{player.ammo_reserves}", True, (255, 255, 255))
    screen.blit(ammo_text, (screen.get_width() - 200, 10))

    health_bar_width = int(screen.get_width() * 0.15)
    health_bar_fill = int((player.health / 100) * health_bar_width)
    pygame.draw.rect(screen, (255, 0, 0), (screen.get_width() - health_bar_width - 50, 50, health_bar_fill, 20))
    pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() - health_bar_width - 50, 50, health_bar_width, 20), 2)

    if reloading:
        reload_text = font.render(f"Reloading... {int(reload_percentage * 100)}%", True, (255, 255, 0))
        screen.blit(reload_text, (screen.get_width() - 250, 80))

def draw_crosshair(screen):
    pygame.draw.line(screen, (0, 255, 0), (screen.get_width() // 2 - 10, screen.get_height() // 2),
                     (screen.get_width() // 2 + 10, screen.get_height() // 2), 2)
    pygame.draw.line(screen, (0, 255, 0), (screen.get_width() // 2, screen.get_height() // 2 - 10),
                     (screen.get_width() // 2, screen.get_height() // 2 + 10), 2)

def draw_minimap(screen, player, enemy):
    minimap_scale = 10  # Increased scale for larger minimap
    minimap_width = len(game_map[0]) * minimap_scale
    minimap_height = len(game_map) * minimap_scale
    pygame.draw.rect(screen, (0, 0, 0), (10, 10, minimap_width, minimap_height))

    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (255, 255, 255), (10 + x * minimap_scale, 10 + y * minimap_scale, minimap_scale, minimap_scale))

    player_x = 10 + int(player.pos[0] // TILE_SIZE * minimap_scale)
    player_y = 10 + int(player.pos[1] // TILE_SIZE * minimap_scale)
    pygame.draw.circle(screen, (255, 0, 0), (player_x, player_y), 5)

    if enemy.active:
        enemy_x = 10 + int(enemy.pos[0] // TILE_SIZE * minimap_scale)
        enemy_y = 10 + int(enemy.pos[1] // TILE_SIZE * minimap_scale)
        pygame.draw.circle(screen, (0, 255, 0), (enemy_x, enemy_y), 5)
