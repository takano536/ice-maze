import modules.player


class Map:

    def __init__(self, map: list, colors: dict, tile_size: tuple) -> None:
        self.__map = map
        self.__start_coord = [zip(line.index('S'), i) for i, line in enumerate(map) if 'S' in line][0]
        self.__goal_coord = [zip(line.index('G'), i) for i, line in enumerate(map) if 'G' in line][0]

        player_size = [tile_size[0] / 2, tile_size[1] / 2]
        self.__player = modules.player.Player(self.__start_coord, player_size, tile_size, colors['player'])
