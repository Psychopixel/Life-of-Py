import random
from typing import Optional, List
import pygame
from src.entities import Entity, Plant, Prey, Predator, Food
from src.config import EnvConfig
from src.neural_net import NeuralNet
from src.event import Event

class World(pygame.Surface):
    """
    Manages a 2D grid of entities and provides methods for adding,
    removing, and updating them. Inherits from pygame.Surface.
    """

    def __init__(self, width: int, height: int, config: Optional[EnvConfig] = None):
        """
        :param width: number of columns in the grid
        :param height: number of rows in the grid
        :param config: optional EnvConfig for loading environment-based parameters
        """
        super().__init__((width, height))  # Initialize the Surface with the given dimensions
        self.width = width
        self.height = height
        self.config = config

        # 2D array (list of lists), each cell can hold a reference to an entity or None
        self.grid: List[List[Optional[Entity]]] = [
            [None for _ in range(width)] for _ in range(height)
        ]

        # Master list of all entities for iteration
        self.entities = []

        # Define colors for each entity type
        self.colors = {
            "Plant": (0, 255, 0),    # Green
            "Prey": (0, 0, 255),     # Blue
            "Predator": (255, 0, 0), # Red
            "Food": (255, 255, 0)    # Yellow
        }

        Plant.plant_reproduce += self.handle_plant_reproduce


    def handle_plant_reproduce(self, plant):
        """
        Handle the plant reproduction event by adding a new plant nearby.
        """
        x = plant.x
        y = plant.y
        self.add_new_plant_nearby(x, y)

    def add_new_plant_nearby(self, x: int, y: int):
        """
        Attempt to add a new plant near the given coordinates.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]

        random.shuffle(directions)  # Randomize the order of directions

        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy

            if self.in_bounds(new_x, new_y) and self.grid[new_y][new_x] is None:
                # Add a new plant at the empty cell
                new_plant = Plant(new_x, new_y)
                self.add_entity(new_plant)
                break  # Stop after placing one new plant

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_entity(self, x: int, y: int) -> Optional[Entity]:
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x]

    def add_entity(self, entity: Entity) -> bool:
        """
        Places entity in the grid if free, returns True if successful, False otherwise.
        """
        x, y = entity.x, entity.y
        if not self.in_bounds(x, y):
            return False

        if self.grid[y][x] is not None:
            # Cell is occupied
            return False

        self.grid[y][x] = entity
        self.entities.append(entity)
        return True

    def remove_entity(self, entity: Entity):
        """
        Removes entity from the grid. If the entity is in self.entities, remove it from there too.
        """
        x, y = entity.x, entity.y
        if self.in_bounds(x, y) and self.grid[y][x] == entity:
            self.grid[y][x] = None

        if entity in self.entities:
            self.entities.remove(entity)

    def move_entity(self, entity: Entity, new_x: int, new_y: int) -> bool:
        """
        Tries to move an entity to a new position. Returns True if moved, False otherwise.
        """
        if not self.in_bounds(new_x, new_y):
            return False
        if self.grid[new_y][new_x] is not None:
            # Occupied
            return False

        # Clear old position
        old_x, old_y = entity.x, entity.y
        if self.in_bounds(old_x, old_y) and self.grid[old_y][old_x] == entity:
            self.grid[old_y][old_x] = None

        # Place at new position
        self.grid[new_y][new_x] = entity
        entity.x, entity.y = new_x, new_y
        return True

    def update(self):
        """
        Main per-tick update for the world:
        1. Build a random list of all living entities
        2. Update each one
        3. Remove any that died
        """
        # 1) Shuffle entities
        random.shuffle(self.entities)

        # 2) Update each entity
        for entity in self.entities:
            if entity.alive:
                entity.update(world=self)

        # 3) Remove dead entities
        dead_entities = [e for e in self.entities if not e.alive]
        for e in dead_entities:
            self.remove_entity(e)

        if random.random() <= self.config.get_float("RANDOM_PLANT_PERC"):
            self.add_plant()

    def draw_entities(self):
        """
        Draws all entities on the World surface.
        Each entity is represented as a point with a specific color:
        - Plant: Green
        - Prey: Blue
        - Predator: Red
        - Food: Yellow
        """
        self.fill((0, 0, 0))  # Clear the surface with a black background

        for entity in self.entities:
            entity_type = type(entity).__name__  # Get the entity's type
            if entity_type in self.colors:
                # Draw a single pixel at the entity's position
                self.set_at((entity.x, entity.y), self.colors[entity_type])

    def populate_randomly(self):
        """
        Example method to place some plants, prey, and predators randomly in the world.
        """
        if self.config:
            num_plants = self.config.get_int("INITIAL_PLANTS")
            num_preys = self.config.get_int("INITIAL_PREYS")
            num_preds = self.config.get_int("INITIAL_PREDATORS")
        else:
            return

        # Randomly place plants
        for _ in range(num_plants):
            self.add_plant()

        # Randomly place preys
        for _ in range(num_preys):
            placed = False
            tries = 0
            while not placed and tries < 1000:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                net = NeuralNet(input_size=8, hidden_size=10, output_size=4)
                prey = Prey(x, y, energy=self.config.get_float("PREY_INITIAL"), max_energy=self.config.get_float("PREY_MAX"), net=net)
                if self.add_entity(prey):
                    placed = True
                tries += 1

        # Randomly place predators
        for _ in range(num_preds):
            placed = False
            tries = 0
            while not placed and tries < 1000:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                predator = Predator(x, y, energy=self.config.get_float("PREDATOR_INITIAL"), max_energy=self.config.get_float("PREDATOR_MAX"))
                if self.add_entity(predator):
                    placed = True
                tries += 1

    def add_plant(self):
        placed = False
        tries = 0
        while not placed and tries < 1000:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            plant = Plant(x, y, nutrition_value=1)
            if self.add_entity(plant):
                placed = True
            tries += 1

    def num_plant(self):
        return sum(1 for entity in self.entities if isinstance(entity, Plant))

    def num_prey(self):
        return sum(1 for entity in self.entities if isinstance(entity, Prey))

    def num_predator(self):
        return sum(1 for entity in self.entities if isinstance(entity, Predator))

    def num_food(self):
        return sum(1 for entity in self.entities if isinstance(entity, Food))