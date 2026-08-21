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
player_size = block_size
player_rect = pygame.Rect(screen_width//2 - 0.5 * player_size, screen_height//2 - 0.5 * player_size, player_size, player_size)
player_rect_right_original = player_rect.right
player_rect_top_original = player_rect.top
print("player_rect_right_original",player_rect_right_original)
print("player_rect_top_original",player_rect_top_original)
pos_x = 0
pos_y = -40
last_frame_pos_x = pos_x
last_frame_pos_y = pos_y
mov_x = 0
mov_y = 0

# Physics
gravity = 0.025
jump_speed = 0.5
move_acceleration = 0.7
max_run_speed = 6.0
max_fall_speed = 16.0
air_drag = 0.92
ground_friction = 0.80

blocks_pos_blocks_in_range = []

stein_img = pygame.image.load("stein.jpg").convert_alpha()
stein_img = pygame.transform.smoothscale(stein_img, (block_size, block_size))
gras_img = pygame.image.load("gras.jpg").convert_alpha()
gras_img = pygame.transform.smoothscale(gras_img, (block_size, block_size))
erde_img = pygame.image.load("erde.jpg").convert_alpha()
erde_img = pygame.transform.smoothscale(erde_img, (block_size, block_size))

white = (255, 255, 255)
black = (0, 0, 0)

speed = 60

new_render_positive = 0 # This point keeps track of where the Player has been and if there needs to be a new render when player goes into unrendered territory.
new_render_negative = 0 # This point keeps track of where the Player has been and if there needs to be a new render when player goes into unrendered territory.
rendering_point = 0 # This is a rounded Version of the X coordinate to decide together with renderin_offset which part of the blocks_pos list to use.
rendering_offset = 0 # This variable keeps track of the offset which builds up as the player explores into negative pos_x territory and new renders are added in the beginning of the list.

#Cave Generation
max_diggers = 3
min_diggers = 1
starting_diggers = random.randint(min_diggers, max_diggers) # For the biases we don't want the same => Separate
diggers_positive_pos =  [[1000,0,random.randint(5,59)],[1000,0,random.randint(5,59)],[1000,0,random.randint(5,59)]]
diggers_negative_pos =  [[1000,0,random.randint(5,59)],[1000,0,random.randint(5,59)],[1000,0,random.randint(5,59)]]

for i in range(starting_diggers): # For the starting pos we want to have the same => Together
    diggers_positive_pos[i][0] = diggers_negative_pos[i][0] = random.randint(4,60)



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
    noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(get_noise_octave2(x_octave2) * amplitude_octave2)
    if noise_value > 10:
        noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
    elif noise_value > 5:
        noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)

    print("noise value",noise_value)
    blocks_pos[z][40 + noise_value] = 1
    blocks_pos[z][40 + noise_value - 1 ] = 2
    blocks_pos[z][40 + noise_value - 2 ] = 2
    for i in range(40 + noise_value - 2):
        blocks_pos[z][i] = 3

for z in range(84):
    for y in range (len(diggers_positive_pos)):
        if diggers_positive_pos[y][0] <= 64:
            blocks_pos[z][diggers_positive_pos[y][0]]= 0
            blocks_pos[z][diggers_positive_pos[y][0] - 1] = 0
            blocks_pos[z][diggers_positive_pos[y][0] + 1] = 0

            #Check if target was met
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


print("blocks_pos",blocks_pos)

