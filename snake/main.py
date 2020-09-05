import pygame
import sys
from enum import Enum
from pygame import Rect
from typing import Union, Tuple, List
from random import choice
from pygame import event, gfxdraw


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GREY = (50, 50, 50)
    LIGHT_GREY = (60, 60, 60)


class Game:
    DEFAULT_RECT_SIZE = 40
    DEFAULT_RECT = Rect(0, 0, DEFAULT_RECT_SIZE, DEFAULT_RECT_SIZE)


class Screen:
    NUM_BLOCKS_X = 20
    NUM_BLOCKS_Y = 15
    block_size = Game.DEFAULT_RECT_SIZE
    WIDTH, HEIGHT = block_size * NUM_BLOCKS_X, block_size * NUM_BLOCKS_Y
    RECT = Rect(0, 0, WIDTH, HEIGHT)
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
        self.image.fill(Color.GREEN)
        pygame.draw.rect(self.image, Color.BLACK, self.rect, 2)


class Snake(pygame.sprite.RenderPlain):
    """
    Group of sprites(snake units) that compose the full snake
    """

    def __init__(self, *snake_units):
        super().__init__(*snake_units)
        self.direction = Direction.E
        self.new_direction = self.direction
        self.frametime_counter = 0
        self.frametime_for_step = 64
        self.shortcuts = {
            pygame.K_UP: Direction.N,
            pygame.K_DOWN: Direction.S,
            pygame.K_RIGHT: Direction.E,
            pygame.K_LEFT: Direction.W,
        }

    def update(self, frametime: int, food_group: pygame.sprite.Group):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in self.shortcuts.keys():
                event: pygame.event.Event
                # Prevents movement to the opposite direction(snake would collide with itself)
                opposites = {
                    Direction.N: Direction.S,
                    Direction.S: Direction.N,
                    Direction.W: Direction.E,
                    Direction.E: Direction.W,
                }
                direction = self.shortcuts.get(event.key)
                if opposites.get(self.direction) != direction:
                    self.new_direction = direction

        # Using frametime keeps the movement relatively stable despite the FPS the game is running at
        if self.frametime_counter >= self.frametime_for_step:
            self.step()
            self.frametime_counter = 0
            head: SnakeUnit = self.sprites().pop()
            collided_foods = pygame.sprite.spritecollide(head, food_group, dokill=True)
            if len(collided_foods) > 0:
                food_group.add(Food(self))
                new_head = SnakeUnit()
                x_mov = self.direction.value[0]
                y_mov = self.direction.value[1]
                new_head.rect = head.rect.move(x_mov, y_mov)
                self.add(new_head)

            # Correct snake position if it is out of screen
            head: SnakeUnit = self.sprites().pop()
            if head.rect.x < 0:
                head.rect.x = Screen.WIDTH - head.rect.w
            elif head.rect.x > Screen.WIDTH - head.rect.w:
                head.rect.x = 0
            elif head.rect.y < 0:
                head.rect.y = Screen.HEIGHT - head.rect.h
            elif head.rect.y > Screen.HEIGHT - head.rect.h:
                head.rect.y = 0

        else:
            self.frametime_counter += frametime

    def step(self):
        """
        Move all snake units by one step
        """
        sprites: List[SnakeUnit] = self.sprites()
        head: SnakeUnit = sprites.pop()
        self.direction = self.new_direction
        x_mov = self.direction.value[0]
        y_mov = self.direction.value[1]
        previous_sprite_rect = head.rect.copy()
        head.rect.move_ip(x_mov, y_mov)
        for sprite in reversed(sprites):
            sprite_rect_bkp = sprite.rect
            sprite.rect = previous_sprite_rect
            previous_sprite_rect = sprite_rect_bkp


class Food(pygame.sprite.Sprite):
    def __init__(self, snake_group: Snake):
        pygame.sprite.Sprite.__init__(self)
        self.rect = random_pos_rect(
            Game.DEFAULT_RECT, [sprite.rect for sprite in snake_group.sprites()]
        )
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        x, y = int(self.rect.w / 2) - 1, int(self.rect.h / 2) - 1
        radius = int(Game.DEFAULT_RECT_SIZE / 2) - 1
        gfxdraw.aacircle(self.image, x, y, radius, Color.RED)
        gfxdraw.filled_circle(self.image, x, y, radius, Color.RED)


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
    checkered = screen.copy()
    checkered.fill(Color.GREY)

    for n, rect in enumerate(possible_rects(Screen.WIDTH, Screen.HEIGHT)):
        if n % 2 == 0:
            pygame.draw.rect(checkered, Color.LIGHT_GREY, rect)

    return checkered


if __name__ == "__main__":
    pygame.display.init()
    pg_screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
    background = checkered_surface(pg_screen)
    clock = pygame.time.Clock()
    s = Game.DEFAULT_RECT_SIZE
    u1 = SnakeUnit(place_after=Game.DEFAULT_RECT.move(s * 3, 0))
    u2 = SnakeUnit(place_after=u1.rect)
    u3 = SnakeUnit(place_after=u2.rect)
    snake = Snake(u1, u2, u3)
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
        pygame.display.update()
        frametime = clock.tick(Screen.FPS)

