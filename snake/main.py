import pygame

from snake.constants import Screen, Game
from snake.entity import Snake, Food
from snake.utils import checkered_surface, score_update


def main():
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("Snake with pygame")
    pg_screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
    background = checkered_surface(pg_screen)
    clock = pygame.time.Clock()
    snake = Snake()
    foods = pygame.sprite.RenderPlain()
    foods.add(Food(snake))

    run = True
    frametime = 0
    while run:
        pg_screen.blit(background, (0, 0))
        snake.update(frametime, foods)
        foods.update()
        snake.draw(pg_screen)
        foods.draw(pg_screen)
        score = len(snake.sprites()) - Game.NUM_UNITS_RESPAWN
        score_update(score, pg_screen)
        pygame.display.update()
        frametime = clock.tick(Screen.FPS)


if __name__ == "__main__":
    main()
