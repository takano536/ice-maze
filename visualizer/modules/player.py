import pygame


class Player:
    def __init__(self, coord: tuple, init_speed: float, acceleration: float) -> None:
        self.__curr_coord = list(coord)
        self.__next_coord = list(coord)
        self.__is_moving = False
        self.__direction = [0, 0]
        self.__init_speed = init_speed
        self.__acceleration = acceleration

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

    def update(self) -> None:
        if not self.__is_moving:
            return

        next_frame_coord = self.__curr_coord.copy()
        next_frame_coord[0] += self.__direction[0] * self.__init_speed
        next_frame_coord[1] += self.__direction[1] * self.__init_speed
        diff = [
            (self.__next_coord[0] - next_frame_coord[0]) * self.__direction[0],
            (self.__next_coord[1] - next_frame_coord[1]) * self.__direction[1]
        ]

        if diff[0] < 0 or diff[1] < 0:
            self.__curr_coord = self.__next_coord.copy()
            self.__is_moving = False
            self.__direction = [0, 0]
            return

        self.__curr_coord = next_frame_coord

    def coord(self) -> tuple:
        return tuple(self.__curr_coord)
