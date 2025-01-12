from src.world import World
from src.config import EnvConfig
import pygame
import time
from src.entities import Plant, Food, Prey, Predator

def main():
    # Load config
    config = EnvConfig("config/.env")
    config.load()

    pygame.init()
    screen = pygame.display.set_mode((800, 800))  # Example window size
    clock = pygame.time.Clock()

    # Read grid width/height from config or fallback
    world = World(
        width=config.get_int("GRID_WIDTH", fallback=1000),
        height=config.get_int("GRID_HEIGHT", fallback=1000),
        config=config
    )

    # Populate it
    world.populate_randomly()

    running = True
    while running:
        # 1) Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # handle keyboard/mouse here

        # 2) Update simulation if not paused
        world.update()

        # 3) Clear screen
        screen.fill((0, 0, 0))

        # 4) Render each cell or entity
        for e in world.entities:
            # e.x, e.y => transform to screen coords
            color = (0, 0, 0)  # Default color (black)
            if isinstance(e, Plant):
                color = (0, 255, 0)  # Green for plants
            elif isinstance(e, Food):
                color = (255, 255, 0)  # Yellow for food
            elif isinstance(e, Prey):
                color = (0, 0, 255)  # Blue for prey
            elif isinstance(e, Predator):
                color = (255, 0, 0)  # Red for predators

            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(e.x * 4, e.y * 4, 4, 4)  # example scale
            )

        pygame.display.flip()
        clock.tick(60)  # ~60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
