import modules.maze
import modules.player

import pygame
import sys


class App:

    MAZE_WIDTH = 12 + 2
    MAZE_HEIGHT = 12 + 2

    TILE_SIZE = 32

    PADDING = TILE_SIZE

    WALL_COLOR = (33, 33, 33)
    BG_COLOR = (66, 165, 245)
    PLAYER_COLOR = (205, 220, 57)

    FPS = 60

    PLAYER_INIT_SPEED = 0.2
    PLAYER_ACCELERATION = 0

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Visualizer')
        self.__screen_size = (
            self.MAZE_WIDTH * self.TILE_SIZE,
            self.MAZE_HEIGHT * self.TILE_SIZE
        )
        self.__screen = pygame.display.set_mode(self.__screen_size)
        self.__clock = pygame.time.Clock()
        self.__maze = modules.maze.Maze()
        self.__player = modules.player.Player(
            self.__maze.start(),
            self.PLAYER_INIT_SPEED,
            self.PLAYER_ACCELERATION
        )

    def run(self):
        while (True):
            self.mainloop()

    def mainloop(self):
        self.__player.update()

        self.draw()
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                self.__player.move(event.key, self.__maze.field())

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.__clock.tick(self.FPS)

    def draw(self):
        self.__screen.fill(self.BG_COLOR)

        # draw walls
        for i in range(len(self.__maze.field())):
            for j in range(len(self.__maze.field()[i])):
                if self.__maze.field()[i][j] != '#':
                    continue
                x = j * self.TILE_SIZE
                y = i * self.TILE_SIZE
                pygame.draw.rect(
                    self.__screen,
                    self.WALL_COLOR,
                    (x, y, self.TILE_SIZE, self.TILE_SIZE)
                )

        # draw player
        player_coord = self.__player.coord()
        pygame.draw.rect(
            self.__screen,
            self.PLAYER_COLOR,
            (
                player_coord[0] * self.TILE_SIZE,
                player_coord[1] * self.TILE_SIZE,
                self.TILE_SIZE,
                self.TILE_SIZE
            )
        )
