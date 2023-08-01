import modules.player

import pygame


class Field:

    def __init__(self, field: list, colors: dict, tile_size: tuple, fps: int, surface: pygame.Surface) -> None:
        self.__field = field
        for i, s in enumerate(field):
            if 'S' in s:
                self.__start_coord = (s.index('S'), i)
            if 'G' in s:
                self.__goal_coord = (s.index('G'), i)
        self.__colors = colors

        for i, s in enumerate(field):
            for j, c in enumerate(s):
                coord = (j * tile_size[1], i * tile_size[0])
                pygame.draw.rect(surface, colors[c], pygame.Rect(coord, tile_size))

        size = [tile_size[0] / 2, tile_size[1] / 2]
        default_speed = max(len(field[0]), len(field)) / fps
        self.__player = modules.player.Player(self.__start_coord, size, tile_size, default_speed, colors['player'], surface)

    def update(self, surface: pygame.Surface, dirty_rects: list, key: int = None) -> None:
        if key == pygame.K_r:
            self.__player.reset(surface, dirty_rects, self.__colors['.'])
        elif key is not None:
            self.__player.move(key, self.__field)
        else:
            self.__player.update(surface, dirty_rects, self.__colors['.'])
