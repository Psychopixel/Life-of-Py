# src/entities.py
from typing import Optional, Tuple
from src.neural_net import NeuralNet
from src.config import EnvConfig
from src.event import Event
import numpy as np
import random  # Importazione mancante

class Entity:
    """
    Base class for all in-world entities (Plant, Prey, Predator, Food).
    """

    def __init__(self, x: int, y: int):
        self.config = EnvConfig("config/.env")
        if not self.config.load():
            raise ValueError("Failed to load .env file. Check the file path and contents.")
        """
        :param x: X position on the grid
        :param y: Y position on the grid
        """
        self.x = x
        self.y = y
        self.alive = True  # or active status

    def update(self, world: "World"):
        """
        Called every simulation tick to update entity state.
        Derived classes will override this.
        """
        pass

    def get_position(self) -> Tuple[int, int]:
        """
        Return the (x, y) position of this entity.
        """
        return self.x, self.y

    def die(self):
        """
        Mark the entity as dead (to be removed from the simulation).
        """
        self.alive = False


class Plant(Entity):
    """
    Plants have no movement, but can reproduce or be eaten.
    In the future, we might add growth timers or reproduction logic.
    """

    plant_reproduce = Event()

    def __init__(self, x: int, y: int, nutrition_value: int = 1):
        super().__init__(x, y)
        self.nutrition_value = nutrition_value
        self.ticks_to_mature = 0  # placeholder for future growth logic

    def update(self, world: "World"):
        """
        For now, plants do nothing unless we implement growth or reproduction logic.
        """
        # e.g., if self.ticks_to_mature > 0: self.ticks_to_mature -= 1
        if self.ticks_to_mature < self.config.get_int("PLANT_TICK_TO_MATURE"):
            self.ticks_to_mature += 1
        # Check if the plant reproduces
        if self.ticks_to_mature >= self.config.get_int("PLANT_TICK_TO_MATURE"):
            check = random.random()  # Random float between 0 and 1
            if check <= self.config.get_float("PLANT_PERC_NEW"):
                # Generate a reproduction event
                # Trigger the plant reproduction event
                Plant.plant_reproduce(self)
                


class Food(Entity):
    """
    Represents leftover food from dead creatures or excess from a predator's meal.
    """

    def __init__(self, x: int, y: int, amount: float = 1.0):
        super().__init__(x, y)
        self.amount = amount  # how much nutritional value is left
        self.decay_rate = 0.1  # just an example for slow decay
        self.decay_timer = 0

    def update(self, world: "World"):
        """
        Decay the food over time. When it reaches 0, it's effectively gone.
        """
        self.decay_timer += 1  # or some time logic
        # for a simple approach: reduce 'amount' every few ticks
        if self.decay_timer >= 10:
            # lose some fraction
            self.amount -= self.decay_rate
            self.decay_timer = 0

        if self.amount <= 0:
            self.die()


