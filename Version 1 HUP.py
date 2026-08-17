import pygame
import random
import math

# Create fullscreen window at desktop resolution

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1280, 720))

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
player_size = block_size
player_rect = pygame.Rect(screen_width // 2 - 0.5 * player_size, screen_height // 2 - 0.5 * player_size, player_size,
                          player_size)
pos_x = 0
pos_y = -20
mov_x = 0
mov_y = 0
drag = 0.80

# Physics


blocks_pos_blocks_in_range = []
stein_img = pygame.image.load("stein.jpg").convert_alpha()
stein_img = pygame.transform.smoothscale(stein_img, (block_size, block_size))
gras_img = pygame.image.load("gras.jpg").convert_alpha()
gras_img = pygame.transform.smoothscale(gras_img, (block_size, block_size))
erde_img = pygame.image.load("erde.jpg").convert_alpha()
erde_img = pygame.transform.smoothscale(erde_img, (block_size, block_size))

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
speed = 60

new_render_positive = 0  # This point keeps track of where the Player has been and if there needs to be a new render when player goes into unrendered territory.
new_render_negative = 0  # This point keeps track of where the Player has been and if there needs to be a new render when player goes into unrendered territory.
rendering_point = 0  # This is a rounded Version of the X coordinate to decide together with renderin_offset which part of the blocks_pos list to use.
rendering_offset = 0  # This variable keeps track of the offset which builds up as the player explores into negative pos_x territory and new renders are added in the beginning of the list.

# Cave Generation
max_diggers = 3
min_diggers = 1
starting_diggers = random.randint(min_diggers, max_diggers)  # For the biases we don't want the same => Separate
diggers_positive_pos = [[1000, 0, random.randint(5, 59)], [1000, 0, random.randint(5, 59)],
                        [1000, 0, random.randint(5, 59)]]
diggers_negative_pos = [[1000, 0, random.randint(5, 59)], [1000, 0, random.randint(5, 59)],
                        [1000, 0, random.randint(5, 59)]]

for i in range(starting_diggers):  # For the starting pos we want to have the same => Together
    diggers_positive_pos[i][0] = diggers_negative_pos[i][0] = random.randint(4, 60)


def get_noise_octave1(pos_for_noise):
    # Determine the two points on our "ruler"
    p1 = math.floor(pos_for_noise) % len(seed_values_octave_1)
    p2 = (p1 + 1) % len(seed_values_octave_1)

    # How far are we between those points (0.0 to 1.0)
    frac = pos_for_noise - math.floor(pos_for_noise)

    # Smoothstep interpolation (the "Fade" function)
    t = frac * frac * (3 - 2 * frac)

    # Blend the two random values
    return seed_values_octave_1[p1] * (1 - t) + seed_values_octave_1[p2] * t


def get_noise_octave2(pos_for_noise):
    # Determine the two points on our "ruler"
    p1 = math.floor(pos_for_noise) % len(seed_values_octave_2)
    p2 = (p1 + 1) % len(seed_values_octave_2)

    # How far are we between those points (0.0 to 1.0)
    frac = pos_for_noise - math.floor(pos_for_noise)

    # Smoothstep interpolation (the "Fade" function)
    t = frac * frac * (3 - 2 * frac)

    # Blend the two random values
    return seed_values_octave_2[p1] * (1 - t) + seed_values_octave_2[p2] * t


def get_noise_octave3(pos_for_noise):
    # Determine the two points on our "ruler"
    p1 = math.floor(pos_for_noise) % len(seed_values_octave_3)
    p2 = (p1 + 1) % len(seed_values_octave_3)

    # How far are we between those points (0.0 to 1.0)
    frac = pos_for_noise - math.floor(pos_for_noise)

    # Smoothstep interpolation (the "Fade" function)
    t = frac * frac * (3 - 2 * frac)

    # Blend the two random values
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

    print("noise value", noise_value)
    blocks_pos[z][40 + noise_value] = 1
    blocks_pos[z][40 + noise_value - 1] = 2
    blocks_pos[z][40 + noise_value - 2] = 2
    for i in range(40 + noise_value - 2):
        blocks_pos[z][i] = 3

