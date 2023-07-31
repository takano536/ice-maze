import pygame


class Player(pygame.sprite.Sprite):

    SPEED = 1

    def __init__(self, coord: tuple, size: tuple, tile_size: tuple, color: tuple) -> None:
        super().__init__()
        self.__start_coord = list(coord)
        self.__curr_coord = list(coord)
        self.__next_coord = list(coord)
        self.__size = size
        self.__padding = [tile_size[0] - self.__size[0], tile_size[1] - self.__size[1]]
        self.__color = color
        self.__is_moving = False
        self.__direction = [0, 0]

    def move(self, key: int, field: list) -> None:
        if self.__is_moving:
            return

        self.__direction = [0, 0]
        if key == pygame.K_w or key == pygame.K_UP:
            self.__direction[1] = -1
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.__direction[1] = 1
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.__direction[0] = -1
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.__direction[0] = 1

        if self.__direction[0] == 0 and self.__direction[1] == 0:
            return

        self.__is_moving = True
        while field[self.__next_coord[1] + self.__direction[1]][self.__next_coord[0] + self.__direction[0]] != '#':
            self.__next_coord[0] += self.__direction[0]
            self.__next_coord[1] += self.__direction[1]

    def update(self, tile_size: tuple, dirty_rects: list, surface: pygame.Surface, background_color: tuple) -> None:
        if not self.__is_moving:
            return

        # draw background
        coord = (self.__curr_coord[0] + self.__padding[0] / 2, self.__curr_coord[1] + self.__padding[1] / 2)
        curr_rect = pygame.Rect(coord, self.__size)
        pygame.draw.rect(surface, background_color, curr_rect)
        dirty_rects.append(curr_rect)

        # update player coord
        self.__curr_coord[0] += self.__direction[0] * self.SPEED
        self.__curr_coord[1] += self.__direction[1] * self.SPEED
        diff = [
            (self.__next_coord[0] - self.__curr_coord[0]) * self.__direction[0],
            (self.__next_coord[1] - self.__curr_coord[1]) * self.__direction[1]
        ]
        if diff[0] < 0 or diff[1] < 0:
            self.__curr_coord = self.__next_coord.copy()
            self.__is_moving = False
            self.__direction = [0, 0]

        # draw player
        coord = (self.__curr_coord[0] + self.__padding[0] / 2, self.__curr_coord[1] + self.__padding[1] / 2)
        next_rect = pygame.Rect(coord, self.__size)
        pygame.draw.rect(surface, self.__color, next_rect)
        dirty_rects.append(next_rect)

    def reset(self) -> None:
        self.__curr_coord = self.__start_coord.copy()
        self.__next_coord = self.__start_coord.copy()
        self.__is_moving = False
        self.__direction = [0, 0]