def build_blocks_in_range(cur_pos_x, cur_pos_y): #cur is for current because pos_y is not updated yet when the function runs for the first time.
# This function allows the pos_x and pos_y to be updated individually to make collision checking work.
    blocks_in_range = []
    for a in range(3):  # This creates a 3x3 box around the player where collision will be checked
        for b in range(3):
            if blocks_pos[40 + rendering_offset + rendering_point + a][-math.ceil(cur_pos_y - 17) + b] != 0:
                blocks_pos[40 + rendering_offset + rendering_point + a][-math.ceil(cur_pos_y - 17) + b] *= -1  # Make the number negative to be detected when drawing blocks_pos

    for z in range(84):
        for y in range(64):
            if blocks_pos[z + rendering_point + rendering_offset][y] < 0:
                # 1. Create the Rect object: (x, y, width, height)
                rect_1 = pygame.Rect((z - cur_pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (cur_pos_y * block_size), block_size, block_size)
                blocks_in_range.append(rect_1)
                blocks_pos[z + rendering_point + rendering_offset][y] *= -1  # putting it back to the original state so the Block gets displayed with the right texture once the player moves away from it
    return blocks_in_range

on_ground = False
done = False
while not done:
    screen.fill(white)

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
    if keys[pygame.K_w]:
        if on_ground:
            mov_y = mov_y - jump_speed
    print(pos_x, pos_y)
    # Gravity
    mov_y += gravity
    if mov_y > max_fall_speed:
        mov_y = max_fall_speed

    # Clamp horizontal speed
    if mov_x > max_run_speed:
        mov_x = max_run_speed
    elif mov_x < -max_run_speed:
        mov_x = -max_run_speed

    # Friction / air drag
    mov_x = mov_x * ground_friction

    # Horizontal step: move only X, then check for collisions
    # pos_y is NOT touched yet, so the vertical gap to the ground from last
    # frame is still intact and this pass can't be fooled by falling motion.
    pos_x += mov_x
    blocks_pos_blocks_in_range = build_blocks_in_range(pos_x, pos_y)

    for block in blocks_pos_blocks_in_range:
        if player_rect.colliderect(block):
            if mov_x > 0:
                player_rect.right = block.left
            elif mov_x < 0:
                player_rect.left = block.right
            mov_x = 0

    player_rect_right_difference = player_rect.right - player_rect_right_original
    pos_x = pos_x + player_rect_right_difference / block_size
    player_rect = pygame.Rect(screen_width // 2 - 0.5 * player_size, screen_height // 2 - 0.5 * player_size, player_size, player_size)

    # Vertical step: move only Y (using the already corrected pos_x), then check for collisions
    pos_y += mov_y
    blocks_pos_blocks_in_range = build_blocks_in_range(pos_x, pos_y)

    on_ground = False
    for block in blocks_pos_blocks_in_range:
        if player_rect.colliderect(block):
            if mov_y > 0:
                player_rect.bottom = block.top
                on_ground = True
            elif mov_y < 0:
                player_rect.top = block.bottom
            mov_y = 0

    player_rect_top_difference = player_rect.top - player_rect_top_original
    pos_y = pos_y + player_rect_top_difference / block_size
    player_rect = pygame.Rect(screen_width // 2 - 0.5 * player_size, screen_height // 2 - 0.5 * player_size, player_size, player_size)

    # Mining Blocks

    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check if the left mouse button is currently pressed
    left_mouse_pressed = pygame.mouse.get_pressed()[0]

    #Creating Rect
    mouse_following_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)
    if left_mouse_pressed:
        for a in range(7):  # This creates a 3x3 box around the player where collision will be checked
            for b in range(7):
                if blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] != 0:
                    blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] *= -1

    blocks_in_range_mouse = []
    for z in range(84):
        for y in range(64):
            if blocks_pos[z + rendering_point + rendering_offset][y] < 0:
                # 1. Create the Rect object: (x, y, width, height)
                rect_1 = pygame.Rect((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (pos_y * block_size), block_size, block_size)
                blocks_in_range_mouse.append(rect_1)
                blocks_pos[z + rendering_point + rendering_offset][y] *= -1  # putting it back to the original state so the Block gets displayed with the right texture once the player moves away from it
                if rect_1.colliderect(mouse_following_rect):
                    blocks_pos[z + rendering_point + rendering_offset][y] = 0





    # DRAWING THE BLOCKS
    for z in range(84):
        for y in range(64):
            if blocks_pos[z + rendering_point + rendering_offset][y] == 0:
                continue
            if blocks_pos[z + rendering_point + rendering_offset][y] == 1:
                screen.blit(gras_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 2:
                screen.blit(erde_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 3:
                screen.blit(stein_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y*block_size - (pos_y * block_size)))



    # DRAWING THE PLAYER
    pygame.draw.rect(screen, black, player_rect)

    if pos_x > new_render_positive:
        new_render_positive += 1
        print("NRP and pos_x", new_render_positive, pos_x)
        x_octave1 = (42 + new_render_positive) / scale_octave1
        x_octave2 = (42 + new_render_positive) / scale_octave2
        x_octave3 = (42 + new_render_positive) / scale_octave3
        noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(get_noise_octave2(x_octave2) * amplitude_octave2)
        if noise_value > 10:
            noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
        elif noise_value > 5:
            noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)
        print("noise value",noise_value)
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
        print("NRN and pos_x",new_render_negative,pos_x)
        x_octave1 = (-42 + new_render_negative) / scale_octave1
        x_octave2 = (-42 + new_render_negative) / scale_octave2
        x_octave3 = (-42 + new_render_negative) / scale_octave3
        noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(get_noise_octave2(x_octave2) * amplitude_octave2)
        if noise_value > 10:
            noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
        elif noise_value > 5:
            noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)
        print("noise value", noise_value)
        blocks_pos.insert(0,[0 for _ in range(64)])

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
    last_frame_pos_x = pos_x
    last_frame_pos_y = pos_y
    pygame.display.flip()
    clock.tick(speed)
pygame.quit()