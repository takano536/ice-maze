import enum
import pygame


class Player(pygame.sprite.Sprite):

    IMG_FILEPATH = 'visualizer/assets/player.png'
    SPEED = 0.75

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

    def __init__(self, coord: tuple, size: tuple, speed: float, surface: pygame.Surface) -> None:
        super().__init__()
        self.__start_coord = list(coord)
        self.__curr_coord = list(coord)
        self.__next_coord = list(coord)
        self.__speed = speed * self.SPEED
        self.__direction = [0, 1]
        self.__is_moving = False
        self.__size = size
        self.__img = pygame.image.load(self.IMG_FILEPATH).convert()
        self.__img.set_colorkey(self.__img.get_at((0, 0)))
        surface.blit(self.__img, self.__draw_coord(), area=self.__draw_rect())

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

        while field[self.__next_coord[1] + self.__direction[1]][self.__next_coord[0] + self.__direction[0]] not in ['#', 'G']:
            self.__next_coord[0] += self.__direction[0]
            self.__next_coord[1] += self.__direction[1]

    def update(self, surface: pygame.Surface, dirty_rects: list, background_img: pygame.Surface) -> None:
        if not self.__is_moving:
            return

        # draw background
        for rect in self.__mask_rects():
            surface.blit(background_img, rect)
            dirty_rects.append(rect)

        # update player coord
        self.__curr_coord[0] += self.__direction[0] * self.__speed
        self.__curr_coord[1] += self.__direction[1] * self.__speed
        diff = [
            (self.__next_coord[0] - self.__curr_coord[0]) * self.__direction[0],
            (self.__next_coord[1] - self.__curr_coord[1]) * self.__direction[1]
        ]
        if diff[0] < 0 or diff[1] < 0:
            self.__curr_coord = self.__next_coord.copy()
            self.__is_moving = False

        # draw player
        next_rect = pygame.Rect(self.__draw_coord(), self.__size)
        surface.blit(self.__img, self.__draw_coord(), area=self.__draw_rect())
        dirty_rects.append(next_rect)

    def reset(self, surface: pygame.Surface, dirty_rects: list, background_img: tuple) -> None:
        # draw background
        for rect in self.__mask_rects():
            surface.blit(background_img, rect)
            dirty_rects.append(rect)

        self.__curr_coord = self.__start_coord.copy()
        self.__next_coord = self.__start_coord.copy()
        self.__direction = [0, 1]
        self.__is_moving = False

        # draw player
        next_rect = pygame.Rect(self.__draw_coord(), self.__size)
        surface.blit(self.__img, self.__draw_coord(), area=self.__draw_rect())
        dirty_rects.append(next_rect)

    def __draw_coord(self) -> tuple:
        x = self.__curr_coord[0] * self.__size[0]
        y = self.__curr_coord[1] * self.__size[1]
        return (x, y)

    def __draw_rect(self):
        return pygame.Rect(self.__is_moving * self.__size[0], self.DIRECTION[tuple(self.__direction)].value * self.__size[1], self.__size[0], self.__size[1])

    def __mask_rects(self):

        def ceil(x, mod):
            return int(-(-x // mod) * mod)

        def floor(x, mod):
            return int(x // mod * mod)

        draw_coord = self.__draw_coord()
        top_left = (floor(draw_coord[0], self.__size[0]), floor(draw_coord[1], self.__size[1]))
        bottom_right = (ceil(draw_coord[0] + self.__size[0], self.__size[0]), ceil(draw_coord[1] + self.__size[1], self.__size[1]))
        rects = [pygame.Rect(x, y, self.__size[0], self.__size[1]) for x in range(top_left[0], bottom_right[0], self.__size[0]) for y in range(top_left[1], bottom_right[1], self.__size[1])]
        return rects
