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
        self.__tile_size = tuple(config['tile_size'].values())

        # load field
        map_filepath = str(Path(config['map_filepath']).resolve())
        with open(map_filepath, 'r') as f:
            input = [s.strip() for s in f.readlines()]
        height, _ = map(int, input[0].split())
        field = [s.replace(' ', '') for s in input[1:height + 1]]

        # load ans
        ans_filepath = str(Path(config['answer_filepath']).resolve())
        with open(ans_filepath, 'r') as f:
            input = [s for s in f.readlines()]
        ans = list()
        for i, s in enumerate(input):
            if i >= height:
                break
            nums = list()
            for j in range(int(len(s) / 3)):
                curr = s[j * 3 - 3:j * 3].strip()
                if curr.isdecimal():
                    nums.append(int(curr))
                else:
                    nums.append(-1)
            ans.append(nums)

        # init surface & dirty rects
        screen_width = len(field[0]) * self.__tile_size[0]
        screen_height = len(field) * self.__tile_size[1]
        self.__surface = pygame.display.set_mode((screen_width, screen_height))
        self.__surface.fill(config['color']['bg'])
        self.__dirty_rects = list()

        # init field
        self.__field = modules.field.Field(field, ans, config['color']['text'], config['font'], config['font_size'], self.__tile_size, config['fps'], self.__surface)

        self.__clock = pygame.time.Clock()
        self.__delta_time = self.__clock.get_time()

        pygame.display.update()

    def run(self):
        while (True):
            self.__mainloop()

    def __mainloop(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.__field.update(self.__surface, self.__dirty_rects, self.__delta_time, event.key)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__quit()
            if event.type == pygame.QUIT:
                self.__quit()

        self.__field.update(self.__surface, self.__dirty_rects, self.__delta_time)

        pygame.display.update(self.__dirty_rects)
        self.__dirty_rects.clear()

        self.__delta_time = self.__clock.tick(self.__fps)
        self.__delta_time /= 1000

    def __quit(self):
        pygame.quit()
        sys.exit()
