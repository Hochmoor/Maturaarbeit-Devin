import pygame

pygame.init()

player_size = 1000


speed = 60
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)

# Create fullscreen window at desktop resolution
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()

player_img = pygame.image.load("texture.png").convert_alpha()
player_img = pygame.transform.smoothscale(player_img, (player_size, player_size))


# Player settings
pos_x = 50
pos_y = screen_height - 100
mov_x = 0
mov_y = 0
drag = 0.985

done = False
while not done:
    screen.fill(white)

    pos_x += mov_x
    pos_y += mov_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True  # ESC to quit fullscreen

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        mov_x += 0.2
    if keys[pygame.K_a]:
        mov_x -= 0.2
    if keys[pygame.K_s]:
        mov_y += 0.2
    if keys[pygame.K_w]:
        mov_y -= 0.2

    mov_x *= drag
    mov_y *= drag

    # Screen bounds (dynamic!)
    if pos_x < 0:
        pos_x = 0
        mov_x = 0
    if pos_y < 0:
        pos_y = 0
        mov_y = 0
    if pos_x > screen_width - player_size:
        pos_x = screen_width - player_size
        mov_x = 0
    if pos_y > screen_height - player_size:
        pos_y = screen_height - player_size
        mov_y = 0

    screen.blit(player_img, (pos_x, pos_y))
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
