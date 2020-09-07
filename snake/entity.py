import sys
from typing import List

import pygame
from pygame import gfxdraw
from pygame.constants import SRCALPHA

from snake.constants import Game, Color, Direction, Screen
from snake.utils import random_pos_rect


class SnakeUnit(pygame.sprite.Sprite):
    """
    Represents a single block of the snake on the screen
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # The RenderPlain group has a draw method that will use the rect and image attributes
        self.rect = Game.DEFAULT_RECT.copy()
        self.image = pygame.Surface(
            (self.rect.w, self.rect.h), flags=SRCALPHA
        ).convert_alpha()
        self.image.fill(Color.GREEN)
        pygame.draw.rect(self.image, SRCALPHA, self.rect, 1)


class Snake(pygame.sprite.RenderPlain):
    """
    Group of sprites(snake units) that compose the full snake
    """

    def __init__(self, *snake_units):
        super().__init__(*snake_units)
        self.dead = False
        self.direction = Direction.E
        self.new_direction = self.direction
        self.frametime_counter = 0
        self.frametime_for_step = Game.FRAMETIME_WAITED
        self.shortcuts = {
            pygame.K_UP: Direction.N,
            pygame.K_DOWN: Direction.S,
            pygame.K_RIGHT: Direction.E,
            pygame.K_LEFT: Direction.W,
        }
        self.add([SnakeUnit() for n in range(Game.NUM_UNITS_RESPAWN)])

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

            # Kill snake if it is out of screen
            head: SnakeUnit = self.sprites().pop()
            if (
                head.rect.x < 0
                or head.rect.x > Screen.WIDTH - head.rect.w
                or head.rect.y < 0
                or head.rect.y > Screen.HEIGHT - head.rect.h
            ):
                self.dead = True

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
        self.image = pygame.Surface(
            (self.rect.w, self.rect.h), flags=SRCALPHA
        ).convert_alpha()
        x, y = int(self.rect.w / 2) - 1, int(self.rect.h / 2) - 1
        radius = int(Game.DEFAULT_RECT_SIZE / 2) - 4
        gfxdraw.aacircle(self.image, x, y, radius, Color.RED)
        gfxdraw.filled_circle(self.image, x, y, radius, Color.RED)
