import modules.field

import json
from pathlib import Path
import pygame
import sys


class App:

    CONFIG_FILEPATH = str(Path(__file__).resolve().parents[1] / 'config' / 'config.json')

    def __init__(self) -> None:

        # init pygame
        pygame.init()
        pygame.display.set_caption('Visualizer')

        # load config
        with open(self.CONFIG_FILEPATH, 'r') as f:
            config = json.load(f)
        self.__fps = config['fps']
        tile_size = tuple(config['tile_size'].values())
        self.__font = pygame.font.SysFont(config['font'], config['font_size'], bold=True)

        # load field
        map_filepath = str(Path(config['map_filepath']).resolve())
        with open(map_filepath, 'r') as f:
            input = [s.strip() for s in f.readlines()]
        height, _ = map(int, input[0].split())
        field = [s.replace(' ', '') for s in input[1:height + 1]]

        # init surface & dirty rects
        screen_width = len(field[0]) * tile_size[0]
        screen_height = len(field) * tile_size[1] - 2 * tile_size[1] / 3
        self.__surface = pygame.display.set_mode((screen_width, screen_height))
        self.__surface.fill(config['color']['bg'])
        self.__dirty_rects = list()

        # init field
        self.__field = modules.field.Field(field, config['color'], tile_size, config['fps'], self.__surface)

        self.__clock = pygame.time.Clock()

        pygame.display.update()

    def run(self):
        while (True):
            self.__mainloop()

    def __mainloop(self):
        self.__field.update(self.__surface, self.__dirty_rects)

        pygame.display.update(self.__dirty_rects)
        self.__dirty_rects.clear()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.__field.update(self.__surface, self.__dirty_rects, event.key)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__quit()
            if event.type == pygame.QUIT:
                self.__quit()

        self.__clock.tick(self.__fps)

    def __quit(self):
        pygame.quit()
        sys.exit()
