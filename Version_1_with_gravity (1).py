
import math
import os
import random
import pygame

pygame.init()

# Create fullscreen window at desktop resolution
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()

# --- Configuration ---
FPS = 60
WORLD_HEIGHT_TILES = 64

scale_octave1 = 100
amplitude_octave1 = 15
scale_octave2 = 10
amplitude_octave2 = 5
scale_octave3 = 3
amplitude_octave3 = 3

# seed values
seed_values_octave_1 = [random.uniform(-1, 1) for _ in range(100)]
seed_values_octave_2 = [random.uniform(-1, 1) for _ in range(99)]
seed_values_octave_3 = [random.uniform(-1, 1) for _ in range(98)]

# Physics
gravity = 0.6
jump_speed = 12.5
move_acceleration = 0.7
max_run_speed = 6.0
max_fall_speed = 16.0
air_drag = 0.92
ground_friction = 0.78

# Player settings
player_size = 40

white = (255, 255, 255)
black = (0, 0, 0)
debug_red = (220, 40, 40)

speed = 60

# Terrain storage:
# terrain[x] = list of 64 tile values, bottom-up (index 0 = bottom row)
terrain = {}

def load_tile_image(path, fallback_color):
    """Load a tile image or create a simple fallback tile if the file is missing."""
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (block_size, block_size))
    except Exception:
        surf = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
        surf.fill(fallback_color)
        pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 1)
        return surf

def get_noise_octave1(pos_for_noise):
    p1 = math.floor(pos_for_noise) % len(seed_values_octave_1)
    p2 = (p1 + 1) % len(seed_values_octave_1)
    frac = pos_for_noise - math.floor(pos_for_noise)
    t = frac * frac * (3 - 2 * frac)
    return seed_values_octave_1[p1] * (1 - t) + seed_values_octave_1[p2] * t

def get_noise_octave2(pos_for_noise):
    p1 = math.floor(pos_for_noise) % len(seed_values_octave_2)
    p2 = (p1 + 1) % len(seed_values_octave_2)
    frac = pos_for_noise - math.floor(pos_for_noise)
    t = frac * frac * (3 - 2 * frac)
    return seed_values_octave_2[p1] * (1 - t) + seed_values_octave_2[p2] * t

def get_noise_octave3(pos_for_noise):
    p1 = math.floor(pos_for_noise) % len(seed_values_octave_3)
    p2 = (p1 + 1) % len(seed_values_octave_3)
    frac = pos_for_noise - math.floor(pos_for_noise)
    t = frac * frac * (3 - 2 * frac)
    return seed_values_octave_3[p1] * (1 - t) + seed_values_octave_3[p2] * t

def generate_column(x_col):
    """Generate one terrain column as a bottom-up list of tile IDs."""
    x_octave1 = x_col / scale_octave1
    x_octave2 = x_col / scale_octave2
    x_octave3 = x_col / scale_octave3

    noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(
        get_noise_octave2(x_octave2) * amplitude_octave2
    )
    if noise_value > 10:
        noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
    elif noise_value > 5:
        noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)

    surface = 40 + noise_value
    surface = max(2, min(WORLD_HEIGHT_TILES - 1, surface))

    column = [0 for _ in range(WORLD_HEIGHT_TILES)]
    column[surface] = 1
    column[surface - 1] = 2
    column[surface - 2] = 2
    for i in range(surface - 2):
        column[i] = 3
    return column

def ensure_column(x_col):
    if x_col not in terrain:
        terrain[x_col] = generate_column(x_col)
    return terrain[x_col]

def highest_solid_tile_top_y(x_col):
    """Return the top y-coordinate (world pixels, top-left system) of the terrain surface tile."""
    column = ensure_column(x_col)
    topmost_bottom_index = max(i for i, tile in enumerate(column) if tile != 0)
    top_row = WORLD_HEIGHT_TILES - 1 - topmost_bottom_index
    return top_row * block_size

def solid_tiles_in_rect(rect):
    """Return solid tile rectangles overlapping a world-space rect."""
    tiles = []
    left_col = math.floor(rect.left / block_size) - 1
    right_col = math.floor((rect.right - 1) / block_size) + 1
    top_row = math.floor(rect.top / block_size) - 1
    bottom_row = math.floor((rect.bottom - 1) / block_size) + 1

    for x_col in range(left_col, right_col + 1):
        column = ensure_column(x_col)
        for row_top in range(top_row, bottom_row + 1):
            if row_top < 0 or row_top >= WORLD_HEIGHT_TILES:
                continue
            bottom_index = WORLD_HEIGHT_TILES - 1 - row_top
            if column[bottom_index] == 0:
                continue
            tiles.append(pygame.Rect(x_col * block_size, row_top * block_size, block_size, block_size))
    return tiles

