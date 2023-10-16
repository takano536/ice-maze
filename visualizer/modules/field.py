import modules.player

import pygame
import random
from pathlib import Path


class Field:

    ASSETS_DIRPATH = str(Path(__file__).resolve().parents[1] / 'assets')
    ROCK_IMG_FILEPATH = str(Path(ASSETS_DIRPATH) / 'rock.png')
    STONE_IMG_FILEPATH = str(Path(ASSETS_DIRPATH) / 'stone.png')
    FLOOR_IMG_FILEPATH = str(Path(ASSETS_DIRPATH) / 'ice-floor.png')
    GOAL_IMG_FILEPATH = str(Path(ASSETS_DIRPATH) / 'goal.png')
    WALL_IMG_FILEPATH = str(Path(ASSETS_DIRPATH) / 'wall-#.png')

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
        self.__floor_img = pygame.image.load(self.FLOOR_IMG_FILEPATH).convert()
        self.__stone_imgs = list()
        self.__goal_img = pygame.image.load(self.GOAL_IMG_FILEPATH).convert()
        self.__goal_img.set_colorkey(self.__goal_img.get_at((0, 0)))
        stone_img = pygame.image.load(self.STONE_IMG_FILEPATH).convert()
        rock_img = pygame.image.load(self.ROCK_IMG_FILEPATH).convert()
        stone_img.set_colorkey(stone_img.get_at((0, 0)))
        rock_img.set_colorkey(rock_img.get_at((0, 0)))
        self.__stone_imgs.append(stone_img)
        self.__stone_imgs.append(rock_img)
        self.__wall_imgs = list()
        for i in range(8):
            img = pygame.image.load(self.WALL_IMG_FILEPATH.replace('#', str(i)))
            self.__wall_imgs.append(img)

        for i, s in enumerate(field):
            for j, c in enumerate(s):
                if i == 0 or i == len(field) - 1 or j == 0 or j == len(field[0]) - 1:
                    continue
                coord = (j * tile_size[1], i * tile_size[0])
                surface.blit(self.__floor_img, coord)
                if c == '#':
                    surface.blit(random.choice(self.__stone_imgs), coord)
                if c == 'G':
                    surface.blit(self.__goal_img, coord)

        surface.blit(self.__wall_imgs[0], (0, 0))
        surface.blit(self.__wall_imgs[2], ((len(field[0]) - 1) * tile_size[1], 0))
        surface.blit(self.__wall_imgs[4], ((len(field[0]) - 1) * tile_size[1], (len(field) - 1) * tile_size[0]))
        surface.blit(self.__wall_imgs[6], (0, (len(field) - 1) * tile_size[0]))

        for j, s in enumerate(field[0]):
            if j == 0 or j == len(field[0]) - 1:
                continue
            coord = (j * tile_size[1], 0)
            surface.blit(self.__wall_imgs[1], coord)
        for i, s in enumerate(field[0]):
            if i == 0 or i == len(field) - 1:
                continue
            coord = ((len(field[0]) - 1) * tile_size[1], i * tile_size[0])
            surface.blit(self.__wall_imgs[3], coord)
        for j, s in enumerate(field[0]):
            if j == 0 or j == len(field[0]) - 1:
                continue
            coord = (j * tile_size[1], (len(field) - 1) * tile_size[0])
            surface.blit(self.__wall_imgs[5], coord)
        for i, s in enumerate(field[0]):
            if i == 0 or i == len(field) - 1:
                continue
            coord = (0, i * tile_size[0])
            surface.blit(self.__wall_imgs[7], coord)

        default_speed = max(tile_size) / 3
        self.__player = modules.player.Player(self.__start_coord, tile_size, default_speed, surface)

    def update(self, surface: pygame.Surface, dirty_rects: list, delta_time: float, key: int = None) -> None:
        if self.__ans_enabled:
            self.__draw_ans(surface, dirty_rects)
        if key == pygame.K_r:
            self.__player.reset(surface, dirty_rects, self.__floor_img)
        if key == pygame.K_SPACE:
            self.__ans_enabled = True
        if key is not None:
            self.__player.move(key, self.__field)
        else:
            self.__player.update(surface, dirty_rects, delta_time, self.__floor_img)

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
