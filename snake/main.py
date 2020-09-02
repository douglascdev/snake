import pygame
from enum import Enum
from pygame import Rect
from typing import Union, Tuple, List
from random import choice


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


class Game:
    DEFAULT_RECT_SIZE = 40
    DEFAULT_RECT = Rect(0, 0, DEFAULT_RECT_SIZE, DEFAULT_RECT_SIZE)


class Screen:
    NUM_BLOCKS_X = 20
    NUM_BLOCKS_Y = 15
    block_size = Game.DEFAULT_RECT_SIZE
    WIDTH, HEIGHT = block_size * NUM_BLOCKS_X, block_size * NUM_BLOCKS_Y
    RECT = WIDTH, HEIGHT
    FPS = 60


class Direction(Enum):
    s = Game.DEFAULT_RECT_SIZE
    # Coordinates to sum to create movement at a step for each direction
    N, S, W, E = (0, -s), (0, s), (-s, 0), (s, 0)


class SnakeUnit(pygame.sprite.Sprite):
    """
    Represents a single block of the snake on the screen
    """

    def __init__(self, place_after=None):
        pygame.sprite.Sprite.__init__(self)
        # The RenderPlain group has a draw method that will use the rect and image attributes
        self.rect = (
            Game.DEFAULT_RECT.copy()
            if place_after is None
            else place_after.move(Game.DEFAULT_RECT_SIZE, 0)
        )
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self.image.fill(Color.WHITE)


class Snake(pygame.sprite.RenderPlain):
    """
    Group of sprites(snake units) that compose the full snake
    """

    def __init__(self, *snake_units):
        super().__init__(*snake_units)
        self.direction = Direction.E
        self.frametime_counter = 0
        self.frametime_for_step = 256
        self.shortcuts = {
            pygame.K_UP: Direction.N,
            pygame.K_DOWN: Direction.S,
            pygame.K_RIGHT: Direction.E,
            pygame.K_LEFT: Direction.W,
        }

    def update(self, frametime: int, food_group: pygame.sprite.Group):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in self.shortcuts.keys():
                event: pygame.event.Event
                self.direction = self.shortcuts.get(event.key)


        # Using frametime keeps the movement relatively stable despite the FPS the game is running at
        if self.frametime_counter >= self.frametime_for_step:
            self.step()
            self.frametime_counter = 0
        else:
            self.frametime_counter += frametime

        head: SnakeUnit = self.sprites()[0]
        collided_foods = pygame.sprite.spritecollide(head, food_group, dokill=True)
        if len(collided_foods) > 0:
            food_group.add(Food(self))
            last_unit = self.sprites()[len(self.sprites()) - 1]
            # TODO: this position for the new last unit is wrong
            self.add(SnakeUnit(place_after=last_unit.rect))

    def step(self):
        """
        Move all snake units by one step
        """
        sprites: List[SnakeUnit] = self.sprites()
        sprites_iter = iter(sprites)
        head: SnakeUnit = next(sprites_iter)
        last_iter_rect: pygame.rect.Rect = head.rect.copy()
        x_mov = self.direction.value[0]
        y_mov = self.direction.value[1]
        head.rect.move_ip(x_mov, y_mov)
        for sprite in sprites_iter:
            new_rect = last_iter_rect.copy()
            last_iter_rect = sprite.rect.copy()
            sprite.rect = new_rect.copy()


class Food(pygame.sprite.Sprite):
    def __init__(self, snake_group: Snake):
        pygame.sprite.Sprite.__init__(self)
        # TODO: use group collision check here instead of passing every rect as argument
        self.rect = random_pos_rect(
            Game.DEFAULT_RECT, [sprite.rect for sprite in snake_group.sprites()]
        )
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self.image.fill(Color.WHITE)


def random_pos_rect(size: Union[Rect, Tuple[int, int]], excluded_rects: List[Rect]) -> Rect:
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
    range_for_rect = lambda max_size: range(0, max_size, Game.DEFAULT_RECT_SIZE)
    # A nested for in a single line... Python is cool af
    possible_screen_rects = (
        Rect(i, j, rect.w, rect.h) for i in range_for_rect(max_width) for j in range_for_rect(max_height)
    )
    rects_without_collision = [
        rect
        for rect in possible_screen_rects
        if not rect.collidelist(excluded_rects) >= 0
    ]
    return choice(rects_without_collision)


if __name__ == "__main__":
    pygame.display.init()
    pg_screen = pygame.display.set_mode(Screen.RECT)
    clock = pygame.time.Clock()
    s = Game.DEFAULT_RECT_SIZE
    u1 = SnakeUnit(place_after=Game.DEFAULT_RECT.move(s * 3, 0))
    u2 = SnakeUnit(place_after=u1.rect)
    u3 = SnakeUnit(place_after=u2.rect)
    snake = Snake(u1, u2, u3)
    foods = pygame.sprite.RenderPlain()
    foods.add(Food(snake))

    frametime = 0
    while True:
        pg_screen.fill(Color.BLACK)
        snake.update(frametime, foods)
        foods.update()
        snake.draw(pg_screen)
        foods.draw(pg_screen)
        pygame.display.update()
        frametime = clock.tick(Screen.FPS)
