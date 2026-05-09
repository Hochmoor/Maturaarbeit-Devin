import pygame
import random
import math

# --------------------
# INIT
# --------------------
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centered Player Survival")
clock = pygame.time.Clock()

# --------------------
# CONSTANTS
# --------------------
PLAYER_SPEED = 5
MONSTER_SPEED = 2
SPAWN_DISTANCE = 500
MONSTER_RADIUS = 15
PLAYER_RADIUS = 20

WHITE = (255, 255, 255)
RED = (220, 50, 50)
BLUE = (50, 120, 255)
BLACK = (0, 0, 0)

# --------------------
# PLAYER (world position)
# --------------------
player_pos = pygame.Vector2(0, 0)

# --------------------
# MONSTERS (world positions)
# --------------------
monsters = []

def spawn_monster():
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        x = random.randint(-SPAWN_DISTANCE, SPAWN_DISTANCE)
        y = -SPAWN_DISTANCE
    elif side == "bottom":
        x = random.randint(-SPAWN_DISTANCE, SPAWN_DISTANCE)
        y = SPAWN_DISTANCE
    elif side == "left":
        x = -SPAWN_DISTANCE
        y = random.randint(-SPAWN_DISTANCE, SPAWN_DISTANCE)
    else:
        x = SPAWN_DISTANCE
        y = random.randint(-SPAWN_DISTANCE, SPAWN_DISTANCE)

    monsters.append(pygame.Vector2(x, y))

# Spawn some initial monsters
for _ in range(6):
    spawn_monster()

# --------------------
# MAIN LOOP
# --------------------
running = True
while running:
    dt = clock.tick(240)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --------------------
    # INPUT
    # --------------------
    keys = pygame.key.get_pressed()
    movement = pygame.Vector2(0, 0)

    if keys[pygame.K_w]:
        movement.y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        movement.y += PLAYER_SPEED
    if keys[pygame.K_a]:
        movement.x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        movement.x += PLAYER_SPEED

    if movement.length() > 0:
        movement = movement.normalize() * PLAYER_SPEED

    # Move player in world space
    player_pos += movement

    # --------------------
    # MONSTER MOVEMENT
    # --------------------
    for monster in monsters:
        direction = player_pos - monster
        if direction.length() > 0:
            direction = direction.normalize()
        monster += direction * MONSTER_SPEED

        # Collision check
        if monster.distance_to(player_pos) < PLAYER_RADIUS + MONSTER_RADIUS:
            print("GAME OVER")
            running = False

    # --------------------
    # DRAW
    # --------------------
    screen.fill(BLACK)

    # Camera offset (player always centered)
    camera_offset = pygame.Vector2(
        WIDTH // 2 - player_pos.x,
        HEIGHT // 2 - player_pos.y
    )

    # Draw monsters
    for monster in monsters:
        draw_pos = monster + camera_offset
        pygame.draw.circle(screen, RED, draw_pos, MONSTER_RADIUS)

    # Draw player (always center)
    pygame.draw.circle(
        screen,
        BLUE,
        (WIDTH // 2, HEIGHT // 2),
        PLAYER_RADIUS
    )

    pygame.display.flip()

pygame.quit()