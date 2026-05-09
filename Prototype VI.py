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
BULLET_SPEED = 10

PLAYER_RADIUS = 20
MONSTER_RADIUS = 100
BULLET_RADIUS = 5

MAX_HEALTH = 100

SPAWN_DISTANCE = 1000

WHITE = (255, 255, 255)
RED = (220, 50, 50)
BLUE = (50, 120, 255)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)

monster_img = pygame.image.load("monster.jpg").convert_alpha()
monster_img = pygame.transform.smoothscale(monster_img, (MONSTER_RADIUS, MONSTER_RADIUS))

# --------------------
# CLASSES
# --------------------

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.health = MAX_HEALTH

    def move(self, direction):
        if direction.length() > 0:
            direction = direction.normalize() * PLAYER_SPEED
        self.pos += direction

    def draw(self):
        pygame.draw.circle(
            screen,
            BLUE,
            (WIDTH // 2, HEIGHT // 2),
            PLAYER_RADIUS
        )

class Monster:
    def __init__(self, pos):
        self.pos = pos

    def update(self, player_pos):
        direction = player_pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * MONSTER_SPEED

    def draw(self, camera_offset):
        draw_pos = self.pos + camera_offset
        screen.blit(monster_img, (draw_pos))


class Bullet:
    def __init__(self, pos, direction):
        self.pos = pos.copy()
        self.direction = direction.normalize()

    def update(self):
        self.pos += self.direction * BULLET_SPEED

    def draw(self, camera_offset):
        draw_pos = self.pos + camera_offset
        pygame.draw.circle(screen, WHITE, draw_pos, BULLET_RADIUS)

# --------------------
# GAME OBJECTS
# --------------------
player = Player()
monsters = []
bullets = []

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
    monsters.append(Monster(pygame.Vector2(x, y)))

for _ in range(5000):
    spawn_monster()

print(monsters)

# --------------------
# MAIN LOOP
# --------------------
running = True
while running:
    clock.tick(60)

    # --------------------
    # EVENTS
    # --------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            direction = mouse_pos - pygame.Vector2(WIDTH // 2, HEIGHT // 2)
            bullets.append(Bullet(player.pos, direction))

    # --------------------
    # INPUT
    # --------------------
    keys = pygame.key.get_pressed()
    movement = pygame.Vector2(0, 0)

    if keys[pygame.K_w]:
        movement.y -= 1
    if keys[pygame.K_s]:
        movement.y += 1
    if keys[pygame.K_a]:
        movement.x -= 1
    if keys[pygame.K_d]:
        movement.x += 1

    player.move(movement)

    # --------------------
    # UPDATE MONSTERS
    # --------------------
    for monster in monsters[:]:
        monster.update(player.pos)

        if monster.pos.distance_to(player.pos) < PLAYER_RADIUS + 0.5 * MONSTER_RADIUS: #0.5 bcs monster texture not optimal
            player.health -= 1

    # --------------------
    # UPDATE BULLETS
    # --------------------
    for bullet in bullets[:]:
        bullet.update()

        for monster in monsters[:]:
            if bullet.pos.distance_to(monster.pos) < BULLET_RADIUS + MONSTER_RADIUS:
                bullets.remove(bullet)
                monsters.remove(monster)
                spawn_monster()
                break

    if player.health <= 0:
        print("GAME OVER")
        running = False

    # --------------------
    # DRAW
    # --------------------
    screen.fill(BLACK)

    camera_offset = pygame.Vector2(
        WIDTH // 2 - player.pos.x,
        HEIGHT // 2 - player.pos.y
    )

    for monster in monsters:
        monster.draw(camera_offset)

    for bullet in bullets:
        bullet.draw(camera_offset)

    player.draw()

    # --------------------
    # HEALTH BAR
    # --------------------
    bar_width = 200
    bar_height = 20
    health_ratio = player.health / MAX_HEALTH

    pygame.draw.rect(screen, RED, (20, 20, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (20, 20, bar_width * health_ratio, bar_height))

    pygame.display.flip()

pygame.quit()
