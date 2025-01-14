import random

import pygame


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
EXIT_POS = (1820, 1010)
START_POS = (1820, 1010)
RESTART_POS = (1820, 1010)
TITOLO_POS = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
TABLE_X = 670
TABLE_Y = SCREEN_HEIGHT / 2
NUOVA_PARTITA = pygame.event.custom_type()
FINE_GIOCO = pygame.event.custom_type()
CONTINUA_GIOCO = pygame.event.custom_type()
END_TEXT_POS = (320, 320)
FASE_INIZIO = "F1"
FASE_GIOCO = "F2"


@singleton
class GameStatus:
    def __init__(self):
        self.resetGame()

    def resetGame(self):
        self.tableCard: list = []
        self.fasePartita: str = FASE_INIZIO

    def start_game(self):
        self.partita = True

    def start_game(self):
        self.partita = True
