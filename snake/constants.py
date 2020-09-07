from enum import Enum
from pygame.rect import Rect
from pygame.color import Color


class Color:
    WHITE = Color(200, 200, 200)
    BLACK = Color(0, 0, 0)
    GREEN = Color(0, 200, 0)
    RED = Color(230, 0, 0)
    GREY = Color(50, 50, 50)
    LIGHT_GREY = Color(60, 60, 60)


class Game:
    DEFAULT_RECT_SIZE = 40
    DEFAULT_RECT = Rect(0, 0, DEFAULT_RECT_SIZE, DEFAULT_RECT_SIZE)
    FONT = {"name": "comicsans", "size": 40, "color": Color.WHITE}
    NUM_UNITS_RESPAWN = 3
    FRAMETIME_WAITED = 64


class Direction(Enum):
    s = Game.DEFAULT_RECT_SIZE
    # Coordinates to sum to create movement at a step for each direction
    N, S, W, E = (0, -s), (0, s), (-s, 0), (s, 0)


class Screen:
    NUM_BLOCKS_X = 20
    NUM_BLOCKS_Y = 15
    block_size = Game.DEFAULT_RECT_SIZE
    WIDTH, HEIGHT = block_size * NUM_BLOCKS_X, block_size * NUM_BLOCKS_Y
    RECT = Rect(0, 0, WIDTH, HEIGHT)
    FPS = 60
