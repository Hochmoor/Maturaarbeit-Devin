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
max_fall_speed = 10
air_drag = 0.92
ground_friction = 0.80

blocks_pos_blocks_in_range = []

#Background Texture
background_img = pygame.image.load("background_2.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_width,screen_height))
background_x = pos_x

# Slime Frames
slime_frame = 0
slime_frames = [
    pygame.transform.scale(pygame.image.load("slime 1.png").convert_alpha(), (block_size, block_size)),
    pygame.transform.scale(pygame.image.load("slime 2.png").convert_alpha(), (block_size, block_size)),
    pygame.transform.scale(pygame.image.load("slime 3.png").convert_alpha(), (block_size, block_size)),
    pygame.transform.scale(pygame.image.load("slime 4.png").convert_alpha(), (block_size, block_size)),
    pygame.transform.scale(pygame.image.load("slime 5.png").convert_alpha(), (block_size, block_size)),
]



# Block Textures
stone_img = pygame.image.load("stone 3.png").convert_alpha()
stone_dark_img = stone_img.copy()
stone_dark_img.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
stone_img = pygame.transform.scale(stone_img, (block_size, block_size))
stone_dark_img = pygame.transform.scale(stone_dark_img, (block_size, block_size))

grass_img = pygame.image.load("grass.png").convert_alpha()
grass_dark_img = grass_img.copy()
grass_img = pygame.transform.scale(grass_img, (block_size, block_size))
grass_dark_img = pygame.transform.scale(grass_dark_img, (block_size, block_size))


dirt_img = pygame.image.load("dirt.png").convert_alpha()
dirt_dark_img = dirt_img.copy()
dirt_dark_img.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT)
dirt_img = pygame.transform.scale(dirt_img, (block_size, block_size))
dirt_dark_img = pygame.transform.scale(dirt_dark_img, (block_size, block_size))

deep_rock_img = pygame.image.load("deep rock 4.png").convert_alpha()
deep_rock_dark_img = deep_rock_img.copy()
deep_rock_dark_img.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT)
deep_rock_img = pygame.transform.scale(deep_rock_img, (block_size, block_size))
deep_rock_dark_img = pygame.transform.scale(deep_rock_dark_img, (block_size, block_size))

magma_img = pygame.image.load("magma3.png").convert_alpha()
magma_dark_img = magma_img.copy()
magma_dark_img.fill((200, 200, 200), special_flags=pygame.BLEND_RGB_MULT)
magma_img = pygame.transform.scale(magma_img, (block_size, block_size))
magma_dark_img = pygame.transform.scale(magma_dark_img, (block_size, block_size))

leaf_light_img = pygame.image.load("leaf_light.png").convert_alpha()
leaf_light_dark_img = leaf_light_img.copy()
leaf_light_img = pygame.transform.scale(leaf_light_img, (block_size, block_size))
leaf_light_dark_img = pygame.transform.scale(leaf_light_dark_img, (block_size, block_size))

leaf_dark_img = pygame.image.load("leaf_dark.png").convert_alpha()
leaf_dark_dark_img = leaf_dark_img.copy()
leaf_dark_img = pygame.transform.scale(leaf_dark_img, (block_size, block_size))
leaf_dark_dark_img = pygame.transform.scale(leaf_dark_dark_img, (block_size, block_size))

wood_img = pygame.image.load("wood.png").convert_alpha()
wood_dark_img = wood_img.copy()
wood_dark_img.fill((200, 200, 200), special_flags=pygame.BLEND_RGB_MULT)
wood_img = pygame.transform.scale(wood_img, (block_size, block_size))
wood_dark_img = pygame.transform.scale(wood_dark_img, (block_size, block_size))

slime_img = pygame.image.load("slime.png").convert_alpha()
slime_img = pygame.transform.scale(slime_img, (block_size, block_size))

copper_img = pygame.image.load("copper 3.png").convert_alpha()
copper_img = pygame.transform.scale(copper_img, (block_size, block_size))

iron_img = pygame.image.load("iron.png").convert_alpha()
iron_img = pygame.transform.scale(iron_img, (block_size, block_size))

diamond_img = pygame.image.load("diamond.png").convert_alpha()
diamond_img = pygame.transform.scale(diamond_img, (block_size, block_size))

mysticite_img = pygame.image.load("mysticite.png").convert_alpha()
mysticite_img = pygame.transform.scale(mysticite_img, (block_size, block_size))

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


# ORE GENERATION
ore_block_types = (9, 10, 11, 12) #copper, iron, diamond, mysticite
ore_cluster_gap = 2 # Minimal distance between ores

