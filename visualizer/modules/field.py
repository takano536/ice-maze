import modules.player

import pygame
import random


class Field:

    ROCK_IMG_FILEPATH = 'visualizer/assets/rock.png'
    STONE_IMG_FILEPATH = 'visualizer/assets/stone.png'
    FLOOR_IMG_FILEPATH = 'visualizer/assets/ice-floor.png'
    GOAL_IMG_FILEPATH = 'visualizer/assets/goal.png'
    WALL_IMG_FILEPATH = 'visualizer/assets/wall-#.png'

    def __init__(self, field: list, colors: dict, tile_size: tuple, fps: int, surface: pygame.Surface) -> None:
        self.__field = field
        for i, s in enumerate(field):
            if 'S' in s:
                self.__start_coord = (s.index('S'), i)
            if 'G' in s:
                self.__goal_coord = (s.index('G'), i)
        self.__colors = colors
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

        default_speed = max(len(field[0]), len(field)) / fps
        self.__player = modules.player.Player(self.__start_coord, tile_size, default_speed, surface)

    def update(self, surface: pygame.Surface, dirty_rects: list, key: int = None) -> None:
        if key == pygame.K_r:
            self.__player.reset(surface, dirty_rects, self.__floor_img)
        elif key is not None:
            self.__player.move(key, self.__field)
        else:
            self.__player.update(surface, dirty_rects, self.__floor_img)
