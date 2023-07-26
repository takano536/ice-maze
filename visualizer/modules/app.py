import modules.maze
import modules.player

import pygame
import sys


class App:

    TILE_SIZE = 32

    PADDING = TILE_SIZE

    BG_COLOR = (33, 33, 33)
    WALL_COLOR = BG_COLOR
    ICE_COLOR = (66, 165, 245)
    PLAYER_COLOR = (205, 220, 57)
    GOAL_COLOR = (39, 99, 147)

    FPS = 60

    PLAYER_INIT_SPEED = 0.4
    PLAYER_ACCELERATION = 0

    def __init__(self) -> None:
        self.__maze = modules.maze.Maze()
        self.__player = modules.player.Player(
            self.__maze.start(),
            self.PLAYER_INIT_SPEED,
            self.PLAYER_ACCELERATION
        )
        self.__maze_width = len(self.__maze.field()[0])
        self.__maze_height = len(self.__maze.field())
        pygame.init()
        pygame.display.set_caption('Visualizer')
        screen_size = (
            self.__maze_width * self.TILE_SIZE + self.PADDING,
            self.__maze_height * self.TILE_SIZE + self.PADDING
        )
        self.__screen = pygame.display.set_mode(screen_size)
        self.__clock = pygame.time.Clock()

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

        # draw field
        for i in range(len(self.__maze.field())):
            for j in range(len(self.__maze.field()[i])):
                x = j * self.TILE_SIZE + self.PADDING / 2
                y = i * self.TILE_SIZE + self.PADDING / 2
                color = self.GOAL_COLOR if self.__maze.field()[i][j] == 'G' else self.ICE_COLOR
                color = self.WALL_COLOR if self.__maze.field()[i][j] == '#' else color
                pygame.draw.rect(
                    self.__screen,
                    color,
                    (x, y, self.TILE_SIZE, self.TILE_SIZE)
                )

        # draw player
        player_coord = self.__player.coord()
        pygame.draw.rect(
            self.__screen,
            self.PLAYER_COLOR,
            (
                player_coord[0] * self.TILE_SIZE + self.PADDING / 2,
                player_coord[1] * self.TILE_SIZE + self.PADDING / 2,
                self.TILE_SIZE,
                self.TILE_SIZE
            )
        )