# Checking distance to nearby ores
def ore_cluster_nearby(x, y):
    for check_x in range(max(0, x - ore_cluster_gap),# max is used to prevent the value from going negative
                         min(len(blocks_pos), x + ore_cluster_gap + 1)):# min is used to take the lower value and prevents checking of blocks pos positions that aren't generated yet. +1 is because ranges (3,5) don't include 5.
        for check_y in range(max(0, y - ore_cluster_gap), # max avoids checking under 0
                             min(world_height, y + ore_cluster_gap + 1)): # min avoids checking over world height
            if abs(check_x - x) + abs(check_y - y) <= ore_cluster_gap: # adding the two absolute values
                if blocks_pos[check_x][check_y] in ore_block_types: # checking blocks pos for ores
                    return True
    return False

def try_generate_ore_vein(x, ore_type, host_block, chance):
    if random.random() >= chance: #random.random gives a some number between 0 and 1, chance could be a value 0.01 => basically 1%
        return # if it returns it means that it exits the function and no ore is generated.

    possible_starts = []
    for y in range(world_height):
        if blocks_pos[x][y] == host_block and not ore_cluster_nearby(x, y): #checks if on right block (stone for iron/ deep rock for diamond) and if there are other clusters nearby.
            possible_starts.append((x, y))

    if not possible_starts: # a list gives the boolean false if empty. So if no possible starts are found the function is left.
        return

    vein_size = random.randint(2, 5) # determines the vein size
    vein_positions = [random.choice(possible_starts)] # chooses a random position from the list containing all valid start positions.

    while len(vein_positions) < vein_size:
        possible_next_blocks = []

        for vein_x, vein_y in vein_positions:
            for next_x, next_y in ((vein_x + 1, vein_y), (vein_x - 1, vein_y),
                                   (vein_x, vein_y + 1), (vein_x, vein_y - 1)): # checking the four directly attached blocks.
                if 0 <= next_x < len(blocks_pos) and 0 <= next_y < world_height: # Preventing the next ore to be placed in impossible pos_x
                    if (next_x, next_y) not in vein_positions: # prevents using a block twice
                        if blocks_pos[next_x][next_y] == host_block and not ore_cluster_nearby(next_x, next_y): #checking for the right host_block and if there are clusters nearby. # doesn't see the blocks of the vein being placed at the moment because the block values haven't switched yet.
                            possible_next_blocks.append((next_x, next_y))

        if not possible_next_blocks:
            break # break leaves the current loop but not the whole function

        vein_positions.append(random.choice(possible_next_blocks)) # add the next possible block

    # Only place complete veins that have managed to grow to at least two blocks.
    if len(vein_positions) >= 2:
        for vein_x, vein_y in vein_positions:
            blocks_pos[vein_x][vein_y] = ore_type #switches the blocks_pos value for the ore value (9 -> copper)

# Function that when executed, executes all try_generate_ore_vein function for the different ores.
# Here the odds for the different ores can be tweaked.
def generate_ores_for_column(x):
    # Copper and iron are common and replace normal stone. (the 3)
    try_generate_ore_vein(x, 9, 3, 0.18)   # Copper
    try_generate_ore_vein(x, 10, 3, 0.14)  # Iron

    # Diamond and Mysticite only replace deep rock. (the 4)
    try_generate_ore_vein(x, 11, 4, 0.02) # Diamond
    try_generate_ore_vein(x, 12, 4, 0.005) # Mysticite


# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
offset = 0

# INVENTORY
# The inventory keeps track of how many and what kind of blocks the player is carrying.
# The dictionary keys match the numbers used in blocks_pos.
inventory = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0} # Inventory can be expanded easily
block_names = {1: "Grass", 2: "Dirt", 3: "Stone", 4: "Leaf Light", 5: "Leaf Dark", 6: "Wood", 7: "Deep Rock", 8: "Coal", 9: "Copper", 10: "Iron", 11: "Diamond", 12: "Mysticite"}
block_images = {1: grass_img, 2: dirt_img, 3: stone_img, 9: copper_img, 10: iron_img, 11: diamond_img, 12: mysticite_img}
inventory_display_blocks = [1, 2, 3, 9, 10, 11, 12]
selected_block = 3      # Block currently selected to place
inventory_open = False  # Toggled by pressing "E"

inventory_font = pygame.font.SysFont(None, max(18, block_size))

