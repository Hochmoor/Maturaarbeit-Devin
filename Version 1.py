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
jump_speed = 0.26       # Start with a low jump (just over one block).
move_acceleration = 0.025
max_run_speed = 0.10    # Movement improves after stages 2, 4 and 6.
max_fall_speed = 8
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

tree_2 = [[0,0,7,0,0,0,0,0],
        [0,0,7,7,0,7,0,0],
        [8,8,8,8,8,7,7,7],
        [0,0,7,7,0,7,0,0],
        [0,0,7,0,0,0,0,0]]

tree_density_mode = random.randint(1,3)
tree_density_mode_negative = random.randint(1,3)

tree_type_mode = random.randint(1,2)
tree_type_mode_negative = random.randint(1,2)

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
    try_generate_ore_vein(x, 11, 4, 0.04) # Diamond
    try_generate_ore_vein(x, 12, 4, 0.015) # Mysticite


# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
offset = 0

# HOTBAR / MINED BLOCK COUNTS
# mined_blocks keeps track of how many blocks the player has available and is also used for progression.
mined_blocks = {1: 100, 2: 100, 3: 0, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 100, 10: 100, 11: 100, 12: 100}
block_names = {1: "Grass", 2: "Dirt", 3: "Stone", 4: "Deep Rock", 5: "Magma", 6: "Leaf Light", 7: "Leaf Dark", 8: "Wood", 9: "Copper", 10: "Iron", 11: "Diamond", 12: "Mysticite"}
block_images = {1: grass_img, 2: dirt_img, 3: stone_img, 4: deep_rock_img, 5: magma_img, 6: leaf_light_img, 7: leaf_dark_img, 8: wood_img, 9: copper_img, 10: iron_img, 11: diamond_img, 12: mysticite_img}
placeable_blocks = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]  # Every block except unmineable magma
selected_block = 3

ui_font = pygame.font.SysFont(None, max(18, block_size))

# PROGRESSION
# The list contains lists with the block number and the required number for the next stage.
# Resources are kept when a stage is completed and rewards are permanent.
stage_goals = [[8, 20], [3, 40], [9, 30], [10, 60], [11, 50], [12, 100]]
completed_stages = 0
mining_time_multiplier = 1.0
stage_message = ""
stage_message_until = 0
final_time = None

# MINING
# A block must be targeted continuously. Changing blocks or releasing resets it.
mining_target = None
mining_started_at = 0
mining_progress = 0.0
mining_rect = None


def get_mining_time(block_type): # Function to get the mining time of a given block type.
    # Times are in milliseconds because pygame.time.get_ticks() uses them.
    if block_type in (4, 9, 10, 11, 12):  # Deep rock and every ore because they should be harder to break.
        base_time = 3200 # = 3.2s
    else:
        base_time = 1600 # = 1.6s
    return base_time * mining_time_multiplier # Time multiplier changes as stages are completed.


def update_progression(): # Checks once per frame if a new stage is unlocked.
    # Makes a few variables global to assign new values to them.
    global completed_stages, mining_time_multiplier, move_acceleration, max_run_speed, jump_speed, stage_message, stage_message_until, final_time

    # The loop also handles resources collected before their stage begins.
    while completed_stages < len(stage_goals): # Checking whether stages remain.
        goal_block, goal_amount = stage_goals[completed_stages] # Gets the goal block (Iron) and the amount to finish the stage (60).
        if mined_blocks[goal_block] < goal_amount: # Checks if the current amount of the
            break # leaves the while loop, because there is nothing after it the function finishes.

        completed_stages += 1 # If it doesn't break this means the next stage is completed so completed stages += 1
        if completed_stages == 6:
            mining_time_multiplier = 0.0  # 0.0 for instant mining
            final_time = pygame.time.get_ticks() - game_start_time # Now that stage 6 is completed the final time is calculated by subtracting the startup time from the time overall.
            reward = "Instant mining + faster movement + higher jumps!"
        else:
            mining_time_multiplier /= 2
            reward = "Mining time halved!"
            if completed_stages in (2, 4): # For stages 2 and 4 the following text is added to "Mining time is halved"
                reward += " Faster movement + higher jumps!"

        if completed_stages == 2: # Movement update for stage 2
            move_acceleration = 0.05
            max_run_speed = 0.20
            jump_speed = 0.34
        elif completed_stages == 4: # Movement update for stage 4
            move_acceleration = 0.075
            max_run_speed = 0.30
            jump_speed = 0.42
        elif completed_stages == 6: # Movement update for stage 6
            move_acceleration = 0.10
            max_run_speed = 0.40
            jump_speed = 0.50

        stage_message = f"Stage {completed_stages} complete: {reward}"
        stage_message_until = pygame.time.get_ticks() + 5000 # Adds 5s to the time since pygame is running so the message can be turned of after those 5 seconds.

