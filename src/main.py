import pygame
import os
# Get screen resolution
import ctypes

import time
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from src.world import World
from src.config import EnvConfig
from src.entities import Plant, Food, Prey, Predator

user32 = ctypes.windll.user32
# screen_width = user32.GetSystemMetrics(0)
screen_width = 3840
# screen_height = user32.GetSystemMetrics(1)
screen_height = 2160
print("screen_width: " + str(screen_width))
print("screen_height: " + str(screen_height))

# Constants for GUI layout
SCALE_FACTOR = 4  # Scale up the visual representation 4x
WORLD_WIDTH = 500  # Width of the world grid display (scaled)
WORLD_HEIGHT = 500  # Height of the world grid display (scaled)
GRAPH_WIDTH = 300  # Width of each graph
GRAPH_HEIGHT = 200  # Height of each graph
MARGIN = 20  # Margin between elements
WINDOW_WIDTH = WORLD_WIDTH * SCALE_FACTOR + GRAPH_WIDTH + 3 * MARGIN  # Total window width
WINDOW_HEIGHT = WORLD_HEIGHT * SCALE_FACTOR # Total window height

# Calculate window position for center of the screen
window_x = (screen_width - WINDOW_WIDTH) / 2
window_y = (screen_height - WINDOW_HEIGHT) / 2
print("window_x: " + str(window_x))
print("window_y: " + str(window_y))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def draw_graph(surface, data, color, x, y, title):
    """
    Draw a graph on the Pygame surface using matplotlib.
    """
    plt.figure(figsize=(3, 2), dpi=100)
    plt.plot(data, color=color)
    plt.title(title)
    plt.xlabel("Ticks")
    plt.ylabel("Count")
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    # Load the image into Pygame
    image = pygame.image.load(buf)
    surface.blit(image, (x, y))
    plt.close()

def draw_counters(surface, tick, elapsed_time, x, y):
    """
    Draw the tick counter and elapsed time on the Pygame surface.
    """
    font = pygame.font.SysFont("Arial", 24)
    
    # Draw tick counter
    tick_text = font.render(f"Tick: {tick}", True, WHITE)
    surface.blit(tick_text, (x, y))
    
    # Draw elapsed time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, WHITE)
    surface.blit(time_text, (x, y + 30))

def main():
    # Load config
    config = EnvConfig("config/.env")
    config.load()

    pygame.init()
    #screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Life of Py Simulation")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Ottieni l'handle della finestra
    # hwnd = pygame.display.get_wm_info()['window']
    # Imposta la posizione della finestra
    # ctypes.windll.user32.SetWindowPos(hwnd, None, window_x, window_y, 0, 0, 0)

    # Initialize world
    world = World(
        width=config.get_int("GRID_WIDTH", fallback=1000),
        height=config.get_int("GRID_HEIGHT", fallback=1000),
        config=config
    )
    world.populate_randomly()

    # Data for graphs
    plant_counts = []
    prey_counts = []
    predator_counts = []
    food_counts = []
    max_ticks = 100  # Number of ticks to display in the graphs

    # Simulation variables
    running = True
    paused = False
    start_time = time.time()
    tick = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused  # Toggle pause

        if not paused:
            # Update simulation
            world.update()
            tick += 1

            # Update entity counts
            plant_counts.append(sum(1 for e in world.entities if isinstance(e, Plant)))
            prey_counts.append(sum(1 for e in world.entities if isinstance(e, Prey)))
            predator_counts.append(sum(1 for e in world.entities if isinstance(e, Predator)))
            food_counts.append(sum(1 for e in world.entities if isinstance(e, Food)))

            # Keep only the last 100 ticks
            if len(plant_counts) > max_ticks:
                plant_counts.pop(0)
                prey_counts.pop(0)
                predator_counts.pop(0)
                food_counts.pop(0)

        # Clear screen
        screen.fill(BLACK)  # Set background to black

        # Draw the world grid
        for e in world.entities:
            color = WHITE  # Default color
            if isinstance(e, Plant):
                color = GREEN  # Green for plants
            elif isinstance(e, Food):
                color = YELLOW  # Yellow for food
            elif isinstance(e, Prey):
                color = BLUE  # Blue for prey
            elif isinstance(e, Predator):
                color = RED  # Red for predators

            # Scale entity positions and size by SCALE_FACTOR
            scaled_x = int(e.x * (WORLD_WIDTH / world.width) * SCALE_FACTOR)
            scaled_y = int(e.y * (WORLD_HEIGHT / world.height) * SCALE_FACTOR)
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(scaled_x, scaled_y, SCALE_FACTOR, SCALE_FACTOR)  # Draw as a 4x4 pixel square
            )

        # Draw graphs
        graph_x = WORLD_WIDTH * SCALE_FACTOR + MARGIN  # Position graphs to the right of the world grid
        draw_graph(screen, plant_counts, "green", graph_x, MARGIN, "Plants")
        draw_graph(screen, prey_counts, "blue", graph_x, GRAPH_HEIGHT + 2 * MARGIN, "Prey")
        draw_graph(screen, predator_counts, "red", graph_x, 2 * GRAPH_HEIGHT + 3 * MARGIN, "Predators")
        draw_graph(screen, food_counts, "yellow", graph_x, 3 * GRAPH_HEIGHT + 4 * MARGIN, "Food")

        # Draw counters below the graphs
        elapsed_time = time.time() - start_time
        draw_counters(screen, tick, elapsed_time, graph_x, 4 * GRAPH_HEIGHT + 5 * MARGIN)

        # Update display
        pygame.display.flip()
        clock.tick(60)  # ~60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()