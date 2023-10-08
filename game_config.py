import pygame
GAME_FPS = 60
GAME_WIDTH = 900
GAME_HEIGHT = 500
GAME_CAPTION = "SHOOTIN' SPACESHIPS"
CHAR_VEL = 3
CHAR_MAX_BULLETS = 3
CHAR_MAX_HEALTH = 10
BULLET_VEL = 15

BORDER = {
    "x_pos": GAME_WIDTH // 2 - 5,
    "y_pos": 0,
    "width": 10,
    "height": GAME_HEIGHT
}

WHITE_RGB = (255, 255, 255)
BLACK_RGB = (0, 0, 0)
RED_RGB = (255, 0, 0)
YELLOW_RGB = (255, 255, 0)

SPACESHIP_WIDTH = 55 
SPACESHIP_HEIGHT = 40

AUDIO_ASSETS = {
    "fire": 'Assets/Gun_Silencer.mp3',
    "hit": 'Assets/Grenade_1.mp3'
}

IMAGE_ASSETS = {
    "BACKGROUND": 'Assets/space.png',
    "YELLOW_SPACESHIP": "Assets/spaceship_yellow.png",
    "RED_SPACESHIP": "Assets/spaceship_red.png",
}

SPACE = pygame.transform.scale(pygame.image.load(
    IMAGE_ASSETS["BACKGROUND"]), (GAME_WIDTH, GAME_HEIGHT))

def draw_window(
        WIN, 
        HEALTH_FONT,
        BORDER_RECT,
        red_spaceship,
        yellow_spaceship
    ):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK_RGB, BORDER_RECT)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_spaceship.health), 1, WHITE_RGB)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_spaceship.health), 1, WHITE_RGB)
    WIN.blit(red_health_text, (GAME_WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(yellow_spaceship.load_image(), (yellow_spaceship.pos_x, yellow_spaceship.pos_y))
    WIN.blit(red_spaceship.load_image(), (red_spaceship.pos_x, red_spaceship.pos_y))

    for bullet in red_spaceship.bullets:
        pygame.draw.rect(WIN, RED_RGB, bullet)

    for bullet in yellow_spaceship.bullets:
        pygame.draw.rect(WIN, YELLOW_RGB, bullet)

    pygame.display.update()

    return

def draw_winner(WIN, WINNER_FONT, text):
    draw_text = WINNER_FONT.render(text, 1, WHITE_RGB)
    WIN.blit(
        draw_text, (GAME_WIDTH // 2 - draw_text.get_width() // 2, GAME_HEIGHT // 2 - draw_text.get_height() // 2)
    )
    pygame.display.update()
    pygame.time.delay(5000)
    return