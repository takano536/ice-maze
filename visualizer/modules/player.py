import enum
import pygame
from pathlib import Path


class Player(pygame.sprite.Sprite):

    ASSETS_DIRPATH = str(Path(__file__).resolve().parents[1] / 'assets')
    IMG_FILEPATH = str(Path(ASSETS_DIRPATH) / 'young_boy_ow___bw_style_by_kleinstudio_d5jjgkf.png')

    class Direction(enum.Enum):
        DOWN = 0
        LEFT = 1
        RIGHT = 2
        UP = 3

    DIRECTION = {
        (0, 1): Direction.DOWN,
        (-1, 0): Direction.LEFT,
        (0, -1): Direction.UP,
        (1, 0): Direction.RIGHT
    }

    MOVING_ANIMATION_TIME = 150

    def __init__(self, coord: tuple, tile_size: tuple, speed_offset: float, surface: pygame.Surface) -> None:
        super().__init__()
        self.__start_coord = list(coord)
        self.__curr_coord = list(coord)
        self.__next_coord = list(coord)
        self.__tile_size = tile_size
        self.__speed = tile_size[0] * 0.25 * speed_offset
        self.__direction = [0, 1]
        self.__is_moving = False
        self.__size = [32, 64]

        img = pygame.image.load(self.IMG_FILEPATH).convert()
        img.set_colorkey(img.get_at((0, 0)))

        self.__standing_imgs = [img.subsurface([16, i * 64, 32, 64]) for i in range(4)]
        self.__moving_imgs = [img.subsurface([3 * 64 + 16, i * 64, 32, 64]) for i in range(4)]
        self.__moving_img_timer = 0

        surface.blit(self.__standing_imgs[self.Direction.DOWN.value], self.__get_draw_coord())

    def move(self, key: int, field: list) -> None:
        if self.__is_moving:
            return

        if key == pygame.K_w or key == pygame.K_UP:
            self.__direction = [0, -1]
            self.__is_moving = True
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.__direction = [0, 1]
            self.__is_moving = True
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.__direction = [-1, 0]
            self.__is_moving = True
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.__direction = [1, 0]
            self.__is_moving = True

        if not self.__is_moving:
            return

        self.__moving_img_timer = pygame.time.get_ticks()

        while field[self.__next_coord[1] + self.__direction[1]][self.__next_coord[0] + self.__direction[0]] not in ['#', 'G']:
            self.__next_coord[0] += self.__direction[0]
            self.__next_coord[1] += self.__direction[1]

    def update(self, surface: pygame.Surface, dirty_rects: list, delta_time: float) -> None:
        if not self.__is_moving:
            return

        # update player coord
        moving_time = pygame.time.get_ticks() - self.__moving_img_timer
        weight = min(moving_time, self.MOVING_ANIMATION_TIME) / self.MOVING_ANIMATION_TIME
        self.__curr_coord[0] += self.__direction[0] * self.__speed * weight * delta_time
        self.__curr_coord[1] += self.__direction[1] * self.__speed * weight * delta_time
        diff = [
            (self.__next_coord[0] - self.__curr_coord[0]) * self.__direction[0],
            (self.__next_coord[1] - self.__curr_coord[1]) * self.__direction[1]
        ]
        if diff[0] < 0 or diff[1] < 0:
            self.__curr_coord = self.__next_coord.copy()
            self.__is_moving = False

        # draw player
        next_rect = pygame.Rect(self.__get_draw_coord(), self.__size)

        should_use_standing_img = pygame.time.get_ticks() - self.__moving_img_timer > self.MOVING_ANIMATION_TIME
        should_use_standing_img = should_use_standing_img or not self.__is_moving
        using_imgs = self.__standing_imgs if should_use_standing_img else self.__moving_imgs
        using_img = using_imgs[self.DIRECTION[tuple(self.__direction)].value]
        surface.blit(using_img, self.__get_draw_coord())

        dirty_rects.append(next_rect)

    def reset(self, surface: pygame.Surface, dirty_rects: list) -> None:
        self.__curr_coord = self.__start_coord.copy()
        self.__next_coord = self.__start_coord.copy()
        self.__direction = [0, 1]
        self.__is_moving = False

        # draw player
        next_rect = pygame.Rect(self.__get_draw_coord(), self.__size)
        surface.blit(self.__standing_imgs[self.Direction.DOWN.value], self.__get_draw_coord())
        dirty_rects.append(next_rect)

    def __get_draw_coord(self) -> tuple:
        x = self.__curr_coord[0] * self.__tile_size[0]
        y = (self.__curr_coord[1] - 1) * self.__tile_size[1]
        return (x, y)

    def get_mask_rects(self):
        def ceil(x, mod):
            return int(-(-x // mod) * mod)

        def floor(x, mod):
            return int(x // mod * mod)

        rects = list()
        topleft_draw_coord = self.__get_draw_coord()
        bottomright_draw_coord = (topleft_draw_coord[0] + self.__size[0], topleft_draw_coord[1] + self.__size[1])
        for i in range(floor(topleft_draw_coord[1], self.__tile_size[1]), ceil(bottomright_draw_coord[1], self.__tile_size[1]), self.__tile_size[1]):
            for j in range(floor(topleft_draw_coord[0], self.__tile_size[0]), ceil(bottomright_draw_coord[0], self.__tile_size[0]), self.__tile_size[0]):
                rects.append(pygame.Rect((j, i), self.__tile_size))

        return rects

    def is_moving(self):
        return self.__is_moving