# Creating blocks_pos and blocks_pos height to keep track of the terrain height.
blocks_pos = [[0 for _ in range(world_height)] for _ in range(84)]
blocks_pos_height = []


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
    blocks_pos_height.append(40 + noise_value)
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

    for i in range(9):
        blocks_pos[z][i + 3] = 4

    blocks_pos[z][2] = random.choices([4, 5], [85, 15])[0]
    blocks_pos[z][1] = random.choices([4, 5], [30, 70])[0]
    blocks_pos[z][0] = 5

print("height",blocks_pos_height)

for z in range(84):
    for y in range (len(diggers_positive_pos)):
        if diggers_positive_pos[y][0] <= 64:
            if blocks_pos[z][diggers_positive_pos[y][0]] != 0 and blocks_pos[z][diggers_positive_pos[y][0]] != 1:
                blocks_pos[z][diggers_positive_pos[y][0]] = 0.5
            if blocks_pos[z][diggers_positive_pos[y][0] - 1] != 0 and blocks_pos[z][diggers_positive_pos[y][0] - 1] != 1:
                blocks_pos[z][diggers_positive_pos[y][0] - 1] = 0.5
            if blocks_pos[z][diggers_positive_pos[y][0] + 1] != 0 and blocks_pos[z][diggers_positive_pos[y][0] + 1] != 1:
                blocks_pos[z][diggers_positive_pos[y][0] + 1] = 0.5

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

# Generate ore veins after the starting caves so ores only replace solid rock.
for z in range(84):
    generate_ores_for_column(z)

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
            if 2 <= blocks_pos[40 + rendering_offset + rendering_point + a][-math.ceil(cur_pos_y - 17) + b] <= 1000:
                blocks_pos[40 + rendering_offset + rendering_point + a][-math.ceil(cur_pos_y - 17) + b] *= -1  # Make the number negative to be detected when listing them in blocks_in_range (to later check collisions with colliderect)

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
        panel_height = 50 + len(inventory_display_blocks) * (block_size + 10)
        panel_rect = pygame.Rect(screen_width // 2 - panel_width // 2, screen_height // 2 - panel_height // 2, panel_width, panel_height)
        pygame.draw.rect(screen, white, panel_rect)
        pygame.draw.rect(screen, black, panel_rect, 2)

        title_surface = inventory_font.render("Inventory", True, black)
        screen.blit(title_surface, (panel_rect.x + 10, panel_rect.y + 10))

        for i, block_type in enumerate(inventory_display_blocks):
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
                if blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] != 0 and blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] != 0.5 and blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] != 5:
                    blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] *= -1 # making the blocks in range negative for it to be detected later.

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

                    if blocks_pos_height[z + rendering_point + rendering_offset] <= y:
                        blocks_pos[z + rendering_point + rendering_offset][
                            y] = 0  # putting it back to the original state 0 = Air

                    else:
                        blocks_pos[z + rendering_point + rendering_offset][y] = 0.5
                        print("happened")



    #Checking 7x7 blocks around player
    if right_mouse_pressed:
        print("right_mouse_pressed")
        for a in range(7):
            for b in range(7):
                if blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] == 0:
                    blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] -= 1

                if blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] == 0.5:
                    blocks_pos[38 + rendering_offset + rendering_point + a][-math.ceil(pos_y - 15) + b] *= -1

    blocks_in_range_mouse = [] # Emptying the list
    for z in range(84):
        for y in range(world_height):
            if blocks_pos[z + rendering_point + rendering_offset][y] < 0: # Finding the blocks made negative by the 7x7 Box
                # Create the Rect object: (x, y, width, height)
                rect_1 = pygame.Rect((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (pos_y * block_size), block_size, block_size)
                blocks_in_range_mouse.append(rect_1)
                if blocks_pos[z + rendering_point + rendering_offset][y] == -1:
                    blocks_pos[z + rendering_point + rendering_offset][y] = 0
                if blocks_pos[z + rendering_point + rendering_offset][y] == - 0.5:
                    blocks_pos[z + rendering_point + rendering_offset][y] *= -1  # putting it back to the original state 0 = Air
                if rect_1.colliderect(mouse_following_rect) and not rect_1.colliderect(player_rect):
                    if inventory.get(selected_block, 0) > 0:                  # Only place if we actually have one in the inventory
                        blocks_pos[z + rendering_point + rendering_offset][y] = selected_block
                        inventory[selected_block] -= 1                        # Placing costs one block from the inventory

# Drawing the black rects separately so they appear behind the player.
    for z in range(84):
        for y in range(world_height):
            if blocks_pos[z + rendering_point + rendering_offset][y] == 0.5:
                black_rect = pygame.Rect((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size), block_size, block_size)
                pygame.draw.rect(screen,black,black_rect)

    # DRAWING THE PLAYER
    slime_frame += 0.1
    if slime_frame >= 5:
        slime_frame = 0

    screen.blit(slime_frames[math.floor(slime_frame)], ((screen_width//2 - block_size // 2),(screen_height//2 - block_size // 2)))


# DRAWING THE BLOCKS
    for z in range(84):
        for y in range(world_height):
            if blocks_pos[z + rendering_point + rendering_offset][y] == 0:
                continue



            if blocks_pos[z + rendering_point + rendering_offset][y] == 1:
                screen.blit(grass_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 2:
                screen.blit(dirt_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height- block_size - y*block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 3:
                screen.blit(stone_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y*block_size - (pos_y * block_size)))

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

            if blocks_pos[z + rendering_point + rendering_offset][y] == 9:
                screen.blit(copper_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 10:
                screen.blit(iron_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 11:
                screen.blit(diamond_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (pos_y * block_size)))

            if blocks_pos[z + rendering_point + rendering_offset][y] == 12:
                screen.blit(mysticite_img, ((z - pos_x + rendering_point) * block_size - block_size * 10, screen_height - block_size - y * block_size - (pos_y * block_size)))

    black_rect = pygame.Rect(0, screen_height - (pos_y * block_size), screen_width, screen_height//2)
    pygame.draw.rect(screen, black, black_rect)

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
        blocks_pos_height.append(40 + noise_value)
        print("blocks_pos_height", blocks_pos_height)
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

        for i in range(9):
            blocks_pos[83 + new_render_positive - new_render_negative][i + 3] = 4

        blocks_pos[83 + new_render_positive - new_render_negative][2] = random.choices([4, 5], [85, 15])[0]
        blocks_pos[83 + new_render_positive - new_render_negative][1] = random.choices([4, 5], [30, 70])[0]
        blocks_pos[83 + new_render_positive - new_render_negative][0] = 5


        for y in range(len(diggers_positive_pos)):
            if diggers_positive_pos[y][0] <= 64:
                if blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0]] != 0 and blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0]] != 1:
                    blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0]] = 0.5
                if blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0] - 1] != 0 and blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0] - 1] != 1:
                    blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0] - 1] = 0.5
                if blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0] + 1] != 0 and blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0] + 1] != 1:
                    blocks_pos[83 + new_render_positive - new_render_negative][diggers_positive_pos[y][0] + 1] = 0.5



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

