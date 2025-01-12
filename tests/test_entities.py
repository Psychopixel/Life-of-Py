import pytest
from src.entities import Plant, Prey, Predator, Food

def test_plant_basic():
    plant = Plant(x=5, y=10, nutrition_value=3)
    assert plant.get_position() == (5, 10)
    assert plant.nutrition_value == 3
    assert plant.alive is True

def test_prey_eat_plant():
    prey = Prey(x=2, y=2, energy=5, max_energy=10)
    prey.eat_plant(3)
    assert prey.energy == 8  # 5 + 3 = 8
    # If we feed more than the max, it should cap
    prey.eat_plant(10)
    assert prey.energy == 10

def test_prey_starve():
    prey = Prey(x=0, y=0, energy=1, max_energy=5)
    prey.update(world="World")  # consumes 0.1 energy (based on code)
    # Not dead yet
    assert prey.alive is True
    # Force next update to starve it
    prey.update(world="World")  # consumes 0.1 energy again (0.8 left, still alive)
    for _ in range(10):
        prey.update(world="World")
    # eventually energy <= 0 => prey.die()
    assert prey.alive is False, "Prey should die after energy is exhausted."

def test_predator_eat_prey():
    pred = Predator(x=3, y=3, energy=20, max_energy=25)
    pred.eat_prey(10)
    # 20 + 10 = 30 => over max => leftover = 5
    assert pred.energy == 25, "Predator energy should cap at 25."

def test_food_decay():
    food = Food(x=5, y=5, amount=2.0, )
    # Update enough times to see some decay
    for _ in range(20):
        food.update(world="World")
    assert food.amount < 2.0, "Food should have decayed at least once."
    # eventually might become 0 and die
    for _ in range(200):
        food.update(world="World")
    assert food.alive is False, "Food should eventually decay to 0 and die."
