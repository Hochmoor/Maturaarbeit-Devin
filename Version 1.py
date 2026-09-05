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

world_height = 104

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

#Background Texture
background_img = pygame.image.load("background.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_width,screen_height))
background_x = pos_x

#Block Textures
stein_img = pygame.image.load("stone.png").convert_alpha()
stein_img = pygame.transform.scale(stein_img, (block_size, block_size))
gras_img = pygame.image.load("grass.png").convert_alpha()
gras_img = pygame.transform.scale(gras_img, (block_size, block_size))
erde_img = pygame.image.load("dirt.png").convert_alpha()
erde_img = pygame.transform.scale(erde_img, (block_size, block_size))
deep_rock_img = pygame.image.load("deep rock.png").convert_alpha()
deep_rock_img = pygame.transform.scale(deep_rock_img, (block_size, block_size))
magma_img = pygame.image.load("magma3.png").convert_alpha()
magma_img = pygame.transform.scale(magma_img, (block_size, block_size))
leaf_light_img = pygame.image.load("leafe_light.png").convert_alpha()
leaf_light_img = pygame.transform.scale(leaf_light_img, (block_size, block_size))
leaf_dark_img = pygame.image.load("leafe_dark.png").convert_alpha()
leaf_dark_img = pygame.transform.scale(leaf_dark_img, (block_size, block_size))
wood_img = pygame.image.load("wood.png").convert_alpha()
wood_img = pygame.transform.scale(wood_img, (block_size, block_size))

#Structures
tree = [[0,0,6,6,7,0],
        [0,0,7,7,6,6],
        [8,8,7,6,6,7],
        [0,0,6,7,7,6],
        [0,0,7,6,7,0]]

tree = [[0,0,7,0,0,0,0,0],
        [0,0,7,7,0,7,0,0],
        [8,8,8,8,8,7,7,7],
        [0,0,7,7,0,7,0,0],
        [0,0,7,0,0,0,0,0]]

tree_density_mode = random.randint(1,3)
tree_density_mode_negative = random.randint(1,3)

next_tree = random.randint(2,5)
next_tree_negative = random.randint(2,5)
print("next_tree",next_tree)

print("len(tree)",len(tree))
print("len(tree[0])",len(tree[0]))

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

# INVENTORY
# The inventory keeps track of how many and what kind of blocks the player is carrying.
# The dictionary keys match the numbers used in blocks_pos.
inventory = {1: 0, 2: 0, 3: 0} # Inventory can be expanded easily
block_names = {1: "Grass", 2: "Dirt", 3: "Stone"}
block_images = {1: gras_img, 2: erde_img, 3: stein_img}
selected_block = 3      # Block currently selected to place
inventory_open = False  # Toggled by pressing "E"

inventory_font = pygame.font.SysFont(None, max(18, block_size))

blocks_pos = [[0 for _ in range(world_height)] for _ in range(84)]


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
    for i in range(22 + noise_value - 2):
        blocks_pos[z][i + 18] = 3

    blocks_pos[z][12] = random.choices([3, 4], [5, 95])[0]
    blocks_pos[z][13] = random.choices([3, 4], [20, 80])[0]
    blocks_pos[z][14] = random.choices([3, 4], [40, 60])[0]
    blocks_pos[z][15] = random.choices([3, 4], [60, 40])[0]
    blocks_pos[z][16] = random.choices([3, 4], [80, 20])[0]
    blocks_pos[z][17] = random.choices([3, 4], [95, 5])[0]

    for i in range(12):
        blocks_pos[z][i] = 4



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

# Drawing Trees
for z in range(74): # 74 because blocks pos is 84 rows long and I want 5 blocks of clearance on each side
    z += 5
    next_tree -= 1
    if next_tree == 0:
        x_octave1 = (z - 42 + 2) / scale_octave1
        x_octave2 = (z - 42 + 2) / scale_octave2
        x_octave3 = (z - 42 + 2) / scale_octave3
        noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(get_noise_octave2(x_octave2) * amplitude_octave2)
        if noise_value > 10:
            noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
        elif noise_value > 5:
            noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)
        ground_height = noise_value
        print("noise value",noise_value)
        for a in range(len(tree)):
            for b in range(len(tree[a])):
                if blocks_pos[a + z][b + ground_height + 40] == 0 or blocks_pos[a + z][b + ground_height + 40] == 1:
                    blocks_pos[a + z][b + ground_height + 40] = tree[a][b]

        if tree_density_mode == 1:
            next_tree = random.randint(16, 40)
        if tree_density_mode == 2:
            next_tree = random.randint(8, 20)
        if tree_density_mode == 3:
            next_tree = random.randint(4, 8)

