import pygame
import random
import math

# Create fullscreen window at desktop resolution
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
block_size = screen_height // 36

# --- Configuration ---
FPS = 60

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

# Player settings
player_size = block_size  # Match block size visually
pos_x = 0
pos_y = 45  # Started a bit higher so you don't fall through the initial empty void
mov_x = 0
mov_y = 0
drag = 0.80

# --- Physics Constants ---
GRAVITY = 0.15
JUMP_FORCE = -3.5
is_grounded = False

stein_img = pygame.image.load("stein.jpg").convert_alpha()
stein_img = pygame.transform.smoothscale(stein_img, (block_size, block_size))
gras_img = pygame.image.load("gras.jpg").convert_alpha()
gras_img = pygame.transform.smoothscale(gras_img, (block_size, block_size))
erde_img = pygame.image.load("erde.jpg").convert_alpha()
erde_img = pygame.transform.smoothscale(erde_img, (block_size, block_size))

white = (255, 255, 255)
black = (0, 0, 0)

speed = 60

new_render_positive = 0
new_render_negative = 0
rendering_point = 0
rendering_offset = 0


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


# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
offset = 0

blocks_pos = [[0 for _ in range(64)] for _ in range(84)]

for z in range(84):
    x_octave1 = (z - 42) / scale_octave1
    x_octave2 = (z - 42) / scale_octave2
    x_octave3 = (z - 42) / scale_octave3
    noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(
        get_noise_octave2(x_octave2) * amplitude_octave2)
    if noise_value > 10:
        noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
    elif noise_value > 5:
        noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)

    blocks_pos[z][40 + noise_value] = 1
    blocks_pos[z][40 + noise_value - 1] = 2
    blocks_pos[z][40 + noise_value - 2] = 2
    for i in range(40 + noise_value - 2):
        blocks_pos[z][i] = 3

done = False
while not done:
    screen.fill(white)

    # --- Apply Gravity ---
    if not is_grounded:
        mov_y += GRAVITY

    # Update position coordinates
    pos_x += mov_x
    pos_y += mov_y

    # Horizontal drag handles sliding slowdown
    mov_x *= drag

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        mov_x += 0.1
    if keys[pygame.K_a]:
        mov_x -= 0.1

    # Modified controls: W triggers jumping if grounded instead of free flight
    if keys[pygame.K_w] and is_grounded:
        mov_y = JUMP_FORCE
        is_grounded = False

    # --- Collision Detection Implementation ---
    # Based on render formulas, find the array offset column that matches the center screen player pos
    current_player_z_index = 42 + rendering_offset + round(pos_x)

    # Determine the structural ground index directly underneath the player's position floor
    under_y_index = math.floor(pos_y)

    is_grounded = False
    if 0 <= current_player_z_index < len(blocks_pos):
        if 0 <= under_y_index < 64:
            # Check if the block directly below the player has ground data (value != 0)
            if blocks_pos[current_player_z_index][under_y_index] != 0:
                is_grounded = True
                mov_y = 0
                pos_y = under_y_index + 1  # Snaps player to rest exactly above the block element

    # DRAWING THE BLOCKS
    for z in range(84):
        for y in range(64):
            if blocks_pos[z + rendering_point + rendering_offset][y] == 0:
                continue
            if blocks_pos[z + rendering_point + rendering_offset][y] == 1:
                screen.blit(gras_img, ((z - pos_x + rendering_point) * block_size - block_size * 10,
                                       screen_height - block_size - y * block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 2:
                screen.blit(erde_img, ((z - pos_x + rendering_point) * block_size - block_size * 10,
                                       screen_height - block_size - y * block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 3:
                screen.blit(stein_img, ((z - pos_x + rendering_point) * block_size - block_size * 10,
                                        screen_height - block_size - y * block_size - (pos_y * block_size)))

    pygame.draw.rect(screen, black,
                     (screen_width // 2 - 1 / 2 * block_size, screen_height // 2 - 1 / 2 * block_size, block_size,
                      block_size))

    if pos_x > new_render_positive:
        new_render_positive += 1
        x_octave1 = (42 + new_render_positive) / scale_octave1
        x_octave2 = (42 + new_render_positive) / scale_octave2
        x_octave3 = (42 + new_render_positive) / scale_octave3
        noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(
            get_noise_octave2(x_octave2) * amplitude_octave2)
        if noise_value > 10:
            noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
        elif noise_value > 5:
            noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)
        blocks_pos.append([0 for _ in range(64)])
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value] = 1
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value - 1] = 2
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value - 2] = 3
        for i in range(40 + noise_value - 2):
            blocks_pos[83 + new_render_positive - new_render_negative][i] = 3

    if pos_x <= new_render_negative:
        rendering_offset += 1
        new_render_negative -= 1
        x_octave1 = (-42 + new_render_negative) / scale_octave1
        x_octave2 = (-42 + new_render_negative) / scale_octave2
        x_octave3 = (-42 + new_render_negative) / scale_octave3
        noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(
            get_noise_octave2(x_octave2) * amplitude_octave2)
        if noise_value > 10:
            noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
        elif noise_value > 5:
            noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)
        blocks_pos.insert(0, [0 for _ in range(64)])

        blocks_pos[0][40 + noise_value] = 1
        blocks_pos[0][40 + noise_value - 1] = 2
        blocks_pos[0][40 + noise_value - 2] = 3
        for i in range(40 + noise_value - 2):
            blocks_pos[0][i] = 3

    rendering_point = math.ceil(pos_x)
    pygame.display.flip()
    clock.tick(speed)
pygame.quit()