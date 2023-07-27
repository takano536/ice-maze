import modules.maze
import modules.player

import pygame
import sys


class App:

    TILE_SIZE = 32

    PADDING = TILE_SIZE

    PLAYER_COLOR = (101, 154, 134)
    GOAL_COLOR = (244, 252, 237)
    ICE_COLOR = (182, 223, 163)
    BG_COLOR = (33, 65, 78)
    WALL_COLOR = BG_COLOR
    TEXT_COLOR = BG_COLOR

    FPS = 240

    PLAYER_INIT_SPEED = 0.125
    PLAYER_ACCELERATION = 0

    def __init__(self) -> None:
        self.__maze = modules.maze.Maze()
        self.__player = modules.player.Player(self.__maze.start(), self.PLAYER_INIT_SPEED, self.PLAYER_ACCELERATION)
        self.__maze_width = len(self.__maze.field()[0])
        self.__maze_height = len(self.__maze.field())
        pygame.init()
        pygame.display.set_caption('Visualizer')

        width = self.__maze_width * self.TILE_SIZE + self.PADDING
        height = self.__maze_height * self.TILE_SIZE + self.PADDING
        self.__screen = pygame.display.set_mode((width, height))

        self.__font = pygame.font.SysFont('Consolas', 14, bold=True)
        self.__clock = pygame.time.Clock()
        self.__answer_enabled = False

    def run(self):
        while (True):
            self.mainloop()

    def mainloop(self):
        self.__player.update()

        self.draw()
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_r:
                    self.__player.reset()

                if event.key == pygame.K_SPACE:
                    self.__answer_enabled = True

                self.__player.move(event.key, self.__maze.field())

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.__clock.tick(self.FPS)

    def draw(self):
        self.__screen.fill(self.BG_COLOR)

        # draw field
        for i in range(len(self.__maze.field())):
            for j in range(len(self.__maze.field()[i])):

                x = j * self.TILE_SIZE + self.PADDING / 2
                y = i * self.TILE_SIZE + self.PADDING / 2
                color = self.WALL_COLOR if self.__maze.field()[i][j] == '#' else self.ICE_COLOR
                size = (x, y, self.TILE_SIZE, self.TILE_SIZE)
                pygame.draw.rect(self.__screen, color, size)

                if self.__maze.field()[i][j] == 'G':
                    size = (x + self.PADDING / 4, y + self.PADDING / 4, self.TILE_SIZE / 2, self.TILE_SIZE / 2)
                    pygame.draw.rect(self.__screen, self.GOAL_COLOR, size)

                if not self.__answer_enabled or self.__maze.answer()[i][j] == -1:
                    continue

                source = self.__font.render(str(self.__maze.answer()[i][j]), True, self.TEXT_COLOR)
                dist = (x - self.PADDING * 0.75, y + self.PADDING * 0.25)
                self.__screen.blit(source, dist)

        # draw player
        player_coord = self.__player.coord()
        x = player_coord[0] * self.TILE_SIZE + self.PADDING / 2
        y = player_coord[1] * self.TILE_SIZE + self.PADDING / 2
        size = (x + self.PADDING * 0.25, y + self.PADDING * 0.25, self.TILE_SIZE * 0.5, self.TILE_SIZE * 0.5)
        pygame.draw.rect(self.__screen, self.PLAYER_COLOR, size)
