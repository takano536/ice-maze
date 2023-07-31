import modules.painter
import modules.map

import json
from pathlib import Path
import pygame
import sys


class App:

    CONFIG_FILEPATH = str(Path('__file__').resolve().parent / 'config' / 'config.json')

    def __init__(self) -> None:

        # init pygame
        pygame.init()
        pygame.display.set_caption('Visualizer')

        # load config
        with open(self.CONFIG_FILEPATH, 'r') as f:
            config = json.load(f)
        self.__fps = config['fps']
        tile_size = tuple(config['tile_size'])
        padding_size = tuple(config['padding_size'])
        self.__font = pygame.font.SysFont(config['font'], config['font_size'], bold=True)

        # load map
        with open(config['map_filepath'], 'r') as f:
            input = [s.strip() for s in f.readlines()]
        height, _ = map(int, input[0].split())
        map = [s.replace(' ', '') for s in input[1:height + 1]]
        self.__map = modules.map.Map(map, config['color'])

        # init surface & dirty rects
        screen_width = len(map[0]) * padding_size[0] + tile_size[0]
        screen_height = len(map) * padding_size[1] + tile_size[1]
        self.__surface = pygame.display.set_mode((screen_width, screen_height))
        self.__dirty_rects = list()

        self.__clock = pygame.time.Clock()