def update_mining(left_mouse_pressed, mouse_x, mouse_y): #Inputs: Is mouse pressed?, position of mouse.
    # Making some variables global allows the function to assign new values to these existing variables
    global mining_target, mining_started_at, mining_progress, mining_rect #Block being mined, when the mining started, value between 0 and 1 for progress, the rectangle for the progress bar.

    target = None
    mining_rect = None
    if left_mouse_pressed:
        # finding a 7x7 box around the player and turning them into rectangles to collide.
        for a in range(7):
            for b in range(7):
                x = 38 + rendering_offset + rendering_point + a
                y = -math.ceil(pos_y - 15) + b
                block_type = blocks_pos[x][y]
                if block_type in (0, 0.5, 5):  # Air, cave air and unmineable magma are excluded because they can't be mined.
                    continue # Skip because they can't be mined

                rect = pygame.Rect((x - rendering_offset - pos_x) * block_size - block_size * 10,
                                   screen_height - block_size - y * block_size - pos_y * block_size,
                                   block_size, block_size) # Making the minable blocks rects so collidepoint works.
                if rect.collidepoint(mouse_x, mouse_y): # Checking if the mouse is on the rect.
                    # Subtract the rendering_offset so generating columns to the left does not make the same world block look like a new target.
                    target = (x - rendering_offset, y, block_type)
                    mining_rect = rect

    if target is None:
        mining_target = None # Clears the remembered target
        mining_progress = 0.0 # progress is reset
        return # ends the function

    now = pygame.time.get_ticks() # How many Milliseconds the game has been running for
    if target != mining_target: # This will happen if you begin mining or switch to another block.
        mining_target = target
        mining_started_at = now
        mining_progress = 0.0 # progress is set to 0 as you have just begun mining.

    world_x, y, block_type = target # This unpacks the target’s three values into separate variables.
    mining_time = get_mining_time(block_type) # Find out how long a block takes to mine
    if mining_time == 0: # Sets it to 1.0 = 100% instantly, avoids division by 0
        mining_progress = 1.0
    else:
        mining_progress = min(1.0, (now - mining_started_at) / mining_time) # Calculate the percentage

    if mining_progress >= 1.0:
        x = world_x + rendering_offset # converts the stable world column back into its current list index.
        mined_blocks[block_type] += 1
        if blocks_pos_height[x] <= y: # blocks_pos_height[x] stores the terrain’s surface height in this column.
            blocks_pos[x][y] = 0  # Air above the surface
        else:
            blocks_pos[x][y] = 0.5  # Black cave air below the surface
        mining_target = None # Setting everything to 0 or None again because the block is now mined.
        mining_progress = 0.0
        mining_rect = None


