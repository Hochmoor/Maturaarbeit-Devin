import pygame

pygame.init()

# Open a fullscreen window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

running = True

while running:
    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Allow closing with ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False



    # Change color depending on mouse button state
    if left_mouse_pressed:
        color = (0, 255, 0)
    else:
        color = (255, 0, 0)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw a 1x1 pixel rectangle at the mouse position
    pygame.draw.rect(screen, color, (mouse_x, mouse_y, 1, 1))

    pygame.display.flip()

    # Limit FPS
    clock.tick(60)

pygame.quit()