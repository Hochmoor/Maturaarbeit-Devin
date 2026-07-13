import pygame
import random
import math

# --- Configuration ---
WIDTH, HEIGHT = 800, 400
FPS = 60
SCALE = 0.02  # How "stretched" the hills are (Frequency)
AMPLITUDE = 100  # How tall the hills are
SPEED = 2  # Scrolling speed

# --- Simple 1D Noise Logic ---
# To keep this "pure Python," we'll use a simple interpolation
# function to simulate the Perlin effect.
seed_values = [random.uniform(-1, 1) for _ in range(1000)]


def get_noise(x):
    # Determine the two points on our "ruler" we are between
    p1 = int(x) % 1000
    p2 = (p1 + 1) % 1000

    # How far are we between those points (0.0 to 1.0)
    frac = x - int(x)

    # Smoothstep interpolation (the "Fade" function)
    t = frac * frac * (3 - 2 * frac)

    # Blend the two random values
    return seed_values[p1] * (1 - t) + seed_values[p2] * t


# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
offset = 0

running = True
while running:
    screen.fill((135, 206, 235))  # Sky Blue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Terrain Generation ---
    points = []
    # We add (0, HEIGHT) and (WIDTH, HEIGHT) to make it a solid shape
    points.append((0, HEIGHT))

    for x in range(0, WIDTH + 1):
        # Calculate noise based on X + the current scroll offset
        noise_val = get_noise((x + offset) * SCALE)

        # Map noise to screen Y (centered at middle of screen)
        y = (HEIGHT // 2) + (noise_val * AMPLITUDE)
        points.append((x, y))

    points.append((WIDTH, HEIGHT))

    # --- Drawing ---
    # Draw the ground as a solid polygon
    pygame.draw.polygon(screen, (34, 139, 34), points)  # Forest Green

    # Update scroll offset to make it "move"
    offset += SPEED

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()