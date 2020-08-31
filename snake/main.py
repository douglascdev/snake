import pygame
from pygame import Rect
from typing import List, Union, Tuple
from random import choice


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


class Screen:
    WIDTH, HEIGHT = 800, 600
    RECT = WIDTH, HEIGHT
    FPS = 60


class Game:
    DEFAULT_RECT_SIZE = 20
    DEFAULT_RECT = Rect(0, 0, DEFAULT_RECT_SIZE, DEFAULT_RECT_SIZE)


def generate_random_pos(
    size: Union[Rect, Tuple[int, int]], excluded_rects: List[Rect] = [],
) -> Rect:
    """
    Generates random position within the screen. Excludes points that would be out of screen and possibly colliding
    objects, which can be passed though a list.
    TODO:Performance for excluding points would probably be improved by keeping a full list of points on screen in
    memory for the function and only limiting the width and height within the generator. Checking if the excluded_rects
    is empty and skipping exclusion too.
    :param size: rect or tuple with object's width and height
    :param excluded_rects: list of positions that will be excluded from the possible rectangles
    :return: rect with a random position within the screen, with the same dimensions
    """
    size_is_rect = isinstance(size, Rect)
    rect = size if size_is_rect else Rect(0, 0, size[0], size[1])
    max_width = Screen.WIDTH - rect.w
    max_height = Screen.HEIGHT - rect.h
    # A nested for in a single line... Python is cool af
    possible_screen_rects = (
        Rect(i, j, rect.w, rect.h) for i in range(max_width) for j in range(max_height)
    )
    points_without_collision = [
        rect
        for rect in possible_screen_rects
        if not rect.collidelist(excluded_rects) >= 0
    ]
    return choice(points_without_collision)


def generate_food() -> pygame.rect.Rect:
    return pygame.draw.rect(
        pg_screen, Color.WHITE, generate_random_pos(Game.DEFAULT_RECT)
    )


if __name__ == "__main__":
    pygame.display.init()
    pg_screen = pygame.display.set_mode(Screen.RECT)
    clock = pygame.time.Clock()
    food_rect = generate_food()

    while True:
        pg_screen.fill(Color.BLACK)
        food_rect = pygame.draw.rect(pg_screen, Color.WHITE, food_rect)
        pygame.display.update()
        clock.tick(Screen.FPS)
