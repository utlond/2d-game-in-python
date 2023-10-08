import pygame
import game_config as g_c
import Spaceship as s_s
pygame.font.init()
pygame.mixer.init()

WIN = pygame.display.set_mode((g_c.GAME_WIDTH, g_c.GAME_HEIGHT))
pygame.display.set_caption(g_c.GAME_CAPTION)

BORDER = pygame.Rect(g_c.BORDER["x_pos"], g_c.BORDER["y_pos"], g_c.BORDER["width"], g_c.BORDER["height"])

BULLET_FIRE_SOUND = pygame.mixer.Sound(g_c.AUDIO_ASSETS["fire"])
BULLET_HIT_SOUND = pygame.mixer.Sound(g_c.AUDIO_ASSETS["hit"])

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


def main():

    yellow_spaceship = s_s.Spaceship(
        g_c.IMAGE_ASSETS["YELLOW_SPACESHIP"],
        {
            "width": g_c.SPACESHIP_WIDTH,
            "height": g_c.SPACESHIP_HEIGHT,
            "rotation": 90
        },
        "left"
    )
    
    red_spaceship = s_s.Spaceship(
        g_c.IMAGE_ASSETS["RED_SPACESHIP"],
        {
            "width": g_c.SPACESHIP_WIDTH,
            "height": g_c.SPACESHIP_HEIGHT,
            "rotation": 270
        },
        "right"
    )


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(g_c.GAME_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                yellow_spaceship.fire_bullets(event, BULLET_FIRE_SOUND)
                red_spaceship.fire_bullets(event, BULLET_FIRE_SOUND)

        winner_text = ""
        if red_spaceship.health == 0:
            winner_text = "Yellow Wins!"

        if yellow_spaceship.health == 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            g_c.draw_winner(WIN, WINNER_FONT, winner_text)
            break
       
        yellow_spaceship.move()
        red_spaceship.move()
        yellow_spaceship.handle_bullets(red_spaceship, BULLET_HIT_SOUND)
        red_spaceship.handle_bullets(yellow_spaceship, BULLET_HIT_SOUND)
        

        g_c.draw_window(WIN, HEALTH_FONT, BORDER, red_spaceship, yellow_spaceship)
    
    main() if run else pygame.quit()
    

if __name__ == "__main__":
    main()
