from sys import exit

import pygame

import gameStatus as gs
from assetManager import AssetManager
from gameStatus import GameStatus
from gui import Gui


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((gs.SCREEN_WIDTH, gs.SCREEN_HEIGHT))
        pygame.display.set_caption("Life of Py")
        self.assetManager = AssetManager()
        self.assetManager.load_all_images()
        pygame_icon = self.assetManager.load_image("preda.png")
        pygame.display.set_icon(pygame_icon)
        self.clock = pygame.time.Clock()
        self.gameStatus = GameStatus()
        self.gui = Gui(self.screen)
        self.gui.AddSubscribersForExitEvent(self.close_game)
        self.gui.AddSubscriberForRestartEvent(self.restart)
        self.gui.AddSubscriberForStartEvent(self.start_game)

    def run(self):
        while True:
            events = pygame.event.get()
            self.manage_input(events)
            self.clock.tick(100)
            self.gui.renderScreen(events, self.gameStatus.tableCard)

    def manage_input(self, events: list):
        for event in events:
            if event.type == pygame.QUIT:
                self.handle_quit_event()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_event()

    def start_game(self):
        print("START")
        self.gameStatus.resetGame()
        self.gameStatus.start_game()
        self.gameStatus.fasePartita = gs.FASE_GIOCO
        pass

    def close_game(self):
        pygame.quit()
        exit()

    def handle_quit_event(self):
        self.close_game()

    def handle_new_game_event(self):
        self.new_game()

    def handle_mouse_event(self):
        pass

    def new_game(self):
        pass

    def reset_game_state(self):
        pass

    def continue_game(self):
        pass

    def restart(self):
        self.gameStatus.resetGame()
        self.gameStatus.start_game()

    def close_game(self):
        pygame.quit()
        exit()
