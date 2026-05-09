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
player_size = 30
pos_x = 50
pos_y = screen_height - 100
mov_x = 0
mov_y = 0
drag = 0.985


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
    blocks_pos[z][0] = 1

print(blocks_pos)

# dirt layer
for z in range(64):
    dirt_layer = random.randint(2, 4)
    for y in range (dirt_layer):
        blocks_pos[z][y+1] = 2

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
