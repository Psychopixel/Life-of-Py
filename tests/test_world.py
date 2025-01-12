import pytest
from src.world import World
from src.entities import Plant, Prey, Predator

def test_world_add_remove():
    w = World(width=10, height=10)

    plant = Plant(2, 2)
    assert w.add_entity(plant) is True
    assert w.get_entity(2, 2) == plant

    # Attempt to place another entity in the same cell
    predator = Predator(2, 2)
    assert w.add_entity(predator) is False, "Cell is occupied"

    # Remove the plant
    w.remove_entity(plant)
    assert w.get_entity(2, 2) is None

def test_world_move_entity():
    w = World(width=10, height=10)
    prey = Prey(2, 2)
    w.add_entity(prey)

    # Move to (3, 2)
    assert w.move_entity(prey, 3, 2) is True
    assert w.get_entity(3, 2) == prey
    assert w.get_entity(2, 2) is None

    # Move out of bounds
    assert w.move_entity(prey, -1, 10) is False

def test_world_update():
    # small world, no collisions expected if we place them carefully
    w = World(width=5, height=5)
    p1 = Prey(0, 0, energy=1)   # very low energy, might die soon
    p2 = Prey(1, 1, energy=5)
    w.add_entity(p1)
    w.add_entity(p2)

    # We'll track how many survive after some ticks
    for _ in range(10):
        w.update()
    # p1 might starve quickly (energy used in update)
    alive_preys = [e for e in w.entities if isinstance(e, Prey) and e.alive]
    assert len(alive_preys) >= 1, "At least p2 should survive"
