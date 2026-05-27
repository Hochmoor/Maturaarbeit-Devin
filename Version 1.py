import pygame
import random
import math

# Create fullscreen window at desktop resolution
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
block_size = screen_height // 36

# --- Configuration ---
FPS = 60
SCALE = 0.005  # How "stretched" the hills are (Frequency)
AMPLITUDE = 15  # How tall the hills are
SPEED = 2  # Scrolling speed

# --- Simple 1D Noise Logic ---
# function to simulate the Perlin effect.
seed_values = [random.uniform(-1, 1) for _ in range(1000)]

# Player settings
player_size = 40
pos_x = 0
pos_y = -20
mov_x = 0
mov_y = 0
drag = 0.80

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


def get_noise(x):
    # Determine the two points on our "ruler" we are between
    p1 = math.floor(x) % 1000
    p2 = (p1 + 1) % 1000

    # How far are we between those points (0.0 to 1.0)
    frac = x - math.floor(x)

    # Smoothstep interpolation (the "Fade" function)
    t = frac * frac * (3 - 2 * frac)

    # Blend the two random values
    return seed_values[p1] * (1 - t) + seed_values[p2] * t


# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
offset = 0

blocks_pos = [[0 for _ in range(64)] for _ in range(84)]
print(blocks_pos)

for z in range(84):
    x = (z - 42) / 10
    noise_value = round(get_noise(x) * AMPLITUDE)
    print(noise_value)
    blocks_pos[z][40 + noise_value] = 1
    blocks_pos[z][40 + noise_value - 1 ] = 2
    blocks_pos[z][40 + noise_value - 2 ] = 2
    for i in range(40 + noise_value - 2):
        blocks_pos[z][i] = 3

print(blocks_pos)

done = False
while not done:
    screen.fill(white)

    pos_x += mov_x
    pos_y += mov_y

    mov_x *= drag
    mov_y *= drag

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True  # ESC to quit fullscreen

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        mov_x += 0.1
    if keys[pygame.K_a]:
        mov_x -= 0.1
    if keys[pygame.K_s]:
        mov_y += 0.1
    if keys[pygame.K_w]:
        mov_y -= 0.1

    print(pos_x, pos_y)



    # DRAWING THE BLOCKS
    for z in range(84):
        for y in range(64):
            if blocks_pos[z + rendering_point][y] == 0:
                continue

            if blocks_pos[z + rendering_point][y] == 1:
                screen.blit(gras_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point][y] == 2:
                screen.blit(erde_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point][y] == 3:
                screen.blit(stein_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size)))


    pygame.draw.rect(screen, black, (screen_width//2 - 1/2 * block_size, screen_height//2 - 1/2 * block_size, block_size,block_size))

    if pos_x > new_render_positive:
        new_render_positive += 1
        print("NRP and pos_x", new_render_positive, pos_x)
        x = (42 + new_render_positive) / 10
        noise_value = round(get_noise(x) * AMPLITUDE)
        print(noise_value)
        blocks_pos.append([0 for _ in range(64)])
        print("new blocks pos", blocks_pos)
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value] = 1
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value - 1] = 2
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value - 2] = 2
        for i in range(40 + noise_value - 2):
                blocks_pos[83 + new_render_positive - new_render_negative][i] = 3

    if pos_x <= new_render_negative:
        new_render_negative -= 1
        print(new_render_negative)
        x = (-42 + new_render_negative) / 10
        noise_value = round(get_noise(x) * AMPLITUDE)
        print(noise_value)
        blocks_pos.insert(0,[0 for _ in range(64)])

        blocks_pos[0][40 + noise_value] = 1
        blocks_pos[0][40 + noise_value - 1] = 2
        blocks_pos[0][40 + noise_value - 2] = 2
        for i in range(40 + noise_value - 2):
                blocks_pos[0][i] = 3
        print("new blocks pos", blocks_pos)

    rendering_point = math.ceil(pos_x)
    print("RENDERING POINT",rendering_point)
    pygame.display.flip()
    clock.tick(speed)
pygame.quit()