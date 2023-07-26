from pathlib import Path


class Maze:

    MAZE_FILEPATH = Path(__file__).parent.parent.parent / 'res' / 'maze.txt'

    def __init__(self) -> None:
        with open(self.MAZE_FILEPATH, 'r') as f:
            self.__field = [s.strip() for s in f.readlines()]
        for i in range(len(self.__field)):
            if 'S' in self.__field[i]:
                self.__start = (self.__field[i].index('S'), i)
            if 'G' in self.__field[i]:
                self.__goal = (self.__field[i].index('G'), i)

    def field(self):
        return self.__field

    def start(self):
        return self.__start

    def goal(self):
        return self.__goal