def draw_progression():
    if final_time is not None:
        elapsed_time = final_time
    else:
        elapsed_time = pygame.time.get_ticks() - game_start_time
    minutes = elapsed_time // 60000 # Calculate Minutes (Dividing milliseconds by 60'000. // = integer division = whole numbers.)
    seconds = (elapsed_time % 60000) / 1000 # % Calculates the remainder of the division. This is divided by 1000 to convert ms to seconds.
    timer_text = f"Time: {minutes:02}:{seconds:04.1f}"

    if completed_stages < len(stage_goals):
        goal_block, goal_amount = stage_goals[completed_stages]
        lines = [timer_text,
                 f"Stage {completed_stages + 1} / 6",
                 f"Collect {goal_amount} {block_names[goal_block]}",
                 f"Progress: {mined_blocks[goal_block]} / {goal_amount}"]
    else:
        lines = [timer_text, "All 6 stages complete!", "Instant mining unlocked"]

    text_surfaces = [ui_font.render(line, True, white) for line in lines]
    panel_width = max(surface.get_width() for surface in text_surfaces) + 20
    line_height = ui_font.get_linesize()
    panel_rect = pygame.Rect(screen_width - panel_width - 20, 20,
                             panel_width, len(lines) * line_height + 20)
    pygame.draw.rect(screen, black, panel_rect)
    for i, surface in enumerate(text_surfaces):
        screen.blit(surface, (panel_rect.x + 10, panel_rect.y + 10 + i * line_height))

    if pygame.time.get_ticks() < stage_message_until: # Makes the message disappear after 5000 ms
        message_surface = ui_font.render(stage_message, True, white)
        message_rect = message_surface.get_rect(midtop=(screen_width // 2, 20))
        pygame.draw.rect(screen, black, message_rect.inflate(20, 10))
        screen.blit(message_surface, message_rect)


def draw_mining_progress():
    if mining_rect is not None: # If mining is happening
        # Draw on top of the block, after its texture has been drawn.
        bar_height = max(5, block_size // 5)
        bar_rect = pygame.Rect(mining_rect.x, mining_rect.bottom - 0.5 * block_size - 0.5 * bar_height,
                               block_size, bar_height)
        pygame.draw.rect(screen, black, bar_rect)
        fill_rect = pygame.Rect(bar_rect.x, bar_rect.y,
                                int(bar_rect.width * mining_progress), bar_rect.height)
        pygame.draw.rect(screen, (70, 220, 90), fill_rect)
        pygame.draw.rect(screen, white, bar_rect, 1)

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

        if tree_type_mode == 1:
            for a in range(len(tree)):
                for b in range(len(tree[a])):
                    if blocks_pos[a + z][b + ground_height + 40] == 0 or blocks_pos[a + z][b + ground_height + 40] == 1:
                        blocks_pos[a + z][b + ground_height + 40] = tree[a][b]

        if tree_type_mode == 2:
            for a in range(len(tree_2)):
                for b in range(len(tree_2[a])):
                    if blocks_pos[a + z][b + ground_height + 40] == 0 or blocks_pos[a + z][b + ground_height + 40] == 1:
                        blocks_pos[a + z][b + ground_height + 40] = tree_2[a][b]

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


def draw_hotbar():
    # Centered hotbar at the bottom of the screen.
    slot_gap = 14
    hotbar_width = len(placeable_blocks) * block_size + (len(placeable_blocks) - 1) * slot_gap
    hotbar_x = screen_width // 2 - hotbar_width // 2
    hotbar_y = screen_height - block_size - 20

    for i, block_type in enumerate(placeable_blocks):
        slot_rect = pygame.Rect(hotbar_x + i * (block_size + slot_gap), hotbar_y, block_size, block_size)
        pygame.draw.rect(screen, white, slot_rect)
        screen.blit(block_images[block_type], slot_rect)

        if block_type == selected_block:
            # Draw the selected border slightly outside the block so it is easier to see.
            pygame.draw.rect(screen, (255, 0, 0), slot_rect.inflate(8, 8), 4)
        else:
            pygame.draw.rect(screen, black, slot_rect, 1)

        # Show how many of this block are currently available.
        count_surface = ui_font.render(str(mined_blocks[block_type]), True, black)
        screen.blit(count_surface, (slot_rect.x + 2, slot_rect.bottom - count_surface.get_height()))


on_ground = False
done = False
game_start_time = pygame.time.get_ticks() # Gets the time that has already elapsed while the game was starting up.
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
        if event.type == pygame.KEYDOWN:
            number_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                           pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]
            if event.key in number_keys:
                hotbar_index = number_keys.index(event.key)
                if hotbar_index < len(placeable_blocks):
                    selected_block = placeable_blocks[hotbar_index]

        if event.type == pygame.MOUSEWHEEL:
            selected_index = placeable_blocks.index(selected_block)
            selected_block = placeable_blocks[(selected_index - event.y) % len(placeable_blocks)]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        mov_x += move_acceleration
    if keys[pygame.K_a]:
        mov_x -= move_acceleration
    if keys[pygame.K_w] or keys[pygame.K_SPACE]:
        if on_ground and pos_y >= -75: # Stops the player from jumping above a certain height to prevent him from going upwards infinitely. (And from crashing the Game.)
            mov_y = mov_y - jump_speed
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

    update_mining(left_mouse_pressed, mouse_x, mouse_y)
    update_progression()

    #Checking 7x7 blocks around player
    if right_mouse_pressed:
        for a in range(7):
            for b in range(7):
                x = 38 + rendering_offset + rendering_point + a
                y = -math.ceil(pos_y - 15) + b

                if blocks_pos[x][y] in (0, 0.5):
                    rect_1 = pygame.Rect((a + 38 - pos_x) * block_size - block_size * 10,
                                         screen_height - block_size - y * block_size - (pos_y * block_size),
                                         block_size, block_size)
                    if rect_1.colliderect(mouse_following_rect) and not rect_1.colliderect(player_rect):
                        if mined_blocks[selected_block] > 0:
                            blocks_pos[x][y] = selected_block
                            mined_blocks[selected_block] -= 1

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

    draw_mining_progress()

    # DRAWING THE HOTBAR
    draw_hotbar()
    draw_progression()

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
        if one_percent == 99: # Take another number for 1% chance to change tree type mode.
            tree_type_mode = random.randint(1, 2)
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
            if tree_type_mode == 1:
                for a in range(len(tree)):
                    for b in range(len(tree[a])):
                        if blocks_pos[a + 83 - 5 + new_render_positive - new_render_negative][b + ground_height + 40] == 0 or blocks_pos[a + 83 - 5 + new_render_positive - new_render_negative][b + ground_height + 40] == 1:
                            blocks_pos[a + 83 - 5 + new_render_positive - new_render_negative][b + ground_height + 40] = tree[a][b]

            if tree_type_mode == 2:
                for a in range(len(tree_2)):
                    for b in range(len(tree_2[a])):
                        if blocks_pos[a + 83 - 5 + new_render_positive - new_render_negative][b + ground_height + 40] == 0 or blocks_pos[a + 83 - 5 + new_render_positive - new_render_negative][b + ground_height + 40] == 1:
                            blocks_pos[a + 83 - 5 + new_render_positive - new_render_negative][b + ground_height + 40] = tree_2[a][b]

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
        if one_percent == 99:
            tree_type_mode_negative = random.randint(1, 2)

        if next_tree_negative == 0:

            ground_height = blocks_pos_height[5]

            if tree_type_mode_negative == 1:
                for a in range(len(tree)):
                    for b in range(len(tree[a])):
                        if blocks_pos[a + 3][b + ground_height] == 0 or blocks_pos[a + 3][b + ground_height] == 1:
                            blocks_pos[a + 3][b + ground_height] = tree[a][b]

            if tree_type_mode_negative == 2:
                for a in range(len(tree_2)):
                    for b in range(len(tree_2[a])):
                        if blocks_pos[a + 3][b + ground_height] == 0 or blocks_pos[a + 3][b + ground_height] == 1:
                            blocks_pos[a + 3][b + ground_height] = tree_2[a][b]

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