def move_and_collide(player_rect, vel_x, vel_y):
    """Move the player rectangle and resolve collisions separately on X and Y."""
    on_ground = False

    # Horizontal movement
    player_rect.x += int(round(vel_x))
    for tile in solid_tiles_in_rect(player_rect):
        if player_rect.colliderect(tile):
            if vel_x > 0:
                player_rect.right = tile.left
            elif vel_x < 0:
                player_rect.left = tile.right
            vel_x = 0

    # Vertical movement
    player_rect.y += int(round(vel_y))
    for tile in solid_tiles_in_rect(player_rect):
        if player_rect.colliderect(tile):
            if vel_y > 0:
                player_rect.bottom = tile.top
                on_ground = True
            elif vel_y < 0:
                player_rect.top = tile.bottom
            vel_y = 0

    return player_rect, vel_x, vel_y, on_ground

# --- Terrain generation ---
# Generate a reasonable starting area.
for x in range(-60, 61):
    ensure_column(x)

# Load textures after pygame.init()
block_size = screen_height // 36
stein_img = load_tile_image("stein.jpg", (110, 110, 110))
gras_img = load_tile_image("gras.jpg", (80, 170, 70))
erde_img = load_tile_image("erde.jpg", (130, 90, 50))

# Resize again in case block_size was not known earlier for fallback tiles
stein_img = pygame.transform.smoothscale(stein_img, (block_size, block_size))
gras_img = pygame.transform.smoothscale(gras_img, (block_size, block_size))
erde_img = pygame.transform.smoothscale(erde_img, (block_size, block_size))

clock = pygame.time.Clock()

# Player state in world coordinates
player_rect = pygame.Rect(0, 0, player_size, player_size)
player_rect.bottom = highest_solid_tile_top_y(0)
player_rect.centerx = 0

vel_x = 0.0
vel_y = 0.0
on_ground = False

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w):
                if on_ground:
                    vel_y = -jump_speed
                    on_ground = False

    keys = pygame.key.get_pressed()

    # Horizontal movement input
    if keys[pygame.K_a]:
        vel_x -= move_acceleration
    if keys[pygame.K_d]:
        vel_x += move_acceleration

    # Optional fast-fall
    if keys[pygame.K_s]:
        vel_y += gravity * 0.5

    # Gravity
    vel_y += gravity
    if vel_y > max_fall_speed:
        vel_y = max_fall_speed

    # Clamp horizontal speed
    if vel_x > max_run_speed:
        vel_x = max_run_speed
    elif vel_x < -max_run_speed:
        vel_x = -max_run_speed

    # Friction / air drag
    if on_ground and not (keys[pygame.K_a] or keys[pygame.K_d]):
        vel_x *= ground_friction
    else:
        vel_x *= air_drag

    # Move and collide
    player_rect, vel_x, vel_y, on_ground = move_and_collide(player_rect, vel_x, vel_y)

    # Make sure terrain is generated a bit ahead of the player
    player_col = math.floor(player_rect.centerx / block_size)
    for x in range(player_col - 50, player_col + 51):
        ensure_column(x)

    # Camera follows the player
    camera_x = player_rect.centerx - screen_width // 2
    camera_y = player_rect.centery - screen_height // 2

    # Draw background
    screen.fill(white)

    # Draw visible terrain only
    start_col = math.floor(camera_x / block_size) - 2
    end_col = math.floor((camera_x + screen_width) / block_size) + 2

    for x_col in range(start_col, end_col + 1):
        column = ensure_column(x_col)
        for bottom_index, tile_type in enumerate(column):
            if tile_type == 0:
                continue

            row_top = WORLD_HEIGHT_TILES - 1 - bottom_index
            draw_x = x_col * block_size - camera_x
            draw_y = row_top * block_size - camera_y

            if draw_x < -block_size or draw_x > screen_width:
                continue
            if draw_y < -block_size or draw_y > screen_height:
                continue

            if tile_type == 1:
                screen.blit(gras_img, (draw_x, draw_y))
            elif tile_type == 2:
                screen.blit(erde_img, (draw_x, draw_y))
            elif tile_type == 3:
                screen.blit(stein_img, (draw_x, draw_y))

    # Draw the player
    player_screen_rect = player_rect.move(-camera_x, -camera_y)
    pygame.draw.rect(screen, black, player_screen_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