def build_blocks_in_range(cur_pos_x, cur_pos_y): #cur is for current because pos_y is not updated yet when the function runs for the first time.
# This function allows the pos_x and pos_y to be updated individually to make collision checking work.
    blocks_in_range = []
    for a in range(3):  # This creates a 3x3 box around the player where collision will be checked
        for b in range(3):
            if blocks_pos[40 + rendering_offset + rendering_point + a][-math.ceil(cur_pos_y - 17) + b] != 0 and blocks_pos[40 + rendering_offset + rendering_point + a][-math.ceil(cur_pos_y - 17) + b] != 1:
                blocks_pos[40 + rendering_offset + rendering_point + a][-math.ceil(cur_pos_y - 17) + b] *= -1  # Make the number negative to be detected when drawing blocks_pos

    for z in range(84):
        for y in range(world_height):
            if blocks_pos[z + rendering_point + rendering_offset][y] < 0:
                # 1. Create the Rect object: (x, y, width, height)
                rect_1 = pygame.Rect((z - cur_pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (cur_pos_y * block_size), block_size, block_size)
                blocks_in_range.append(rect_1)
                blocks_pos[z + rendering_point + rendering_offset][y] *= -1  # putting it back to the original state so the Block gets displayed with the right texture once the player moves away from it
    return blocks_in_range


def draw_inventory():
    # A small hotbar in the top-left, always visible, showing what will be placed and how much of it we have.
    hotbar_x = 20
    hotbar_y = 20
    for i, block_type in enumerate([1, 2, 3]):
        slot_rect = pygame.Rect(hotbar_x + i * (block_size + 10), hotbar_y, block_size, block_size)
        pygame.draw.rect(screen, white, slot_rect)
        screen.blit(block_images[block_type], slot_rect)
        border_color = (255, 0, 0) if block_type == selected_block else black
        border_width = 3 if block_type == selected_block else 1
        pygame.draw.rect(screen, border_color, slot_rect, border_width)
        count_surface = inventory_font.render(str(inventory[block_type]), True, black)
        screen.blit(count_surface, (slot_rect.x + 2, slot_rect.bottom - count_surface.get_height()))

    # The bigger panel only appears while the inventory is toggled open with "E".
    if inventory_open:
        panel_width = 260
        panel_height = 50 + len(inventory) * (block_size + 10)
        panel_rect = pygame.Rect(screen_width // 2 - panel_width // 2, screen_height // 2 - panel_height // 2, panel_width, panel_height)
        pygame.draw.rect(screen, white, panel_rect)
        pygame.draw.rect(screen, black, panel_rect, 2)

        title_surface = inventory_font.render("Inventory", True, black)
        screen.blit(title_surface, (panel_rect.x + 10, panel_rect.y + 10))

        for i, block_type in enumerate([1, 2, 3]):
            row_y = panel_rect.y + 50 + i * (block_size + 10)
            icon_rect = pygame.Rect(panel_rect.x + 10, row_y, block_size, block_size)
            screen.blit(block_images[block_type], icon_rect)
            label_surface = inventory_font.render(f"{block_names[block_type]}: {inventory[block_type]}", True, black)
            screen.blit(label_surface, (icon_rect.right + 10, row_y + block_size // 2 - label_surface.get_height() // 2))


on_ground = False
done = False
while not done:
    screen.fill(white)

    #Makes the Background loop
    if background_x >= 0.5 * screen_width:
        background_x = background_x - screen_width

    if background_x <= - 0.5 * screen_width:
        background_x = background_x + screen_width

    # Displaying the Background
    screen.blit(background_img, (- background_x - 0.5 * screen_width,0))
    screen.blit(background_img, (- background_x + 0.5 * screen_width,0))

    # DRAWING THE PLAYER
    pygame.draw.rect(screen, black, player_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True  # ESC to quit fullscreen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            inventory_open = not inventory_open  # Toggle the inventory panel open/closed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            selected_block = 1  # Select Grass for placing
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            selected_block = 2  # Select Dirt for placing
        if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            selected_block = 3  # Select Stone for placing

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

    # MINING & PLACING
    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check if the left mouse button is currently pressed
    left_mouse_pressed = pygame.mouse.get_pressed()[0]
    right_mouse_pressed = pygame.mouse.get_pressed()[2]

    mouse_following_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)

    #Checking 7x7 blocks around player
    if left_mouse_pressed:
        for a in range(7):
            for b in range(7):
                if blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] != 0:
                    blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] *= -1

    blocks_in_range_mouse = [] # Emptying the list
    for z in range(84):
        for y in range(world_height):
            if blocks_pos[z + rendering_point + rendering_offset][y] < 0: # Finding the blocks made negative by the 7x7 Box
                # Create the Rect object: (x, y, width, height)
                rect_1 = pygame.Rect((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (pos_y * block_size), block_size, block_size)
                blocks_in_range_mouse.append(rect_1)
                blocks_pos[z + rendering_point + rendering_offset][y] *= -1  # putting it back to the original state so the Block gets displayed with the right texture once the player moves away from it
                if rect_1.colliderect(mouse_following_rect):
                    mined_block_type = blocks_pos[z + rendering_point + rendering_offset][y]  # Remember which block we're about to remove
                    inventory[mined_block_type] = inventory.get(mined_block_type, 0) + 1       # Add one of that block to the inventory
                    blocks_pos[z + rendering_point + rendering_offset][y] = 0 # Removing the block by setting it to zero

    #Checking 7x7 blocks around player
    if right_mouse_pressed:
        print("right_mouse_pressed")
        for a in range(7):
            for b in range(7):
                if blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] == 0:
                    blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] = -1

    blocks_in_range_mouse = [] # Emptying the list
    for z in range(84):
        for y in range(world_height):
            if blocks_pos[z + rendering_point + rendering_offset][y] < 0: # Finding the blocks made negative by the 7x7 Box
                # Create the Rect object: (x, y, width, height)
                rect_1 = pygame.Rect((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (pos_y * block_size), block_size, block_size)
                blocks_in_range_mouse.append(rect_1)
                blocks_pos[z + rendering_point + rendering_offset][y] = 0  # putting it back to the original state 0 = Air
                if rect_1.colliderect(mouse_following_rect) and not rect_1.colliderect(player_rect):
                    if inventory.get(selected_block, 0) > 0:                  # Only place if we actually have one in the inventory
                        blocks_pos[z + rendering_point + rendering_offset][y] = selected_block
                        inventory[selected_block] -= 1                        # Placing costs one block from the inventory


    # DRAWING THE BLOCKS
    for z in range(84):
        for y in range(world_height):
            if blocks_pos[z + rendering_point + rendering_offset][y] == 0:
                continue
            if blocks_pos[z + rendering_point + rendering_offset][y] == 1:
                screen.blit(gras_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 2:
                screen.blit(erde_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 3:
                screen.blit(stein_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 4:
                screen.blit(deep_rock_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 5:
                screen.blit(magma_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 6:
                screen.blit(leaf_light_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 7:
                screen.blit(leaf_dark_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 8:
                screen.blit(wood_img, ((z - pos_x + rendering_point) * block_size - block_size * 10,screen_height - block_size - y * block_size - (pos_y * block_size)))

    # DRAWING THE INVENTORY (hotbar + optional panel)
    draw_inventory()

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
        blocks_pos.append([0 for _ in range(world_height)])
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value] = 1
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value - 1] = 2
        blocks_pos[83 + new_render_positive - new_render_negative][40 + noise_value - 2] = 2
        for i in range(22 + noise_value - 2):
            blocks_pos[83 + new_render_positive - new_render_negative][i + 18] = 3

        blocks_pos[83 + new_render_positive - new_render_negative][12] = random.choices([3, 4], [5, 95])[0]
        blocks_pos[83 + new_render_positive - new_render_negative][13] = random.choices([3, 4], [20, 80])[0]
        blocks_pos[83 + new_render_positive - new_render_negative][14] = random.choices([3, 4], [40, 60])[0]
        blocks_pos[83 + new_render_positive - new_render_negative][15] = random.choices([3, 4], [60, 40])[0]
        blocks_pos[83 + new_render_positive - new_render_negative][16] = random.choices([3, 4], [80, 20])[0]
        blocks_pos[83 + new_render_positive - new_render_negative][17] = random.choices([3, 4], [95, 5])[0]

        for i in range(12):
            blocks_pos[83 + new_render_positive - new_render_negative][i] = 4


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

        next_tree -= 1
        one_percent = random.randint(1, 100)
        if one_percent == 100:
            tree_density_mode = random.randint(1, 3)
        if next_tree == 0:
            x_octave1 = (42 - 3 + new_render_positive) / scale_octave1
            x_octave2 = (42 - 3 + new_render_positive) / scale_octave2
            x_octave3 = (42 - 3 + new_render_positive) / scale_octave3
            noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(
                get_noise_octave2(x_octave2) * amplitude_octave2)
            if noise_value > 10:
                noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
            elif noise_value > 5:
                noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)
            ground_height = noise_value
            print("noise value", noise_value)
            for a in range(len(tree)):
                for b in range(len(tree[a])):
                    if blocks_pos[a + 83 - 5 + new_render_positive - new_render_negative][b + ground_height + 40] == 0 or blocks_pos[a + 83 - 5 + new_render_positive - new_render_negative][b + ground_height + 40] == 1:
                        blocks_pos[a + 83 - 5 + new_render_positive - new_render_negative][b + ground_height + 40] = tree[a][b]

            if tree_density_mode == 1:
                next_tree = random.randint(16, 40)
            if tree_density_mode == 2:
                next_tree = random.randint(8, 20)
            if tree_density_mode == 3:
                next_tree = random.randint(4, 8)


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
        blocks_pos.insert(0,[0 for _ in range(world_height)])

        blocks_pos[0][40 + noise_value] = 1
        blocks_pos[0][40 + noise_value - 1] = 2
        blocks_pos[0][40 + noise_value - 2] = 2
        for i in range(22 + noise_value - 2):
            blocks_pos[0][i + 18] = 3

        blocks_pos[0][12] = random.choices([3, 4], [5, 95])[0]
        blocks_pos[0][13] = random.choices([3, 4], [20, 80])[0]
        blocks_pos[0][14] = random.choices([3, 4], [40, 60])[0]
        blocks_pos[0][15] = random.choices([3, 4], [60, 40])[0]
        blocks_pos[0][16] = random.choices([3, 4], [80, 20])[0]
        blocks_pos[0][17] = random.choices([3, 4], [95, 5])[0]

        for i in range(12):
            blocks_pos[0][i] = 4

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

        next_tree_negative -= 1
        one_percent = random.randint(1, 100)
        if one_percent == 100:
            tree_density_mode_negative = random.randint(1, 3)
        if next_tree_negative == 0:
            x_octave1 = (-42 + 7 + new_render_negative) / scale_octave1
            x_octave2 = (-42 + 7 + new_render_negative) / scale_octave2
            x_octave3 = (-42 + 7 + new_render_negative) / scale_octave3
            noise_value = round(get_noise_octave1(x_octave1) * amplitude_octave1) + round(
                get_noise_octave2(x_octave2) * amplitude_octave2)
            if noise_value > 10:
                noise_value += round(get_noise_octave3(x_octave3) * amplitude_octave3)
            elif noise_value > 5:
                noise_value += round(get_noise_octave3(x_octave3) * 0.5 * amplitude_octave3)
            ground_height = noise_value
            print("noise value", noise_value)
            for a in range(len(tree)):
                for b in range(len(tree[a])):
                    if blocks_pos[a + 5][b + ground_height + 40] == 0 or blocks_pos[a + 5][b + ground_height + 40] == 1:
                        blocks_pos[a + 5][b + ground_height + 40] = tree[a][b]

            if tree_density_mode_negative == 1:
                next_tree_negative = random.randint(16, 40)
            if tree_density_mode_negative == 2:
                next_tree_negative = random.randint(8, 20)
            if tree_density_mode_negative == 3:
                next_tree_negative = random.randint(4, 8)

    rendering_point = math.ceil(pos_x)

    # Updating Background Position
    background_x = background_x + 2 * (pos_x - last_frame_pos_x)


    last_frame_pos_x = pos_x
    last_frame_pos_y = pos_y
    pygame.display.flip()
    print("FPS",clock.get_fps())
    clock.tick(speed)
pygame.quit()