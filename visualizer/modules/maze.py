from pathlib import Path


class Maze:

    MAZE_FILEPATH = Path(__file__).parent.parent.parent / 'res' / 'maze.txt'
    ANSWER_FILEPATH = Path(__file__).parent.parent.parent / 'res' / 'answer.txt'

    def __init__(self) -> None:
        with open(self.MAZE_FILEPATH, 'r') as f:
            self.__field = [s.strip() for s in f.readlines()]
        for i in range(len(self.__field)):
            if 'S' in self.__field[i]:
                self.__start = (self.__field[i].index('S'), i)
            if 'G' in self.__field[i]:
                self.__goal = (self.__field[i].index('G'), i)
        self.__answer = list()
        with open(self.ANSWER_FILEPATH, 'r') as f:
            for i, s in enumerate(f.readlines()):
                nums = list()
                for j in range(int(len(s) / 3)):
                    curr = s[j * 3 - 3:j * 3].strip()
                    if curr.isdecimal():
                        nums.append(int(curr))
                    else:
                        nums.append(-1)
                self.__answer.append(nums)

    def field(self):
        return self.__field

    def start(self):
        return self.__start

    def goal(self):
        return self.__goal

    def answer(self):
        return self.__answer
