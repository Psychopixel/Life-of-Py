from src.world import World
from src.config import EnvConfig

def main():
    # Load config
    config = EnvConfig("config/.env")
    config.load()

    # Read grid width/height from config or fallback
    world = World(
        width=config.get_int("GRID_WIDTH", fallback=200),
        height=config.get_int("GRID_HEIGHT", fallback=200),
        config=config
    )

    # Populate it
    world.populate_randomly()

    # Example main loop
    num_ticks = 1000
    for tick in range(num_ticks):
        world.update()  # calls update() on each entity in random order
        # Possibly do some printing/logging
        if tick % 50 == 0:
            print(f"Tick {tick}: {len(world.entities)} entities alive.")

    print("Simulation finished.")

if __name__ == "__main__":
    main()