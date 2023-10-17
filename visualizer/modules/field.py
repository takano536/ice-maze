import modules.player

import pygame
from pathlib import Path


class Field:

    ASSETS_DIRPATH = str(Path(__file__).resolve().parents[1] / 'assets')
    IMG_FILEPATH = str(Path(ASSETS_DIRPATH) / 'ice_path_tileset_by_piacarrot_d6hslib.png')

    def __init__(self, field: list, ans: list, ans_color: dict, font: str, font_size: int, tile_size: tuple, fps: int, surface: pygame.Surface) -> None:
        self.__field = field
        for i, s in enumerate(field):
            if 'S' in s:
                self.__start_coord = (s.index('S'), i)
            if 'G' in s:
                self.__goal_coord = (s.index('G'), i)
        self.__ans = ans
        self.__ans_enabled = False
        self.__should_write_answer = True
        self.__font_color = ans_color
        self.__font = pygame.font.SysFont(font, font_size, bold=True)
        self.__tile_size = tile_size

        tileset = pygame.image.load(self.IMG_FILEPATH).convert()
        self.__floor_img = tileset.subsurface([0, 0, 32, 32])
        self.__goal_img = tileset.subsurface([64, 0, 32, 32])
        self.__stone_img = tileset.subsurface([64, 64, 32, 32])

        for i, s in enumerate(field):
            for j, c in enumerate(s):
                coord = (j * tile_size[1], i * tile_size[0])
                surface.blit(self.__floor_img, coord)
                if c == '#':
                    surface.blit(self.__stone_img, coord)
                if c == 'G':
                    surface.blit(self.__goal_img, coord)

        self.__player = modules.player.Player(self.__start_coord, tile_size, surface)

    def update(self, surface: pygame.Surface, dirty_rects: list, delta_time: float, key: int = None) -> None:
        if self.__ans_enabled:
            self.__draw_ans(surface, dirty_rects)
        if key == pygame.K_SPACE:
            self.__ans_enabled = True
        if key == pygame.K_r:
            self.__draw_mask(surface, dirty_rects)
            self.__player.reset(surface, dirty_rects)
            
        if key is not None:
            self.__player.move(key, self.__field)
            
        if self.__player.is_moving():
            self.__draw_mask(surface, dirty_rects)
        self.__player.update(surface, dirty_rects, delta_time)

    def __draw_ans(self, surface: pygame.Surface, dirty_rects: list):
        if not self.__should_write_answer:
            return
        for i, l in enumerate(self.__ans):
            for j, num in enumerate(l):
                if num == -1:
                    continue
                coord = ((j - 1) * self.__tile_size[1] + self.__tile_size[1] / 3, i * self.__tile_size[0] + self.__tile_size[0] / 3)
                text = self.__font.render(str(num), True, self.__font_color)
                surface.blit(text, coord)
                dirty_rects.append(pygame.Rect(coord, self.__tile_size))
        self.__should_write_answer = False

    def __draw_mask(self, surface: pygame.Surface, dirty_rects: list):
        def coord2idx(coord: tuple) -> tuple:
            return (coord[1] // self.__tile_size[1], coord[0] // self.__tile_size[0])

        mask_rects = self.__player.get_mask_rects()
        for rect in mask_rects:
            i, j = coord2idx(pygame.Rect(rect).topleft)
            mask_img = self.__stone_img if self.__field[i][j] == '#' else self.__goal_img if self.__field[i][j] == 'G' else self.__floor_img
            surface.blit(mask_img, rect)
            dirty_rects.append(rect)
