import pygame


class IceTile(pygame.sprite.Sprite):
    def __init__(self, coord):
        super().__init__()
        self.__image = pygame.image.load('./assets/ice-floor.png').convert()
        self.__rect = self.__image.get_rect()
        self.__rect.x = coord[0]
        self.__rect.y = coord[1]
