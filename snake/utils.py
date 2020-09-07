from random import choice
from typing import Union, Tuple, List

import pygame
from pygame.rect import Rect

from snake.constants import Screen, Game, Color


def random_pos_rect(
    size: Union[Rect, Tuple[int, int]], excluded_rects: List[Rect]
) -> Rect:
    """
    Generates random position within the screen. Excludes points that would be out of screen and possibly colliding
    objects, which can be passed though a list.
    :param size: rect or tuple with object's width and height
    :param excluded_rects: list of positions that will be excluded from the possible rectangles
    :return: rect with a random position within the screen, with the same dimensions
    """
    size_is_rect = isinstance(size, Rect)
    rect = size if size_is_rect else Rect(0, 0, size[0], size[1])
    max_width = Screen.WIDTH - rect.w
    max_height = Screen.HEIGHT - rect.h
    rects_without_collision = [
        rect
        for rect in possible_rects(max_width, max_height)
        if not rect.collidelist(excluded_rects) >= 0
    ]
    return choice(rects_without_collision)


def possible_rects(max_width: int, max_height: int):
    range_for_rect = lambda max_size: range(0, max_size, Game.DEFAULT_RECT_SIZE)
    possible_screen_rects = (
        Rect(i, j, Game.DEFAULT_RECT_SIZE, Game.DEFAULT_RECT_SIZE)
        for i in range_for_rect(max_width)
        for j in range_for_rect(max_height)
    )
    return possible_screen_rects


def checkered_surface(screen: pygame.Surface) -> pygame.Surface:
    checkered = screen.copy().convert_alpha()
    checkered.fill(Color.GREY)

    for n, rect in enumerate(possible_rects(Screen.WIDTH, Screen.HEIGHT)):
        if n % 2 == 0:
            pygame.draw.rect(checkered, Color.LIGHT_GREY, rect)

    return checkered


def score_update(score, screen):
    font = pygame.font.SysFont("comicsans", Game.DEFAULT_RECT_SIZE, True)
    text = font.render(
        "Score: " + str(score), 100, Color.WHITE
    )  # Arguments are: text, anti-aliasing, color
    screen.blit(
        text, (Screen.WIDTH - (4 * Screen.block_size), int(Game.DEFAULT_RECT_SIZE / 10))
    )
