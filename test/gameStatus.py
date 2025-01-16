import random
import os
import time
import pygame
from world import World
from config import EnvConfig


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class GameStatus:
    
    def __init__(self):
        self.config = EnvConfig("config/.env")
        if not self.config.load():
            raise ValueError("Failed to load .env file. Check the file path and contents.")
        self.resetGame()
    
    def resetGame(self):
        # Data for graphs
        plant_counts = []
        prey_counts = []
        predator_counts = []
        food_counts = []
        max_ticks = 100  # Number of ticks to display in the graphs

        # Initialize world
        world = World(
            width=self.config.get_int("GRID_WIDTH", fallback=1000),
            height=self.config.get_int("GRID_HEIGHT", fallback=1000),
            config=self.config,
        )
        world.populate_randomly()
        self.fasePartita: str = self.config.get("FASE_INIZIO")

    def start_game(self):
        self.partita = True
        start_time = time.time()
        tick = 0