# Ore generation
        generate_ores_for_column(83 + new_render_positive - new_render_negative)

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
        blocks_pos_height.insert(0,40 + noise_value)
        print("blocks_pos_height",blocks_pos_height)
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

        for i in range(9):
            blocks_pos[0][i + 3] = 4

        blocks_pos[0][2] = random.choices([4, 5], [85, 15])[0]
        blocks_pos[0][1] = random.choices([4, 5], [30, 70])[0]
        blocks_pos[0][0] = 5

        for y in range(len(diggers_negative_pos)):
            if diggers_negative_pos[y][0] <= 64:
                if blocks_pos[0][diggers_negative_pos[y][0]] != 0 and blocks_pos[0][diggers_negative_pos[y][0]] != 1:
                    blocks_pos[0][diggers_negative_pos[y][0]] = 0.5
                if blocks_pos[0][diggers_negative_pos[y][0] - 1] != 0 and blocks_pos[0][diggers_negative_pos[y][0] - 1] != 1:
                    blocks_pos[0][diggers_negative_pos[y][0] - 1] = 0.5
                if blocks_pos[0][diggers_negative_pos[y][0] + 1] != 0 and blocks_pos[0][diggers_negative_pos[y][0] + 1] != 1:
                    blocks_pos[0][diggers_negative_pos[y][0] + 1] = 0.5

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

# ore generation
        generate_ores_for_column(0)

        next_tree_negative -= 1
        one_percent = random.randint(1, 100)
        if one_percent == 100:
            tree_density_mode_negative = random.randint(1, 3)
        if next_tree_negative == 0:

            ground_height = blocks_pos_height[5]

            for a in range(len(tree)):
                for b in range(len(tree[a])):
                    if blocks_pos[a + 3][b + ground_height] == 0 or blocks_pos[a + 3][b + ground_height] == 1:
                        blocks_pos[a + 3][b + ground_height] = tree[a][b]

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