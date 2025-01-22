from sys import exit
import pygame
from src.config import EnvConfig  # Import from config.py
from src.assetManager import AssetManager
from src.gameStatus import GameStatus
from src.gui import Gui
import os
import ctypes


class Game:
    def __init__(self):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Disable scaling
        pygame.init()
        if not pygame.display.get_init():
            pygame.display.init()
        # Load environment variables
        self.config = EnvConfig("config/.env")
        if not self.config.load():
            raise ValueError("Failed to load .env file. Check the file path and contents.")
        pygame.display.set_mode((self.config.get_int("SCREEN_WIDTH"), self.config.get_int("SCREEN_HEIGHT")), pygame.SHOWN)  # Use pygame.SHOWN for a regular window
        pygame.display.set_caption("Life of Py")
        self.assetManager = AssetManager()
        self.assetManager.load_all_images()
        pygame_icon = self.assetManager.load_image("preda.png")
        pygame.display.set_icon(pygame_icon)
        
        self.clock = pygame.time.Clock()
        self.gameStatus = GameStatus()
        self.gui = Gui()
        self.gui.AddSubscribersForExitEvent(self.close_game)
        self.gui.AddSubscriberForRestartEvent(self.restart)
        self.gui.AddSubscriberForStartEvent(self.start_game)

    def run(self):
        while True:
            #print("game: running")
            events = pygame.event.get()
            self.manage_input(events)
            self.clock.tick(100)
            if self.gameStatus.status:
                self.gameStatus.step_tick()
            self.gui.renderScreen(events)

    def manage_input(self, events: list):
        for event in events:
            if event.type == pygame.QUIT:
                self.handle_quit_event()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_event()

    def start_game(self):
        print("game: start_game")
        self.gameStatus.resetGame()
        self.gameStatus.fasePartita = self.config.get("FASE_GIOCO")
        self.gameStatus.start_game()

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