class Prey(Entity):
    """
    Prey are creatures that:
    - Have energy and can starve if it reaches 0.
    - Eat plants to regain energy.
    - Use a neural network to decide actions (stay still, turn, move forward).
    - Eventually reproduce if conditions are met.
    """

    def __init__(
        self,
        x: int,
        y: int,
        energy: float = 10.0,
        max_energy: float = 20.0,
        net: Optional[NeuralNet] = None,
        reproduction_cooldown_max: int = 100,
        reproduction_energy_threshold: float = 15.0
    ):
        """
        :param x: Initial X-coordinate
        :param y: Initial Y-coordinate
        :param energy: Starting energy
        :param max_energy: Maximum energy cap
        :param net: A NeuralNet instance (optional)
        :param reproduction_cooldown_max: Ticks required between reproductions
        :param reproduction_energy_threshold: Minimum energy required to reproduce
        """
        super().__init__(x, y)
        self.energy = energy
        self.max_energy = max_energy
        self.net = net  # If None, the Prey won't do NN-driven actions.
        self.direction = 0  # 0=Up, 1=Right, 2=Down, 3=Left

        # Reproduction logic
        self.reproduction_cooldown_max = reproduction_cooldown_max
        self.reproduction_cooldown = self.reproduction_cooldown_max
        self.reproduction_energy_threshold = reproduction_energy_threshold

    def update(self, world: "World"):
        """
        Called every tick to update the Prey's state.
        1) Consume idle energy.
        2) Check for starvation.
        3) If there's a neural net, run it to decide an action.
        4) Handle movement/eating plants if the chosen action is 'move forward'.
        5) Count down reproduction cooldown; reproduce if possible.
        """
        # (1) Idle energy consumption
        self._consume_energy(0.1)  # Example idle cost

        # (2) Check for starvation
        if self.energy <= 0:
            self.die()
            return

        # (3) Neural net logic: decide an action if we have a net
        if self.net:
            action_idx = self._decide_action(world)
            self._execute_action(action_idx, world)

        # (4) Reproduction logic
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1
        elif self.energy >= self.reproduction_energy_threshold:
            self._attempt_reproduction(world)

    def eat_plant(self, plant_nutrition: float):
        """
        Increase energy by the plant's nutrition value, capped at max_energy.
        """
        self.energy = min(self.max_energy, self.energy + plant_nutrition)

    def _consume_energy(self, amount: float):
        """
        Subtract a specified amount of energy. If <= 0, entity will die in update().
        """
        self.energy -= amount

    def _decide_action(self, world: "World") -> int:
        """
        Build the input vector for the neural net, run forward pass, return argmax action index.
        The typical mapping might be:
        0 -> Stay still
        1 -> Turn left
        2 -> Turn right
        3 -> Move forward
        """
        # Example 8 inputs (you can expand these with real "vision" logic)
        energy_norm = self.energy / self.max_energy
        repro_norm = self.reproduction_cooldown / self.reproduction_cooldown_max \
                     if self.reproduction_cooldown_max > 0 else 0.0

        # Dummy placeholders for "view" (left, front, right) type/distance
        # In a real simulation, you'd check the cells around the Prey and encode them properly.
        left_type = 0.0
        left_dist = 0.0
        front_type = 0.0
        front_dist = 0.0
        right_type = 0.0
        right_dist = 0.0

        input_vec = np.array([
            energy_norm,
            repro_norm,
            left_type,
            left_dist,
            front_type,
            front_dist,
            right_type,
            right_dist
        ], dtype=np.float32)

        output = self.net.forward(input_vec)
        action_idx = np.argmax(output)  # Choose the action with highest score
        return action_idx

    def _execute_action(self, action_idx: int, world: "World"):
        """
        Perform the action chosen by the neural net.
        0 -> Stay still
        1 -> Turn left  (direction -= 1)
        2 -> Turn right (direction += 1)
        3 -> Move forward in the current direction
        """
        if action_idx == 0:
            # Stay still
            pass
        elif action_idx == 1:
            # Turn left
            self.direction = (self.direction - 1) % 4
        elif action_idx == 2:
            # Turn right
            self.direction = (self.direction + 1) % 4
        elif action_idx == 3:
            # Move forward
            dx, dy = self._dir_to_vector(self.direction)
            new_x = self.x + dx
            new_y = self.y + dy

            # Check bounds
            if not world.in_bounds(new_x, new_y):
                return  # Can't move out of bounds

            occupant = world.get_entity(new_x, new_y)
            if occupant is None:
                # Move if cell is free
                world.move_entity(self, new_x, new_y)
            elif isinstance(occupant, Plant):
                # Eat the plant, then move into its cell
                self.eat_plant(occupant.nutrition_value)
                occupant.die()
                world.move_entity(self, new_x, new_y)
            # If occupant is another Prey, Predator, or Food, handle accordingly
            # (e.g., Prey won't eat Food, Predator might eat Prey, etc.)

    def _dir_to_vector(self, direction: int) -> Tuple[int, int]:
        """
        Converts a direction index (0=Up, 1=Right, 2=Down, 3=Left)
        into an (dx, dy) movement vector.
        """
        if direction == 0:  # Up
            return 0, -1
        elif direction == 1:  # Right
            return 1, 0
        elif direction == 2:  # Down
            return 0, 1
        elif direction == 3:  # Left
            return -1, 0
        return 0, 0

    def _attempt_reproduction(self, world: "World"):
        """
        Tries to create a new Prey in one of the adjacent cells (if free).
        Resets reproduction cooldown and deducts some energy if needed.
        Also demonstrates how to mutate the neural net for offspring.
        """
        # For example, check the 8 surrounding cells for a free spot
        offsets = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0),           (1, 0),
            (-1, 1),  (0, 1),  (1, 1)
        ]
        possible_positions = []
        for dx, dy in offsets:
            nx, ny = self.x + dx, self.y + dy
            if world.in_bounds(nx, ny) and world.get_entity(nx, ny) is None:
                possible_positions.append((nx, ny))

        if not possible_positions:
            return  # No space to reproduce

        # Choose a random adjacent cell
        child_x, child_y = random.choice(possible_positions)

        # Create a "child" neural net by copying and mutating the parent's net
        child_net = None
        if self.net:
            child_net = NeuralNet(
                input_size=self.net.input_size,
                hidden_size=self.net.hidden_size,
                output_size=self.net.output_size
            )
            # Copy weights from parent
            child_net.W1 = self.net.W1.copy()
            child_net.b1 = self.net.b1.copy()
            child_net.W2 = self.net.W2.copy()
            child_net.b2 = self.net.b2.copy()
            # Mutate them
            mutation_rate = 0.05   # or from config
            mutation_stddev = 0.1
            child_net.mutate(mutation_rate, mutation_stddev)

        # Create the child Prey
        child = Prey(
            x=child_x,
            y=child_y,
            energy=self.energy * 0.5,  # example: half the parent's energy
            max_energy=self.max_energy,
            net=child_net,
            reproduction_cooldown_max=self.reproduction_cooldown_max,
            reproduction_energy_threshold=self.reproduction_energy_threshold
        )
        # Deduct parent's energy (example: half goes to child)
        self.energy *= 0.5

        # Reset parent's reproduction cooldown
        self.reproduction_cooldown = self.reproduction_cooldown_max

        # Finally, add child to the world
        world.add_entity(child)


class Predator(Entity):
    """
    Predators eat prey (and sometimes leftover food).
    """

    def __init__(self, x: int, y: int, energy: float = 12.0, max_energy: float = 25.0):
        super().__init__(x, y)
        self.energy = energy
        self.max_energy = max_energy
        self.reproduction_cooldown = 120  # example
        self.direction = 0

    def update(self, world: "World"):
        """
        - Decrease energy from movement
        - Possibly chase prey or random movement
        - Reproduce if conditions are met
        """
        self._consume_energy(0.2)  # example idle cost

        if self.energy <= 0:
            self.die()
            return

        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1

    def eat_prey(self, prey_energy: float):
        """
        Increase energy by some or all of the prey's energy.
        If it exceeds max, leftover becomes Food in the simulation (handled in World).
        """
        self.energy += prey_energy
        if self.energy > self.max_energy:
            excess = self.energy - self.max_energy
            self.energy = self.max_energy
            # We’ll need the world logic to create leftover Food with 'excess'

    def _consume_energy(self, amount: float):
        """
        Subtract a specified amount of energy.
        """
        self.energy -= amount