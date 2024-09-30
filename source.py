import pygame
from player import Player
from enemy import Enemy
from raycasting import cast_rays
from bullet import BulletManager
from utils import draw_hud, draw_crosshair, draw_minimap, TILE_SIZE

# Initialize pygame
pygame.init()

# Set fullscreen mode
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

# Colors
BLACK = (0, 0, 0)
FPS = 60
clock = pygame.time.Clock()

# Initialize player, enemy, and bullet manager
player = Player([100, 100], 3)
enemy = Enemy([300, 300], 1.5, 50,player)
bullet_manager = BulletManager()

# Main loop
running = True
reloading = False  # Flag to indicate if the player is reloading
reload_timer = 0  # Timer for reloading delay
RELOAD_TIME = 120  # Reload time in frames (e.g., 2 seconds at 60 FPS)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not reloading:  # Fire bullet when spacebar is pressed, but not while reloading
                bullet_manager.shoot_bullet(player)
            if event.key == pygame.K_r and not reloading:  # Reload when R is pressed
                reloading = True
                reload_timer = RELOAD_TIME

    screen.fill(BLACK)

    # Handle reloading
    if reloading:
        reload_timer -= 1
        if reload_timer <= 0:
            player.reload()
            reloading = False

    # Move player
    player.move()

    # Cast rays and render walls
    cast_rays(screen, player)

    # Update and render bullets
    bullet_manager.update_bullets(player, enemy, screen)

    # Render and update the enemy
    enemy.update(player)
    enemy.render(screen, player)

    # Draw the HUD, crosshair, and minimap
    draw_hud(screen, player, reloading, reload_timer / RELOAD_TIME)
    draw_crosshair(screen)
    draw_minimap(screen, player, enemy)

    # Update display
    pygame.display.flip()

    # Control FPS
    clock.tick(FPS)

# Quit pygame
pygame.quit()