for z in range(84):
    for y in range(len(diggers_positive_pos)):
        if diggers_positive_pos[y][0] <= 64:
            blocks_pos[z][diggers_positive_pos[y][0]] = 0
            blocks_pos[z][diggers_positive_pos[y][0] - 1] = 0
            blocks_pos[z][diggers_positive_pos[y][0] + 1] = 0

            # Check if target was met
            if diggers_positive_pos[y][0] == diggers_positive_pos[y][2]:
                diggers_positive_pos[y][2] = random.randint(5, 49)

            if diggers_positive_pos[y][0] <= 5:
                diggers_positive_pos[y][0] += random.randint(0, 2)

            elif 5 < diggers_positive_pos[y][0] < 59:
                if diggers_positive_pos[y][0] <= diggers_positive_pos[y][2]:
                    diggers_positive_pos[y][0] += random.randint(-1, 2)
                elif diggers_positive_pos[y][0] >= diggers_positive_pos[y][2]:
                    diggers_positive_pos[y][0] += random.randint(-2, 1)

            elif diggers_positive_pos[y][0] >= 59:
                diggers_positive_pos[y][0] += random.randint(-2, 0)

print("blocks_pos", blocks_pos)

done = False
while not done:
    screen.fill(white)
    blocks_pos_blocks_in_range = []

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

    # print(pos_x, pos_y)

    for a in range(
            3):  # This creates a 3x3 box around the player where collision will be checked in the future at the moment it just makes everything air.
        for b in range(3):
            if blocks_pos[40 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 17) + b] != 0:
                blocks_pos[40 + rendering_offset + rendering_point + a][
                    -math.ceil(pos_y - 17) + b] *= -1  # Make the number negative to be detected when drawing blocks_pos

    # set back the blocks in range thing
    blocks_pos_blocks_in_range = []

    # iterate over all blocks
    for z in range(84):
        for y in range(64):

            # for better readibility: use variable block_type - this one
            block_type = abs(blocks_pos[z + rendering_point + rendering_offset][y])
            if block_type == 0:
                continue

            # Convert world coordinates (z, y) to screen pixel coordinates (screen_x, screen_y)
            screen_x = (z - pos_x + rendering_point) * block_size - block_size * 10
            screen_y = screen_height - block_size - y * block_size - (pos_y * block_size)

            # Render the corresponding texture onto the screen based on block type
            if block_type == 1:
                screen.blit(gras_img, (screen_x, screen_y))
            elif block_type == 2:
                screen.blit(erde_img, (screen_x, screen_y))
            elif block_type == 3:
                screen.blit(stein_img, (screen_x, screen_y))

            # Construct a bounding rectangle for the block at its rendered screen position
            block_rect = pygame.Rect(screen_x, screen_y, block_size, block_size)

            # If the block overlaps with the player's bounding box, collect it for collision handling/debugging
            if player_rect.colliderect(block_rect):
                blocks_pos_blocks_in_range.append(block_rect)

    # Draw all these blocks now
    for block_rect in blocks_pos_blocks_in_range:
        pygame.draw.rect(screen, red, block_rect)

    # resetting player_rect
    player_rect_temporary = player_rect
    player_rect = pygame.Rect(screen_width // 2 - 0.5 * player_size, screen_height // 2 - 0.5 * player_size,
                              player_size, player_size)
    difference_x = player_rect_temporary[0] - player_rect[0]
    difference_y = player_rect_temporary[1] - player_rect[1]
    # print("difference_x", difference_x)
    pos_x += difference_x / block_size
    pos_y += difference_y / block_size

    # DRAWING THE PLAYER
    pygame.draw.rect(screen, black, player_rect)

    if pos_x > new_render_positive:
        new_render_positive += 1
        print("NRP and pos_x", new_render_positive, pos_x)
        x_octave1 = (42 + new_render_positive) / scale_octave1
        x_octave2 = (42 + new_render_positive) / scale_octave2
        x_octave3 = (42 + new_render_positive) / scale_octave3
        noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(
            get_noise_octave2(x_octave2) * amplitude_octave2)
        if noise_value > 10:
            noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
        elif noise_value > 5:
            noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)
        print("noise value", noise_value)
        blocks_pos.append([0 for _ in range(64)])
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value] = 1
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value - 1] = 2
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value - 2] = 2
        for i in range(40 + noise_value - 2):
            blocks_pos[83 + new_render_positive - new_render_negative][i] = 3

        for y in range(len(diggers_positive_pos)):
            if diggers_positive_pos[y][0] <= 64:
                blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0]] = 0
                blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0] - 1] = 0
                blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0] + 1] = 0

                # Check if target was met
                if diggers_positive_pos[y][0] == diggers_positive_pos[y][2]:
                    diggers_positive_pos[y][2] = random.randint(5, 49)

                if diggers_positive_pos[y][0] <= 5:
                    diggers_positive_pos[y][0] += random.randint(0, 2)

                elif 5 < diggers_positive_pos[y][0] < 59:
                    if diggers_positive_pos[y][0] <= diggers_positive_pos[y][2]:
                        diggers_positive_pos[y][0] += random.randint(-1, 2)
                    elif diggers_positive_pos[y][0] >= diggers_positive_pos[y][2]:
                        diggers_positive_pos[y][0] += random.randint(-2, 1)

                elif diggers_positive_pos[y][0] >= 59:
                    diggers_positive_pos[y][0] += random.randint(-2, 0)

    if pos_x <= new_render_negative:
        rendering_offset += 1
        new_render_negative -= 1
        print("NRN and pos_x", new_render_negative, pos_x)
        x_octave1 = (-42 + new_render_negative) / scale_octave1
        x_octave2 = (-42 + new_render_negative) / scale_octave2
        x_octave3 = (-42 + new_render_negative) / scale_octave3
        noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(
            get_noise_octave2(x_octave2) * amplitude_octave2)
        if noise_value > 10:
            noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
        elif noise_value > 5:
            noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)
        print("noise value", noise_value)
        blocks_pos.insert(0, [0 for _ in range(64)])

        blocks_pos[0][40 + noise_value] = 1
        blocks_pos[0][40 + noise_value - 1] = 2
        blocks_pos[0][40 + noise_value - 2] = 2
        for i in range(40 + noise_value - 2):
            blocks_pos[0][i] = 3

        for y in range(len(diggers_negative_pos)):
            if diggers_negative_pos[y][0] <= 64:
                blocks_pos[0][diggers_negative_pos[y][0]] = 0
                blocks_pos[0][diggers_negative_pos[y][0] - 1] = 0
                blocks_pos[0][diggers_negative_pos[y][0] + 1] = 0

                # Check if target was met
                if diggers_negative_pos[y][0] == diggers_negative_pos[y][2]:
                    diggers_negative_pos[y][2] = random.randint(5, 49)

                if diggers_negative_pos[y][0] <= 5:
                    diggers_negative_pos[y][0] += random.randint(0, 2)

                elif 5 < diggers_negative_pos[y][0] < 59:
                    if diggers_negative_pos[y][0] <= diggers_negative_pos[y][2]:
                        diggers_negative_pos[y][0] += random.randint(-1, 2)
                    elif diggers_negative_pos[y][0] >= diggers_negative_pos[y][2]:
                        diggers_negative_pos[y][0] += random.randint(-2, 1)

                elif diggers_negative_pos[y][0] >= 59:
                    diggers_negative_pos[y][0] += random.randint(-2, 0)

    rendering_point = math.ceil(pos_x)
    pygame.display.flip()
    clock.tick(speed)
pygame.quit()