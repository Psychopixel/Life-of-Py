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
        self.max_ticks = 100  # Number of ticks to display in the graphs
        self.plant_counts = [0]
        self.prey_counts = [0]
        self.predator_counts = [0]
        self.food_counts = [0]
        # Initialize world
        self.world = World(
            width=self.config.get_int("GRID_WIDTH", fallback=1000),
            height=self.config.get_int("GRID_HEIGHT", fallback=1000),
            config=self.config,
        )
        self.world.populate_randomly()
        self.plant_counts.append(self.world.num_plant())
        self.prey_counts.append(self.world.num_prey())
        self.predator_counts.append(self.world.num_predator())
        self.food_counts.append(self.world.num_food())
        self.partita = False
        self.fasePartita: str = self.config.get("FASE_INIZIO")

    def start_game(self):
        self.partita = True
        self.start_time = time.time()
        self.tick = 0

    def status(self):
        return self.partita
    
    def max_ticks(self):
        return self.max_ticks
    
    def tick(self):
        return self.tick
    
    def world(self):
        return self.world
    
    def elapsed_time(self):
        # Draw counters below the graphs
        return time.time() - self.start_time