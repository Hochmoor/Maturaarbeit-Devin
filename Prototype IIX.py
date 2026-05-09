import random

import pygame

pygame.init()

speed = 60
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)

# Create fullscreen window at desktop resolution
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()

# Player settings
player_size = 40
pos_x = 50
pos_y = screen_height
mov_x = 0
mov_y = 0
drag = 0.985

stein_img = pygame.image.load("stein.jpg").convert_alpha()
stein_img = pygame.transform.smoothscale(stein_img, (40, 40))
gras_img = pygame.image.load("gras.jpg").convert_alpha()
gras_img = pygame.transform.smoothscale(gras_img, (40, 40))
erde_img = pygame.image.load("erde.jpg").convert_alpha()
erde_img = pygame.transform.smoothscale(erde_img, (40, 40))


# WORLD GENERATION
import random

initial_y = [10]

# Blocks pos 0 [block_y, block_x_, ]
blocks_pos = []

for i in range(64):  # already have 1 value


    if initial_y[i] < 5:
        initial_y[i] = initial_y[i] + random.randint(0, 3)
    elif 5 <= initial_y[i] <= 15:
        initial_y[i] = initial_y[i] + random.randint(-2, 2)
    else:
        initial_y[i] = initial_y[i] + random.randint(-3, 0)

    initial_y.append(initial_y[i])


print(initial_y)

blocks_pos = [[] for _ in range(64)]
for z in range(64):
    for i in range(initial_y[z]):
        blocks_pos[z].append(0)

print(blocks_pos)

# grass layer
for z in range(64):
    blocks_pos[z][initial_y[z]-1] = 1

print(blocks_pos)

# dirt layer
for z in range(64):
    if initial_y[z] < 5:
        dirt_layer = random.randint(1, 2)
        for y in range (dirt_layer):
            blocks_pos[z][initial_y[z]-2-y] = 2
    elif initial_y[z] >= 5:
        dirt_layer = random.randint(2, 4)
        for y in range (dirt_layer):
            blocks_pos[z][initial_y[z]-2-y] = 2

print(blocks_pos)


done = False
while not done:
    screen.fill(white)

    pos_x += mov_x
    pos_y += mov_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True  # ESC to quit fullscreen

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        mov_x += 0.2
    if keys[pygame.K_a]:
        mov_x -= 0.2
    if keys[pygame.K_s]:
        mov_y += 0.2
    if keys[pygame.K_w]:
        mov_y -= 0.2

    mov_x *= drag
    mov_y *= drag

    # DRAWING THE BLOCKS
    for z in range(64):
        for y in range(initial_y[z]):
            if blocks_pos[z][y] == 0:
                screen.blit(stein_img, (z*40, 1400 - y*40))

    for z in range(64):
        for y in range(initial_y[z]):
            if blocks_pos[z][y] == 1:
                screen.blit(gras_img, (z*40, 1400 - y*40))

    for z in range(64):
        for y in range(initial_y[z]):
            if blocks_pos[z][y] == 2:
                screen.blit(erde_img, (z*40, 1400 - y*40))

    # Screen bounds (dynamic!)
    if pos_x < 0:
        pos_x = 0
        mov_x = 0
    if pos_y < 0:
        pos_y = 0
        mov_y = 0
    if pos_x > screen_width - player_size:
        pos_x = screen_width - player_size
        mov_x = 0
    if pos_y > screen_height - player_size:
        pos_y = screen_height - player_size
        mov_y = 0

    pygame.draw.rect(screen, black, (pos_x, pos_y, player_size, player_size))
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
