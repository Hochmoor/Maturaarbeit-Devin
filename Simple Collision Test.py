import pygame

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Player stays in the center
player = pygame.Rect(375, 275, 50, 50)

# Block to demonstrate Collision
block = pygame.Rect(100, 275, 50, 50)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # The block is moved, not the player to keep the concept of the "real" game
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        block.x += 5
    if keys[pygame.K_d]:
        block.x -= 5
    if keys[pygame.K_w]:
        block.y += 5
    if keys[pygame.K_s]:
        block.y -= 5

    # Collision detection
    collision = player.colliderect(block)

    # Drawing
    screen.fill((0, 0, 0)) # Black Background

    pygame.draw.rect(screen, (0, 200, 0), player)
    pygame.draw.rect(screen, (200, 50, 50), block)

    # Show collision by turning block white
    if collision:
        pygame.draw.rect(screen, (255, 255, 255), block)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()