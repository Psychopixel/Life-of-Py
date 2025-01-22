import pygame

import src.gameStatus as gs
from src.assetManager import AssetManager
from src.button import Button
from src.event import Event
from src.gameStatus import GameStatus
import matplotlib.pyplot as plt
from io import BytesIO
from src.config import EnvConfig
import numpy as np


class Gui:
    def __init__(self):
        self.config = EnvConfig("config/.env")
        if not self.config.load():
            raise ValueError(
                "Failed to load .env file. Check the file path and contents."
            )
        self.assetManager = AssetManager()
        self.screen = pygame.display.get_surface()
        self.gameStatus = GameStatus()
        self.exit = Event()
        self.calare = Event()
        self.prendi = Event()
        self.restart = Event()
        self.start = Event()
        self.titolo = self.assetManager.load_image("copertina.png")
        self.titolo_rect = self.titolo.get_rect()
        self.background = self.assetManager.load_image("tavolo.png")
        self.background_rect = self.background.get_rect()
        self.startButtonGroup = pygame.sprite.GroupSingle()
        self.start_button = Button(
            self.screen,
            "startButton_up.png",
            "startButton_down.png",
            (self.config.get_int("START_POS_X"), self.config.get_int("START_POS_Y")),
            self.onStartButtonClick,
            "black",
            30,
            "./assett/AdobeFangsongStd-Regular_0.otf",
            "",
            self.startButtonGroup,
        )
        self.exitButtonGroup = pygame.sprite.GroupSingle()
        self.exit_button = Button(
            self.screen,
            "exitButton_up.png",
            "exitButton_down.png",
            (self.config.get_int("EXIT_POS_X"), self.config.get_int("EXIT_POS_Y")),
            self.onExitButtonClick,
            "black",
            30,
            "./assett/AdobeFangsongStd-Regular_0.otf",
            "",
            self.exitButtonGroup,
        )
        # ---------------------------------------------

    def AddSubscriberForStartEvent(self, objMethod):
        self.start += objMethod

    def RemoveSubscribersForStartEvent(self, objMethod):
        self.start -= objMethod

    def AddSubscriberForRestartEvent(self, objMethod):
        self.restart += objMethod

    def RemoveSubscribersRestartEvent(self, objMethod):
        self.restart -= objMethod

    def AddSubscribersForExitEvent(self, objMethod):
        self.exit += objMethod

    def RemoveSubscribersExitEvent(self, objMethod):
        self.exit -= objMethod

    def onExitButtonClick(self):
        self.exit()

    def onStartButtonClick(self):
        self.start()

    def onRestartButtonClick(self):
        self.restart()

    def onCalareButtonClik(self):
        self.calare()

    def onPrendiButtonClick(self):
        self.prendi()

    def blit_text(self, surface, text, pos, font, color=pygame.Color("black")):
        words = [
            word.split(" ") for word in text.splitlines()
        ]  # 2D array where each row is a list of words.
        space = font.size(" ")[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    """
    def generate_angles(self, number, add=0):
        # For number 1, return [0]
        if number == 1:
            return [0 + add]

        angles = []

        # Calculate half of the angles since they will be symmetric
        half_n = number // 2

        for i in range(1, half_n + 1):
            angle = i * gs.SCOPE_ROTATION
            angles.append(angle + add)
            angles.append(-angle + add)

        # If odd number of total angles, append 0 in the center
        if number % 2 != 0:
            angles.append(0 + add)

        return sorted(angles)
"""

    def rotate(self, surface, angle, pivot, offset):
        """Rotate the surface around the pivot point.

        Args:
            surface (pygame.Surface): The surface that is to be rotated.
            angle (float): Rotate by this angle.
            pivot (tuple, list, pygame.math.Vector2): The pivot point.
            offset (pygame.math.Vector2): This vector is added to the pivot.
        """
        rotated_image = pygame.transform.rotozoom(
            surface, -angle, 1
        )  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect  # Return the rotated image and shifted rect.

    def draw_graph(self, surface, population_data, color, x, y, title):
        """
        Draw a graph on the Pygame surface using matplotlib.
        Only the last 100 ticks of the population data are shown.
        The y-axis always starts at 0 and remains at the bottom.
        """
        # Ensure only the last 100 ticks are shown
        if len(population_data) > 100:
            data_to_plot = population_data[-100:]
        else:
            data_to_plot = population_data

        # Handle empty data
        if not data_to_plot:
            data_to_plot = [0]  # Default to 0 if no data is available

        # Create the plot
        plt.figure(
            figsize=(6, 2), dpi=100, facecolor=(0.5, 1, 1, 0.8)
        )  # White background
        plt.plot(
            data_to_plot, color=color, linestyle="-", marker="", label="Population"
        )
        plt.title(title, fontsize=10)
        plt.xlabel("Ticks (Last 100)", fontsize=8)
        plt.ylabel("Population", fontsize=8)
        plt.grid(True)

        # Set x-axis limits (fixed to 100 ticks)
        plt.xlim(0, 100)

        # Set y-axis limits to always start at 0
        y_min = 0  # Always start at 0
        y_max = max(data_to_plot) * 1.1 if data_to_plot else 1  # Add 10% padding
        plt.ylim(y_min, y_max)

        # Use integer ticks on the y-axis
        plt.yticks(
            np.arange(y_min, y_max + 1, max(1, int(y_max / 10)))
        )  # Ensure at least 1 step

        # Ensure the y-axis starts at the bottom
        plt.gca().set_ylim(bottom=0)  # Explicitly set the bottom of the y-axis to 0

        plt.tight_layout()

        # Save the plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(
            buf, format="png", bbox_inches="tight", facecolor=(1, 1, 1, 0.8)
        )  # Ensure background is white
        buf.seek(0)

        # Load the image into Pygame
        image = pygame.image.load(buf)
        surface.blit(image, (x, y))
        plt.close()

    def draw_counters(self, surface, tick, elapsed_time, x, y):
        """
        Draw the tick counter and elapsed time on the Pygame surface.
        """
        font = pygame.font.SysFont("Arial", 24)

        counter_background = pygame.Rect(x, y, 150, 90)
        pygame.draw.rect(surface, pygame.Color(200, 200, 200, 0), counter_background)

        # Draw tick counter
        tick_text = font.render(f"Tick: {tick}", True, self.config.get_color("BLACK"))
        surface.blit(tick_text, (self.config.get_int("COUNTER_TEXT_X"), self.config.get_int("COUNTER_TEXT_Y")))

        # Draw elapsed time
        minutes = int(elapsed_time() // 60)
        seconds = int(elapsed_time() % 60)
        time_text = font.render(
            f"Time: {minutes:02}:{seconds:02}", True, self.config.get_color("BLACK")
        )
        surface.blit(time_text, (self.config.get_int("COUNTER_TEXT_X"), self.config.get_int("COUNTER_TEXT_Y") + self.config.get_int("MARGIN") * 2))

    def draw_entities(self, world, surface):
        """
        Draws entities on the surface based on the 2D world list.
        Each entity is represented as a point with a specific color:
        - Plant: Green
        - Prey: Blue
        - Predator: Red
        - Food: Yellow
        """
        # Define colors for each entity type
        colors = {
            "Plant": (0, 255, 0),    # Green
            "Prey": (0, 0, 255),     # Blue
            "Predator": (255, 0, 0), # Red
            "Food": (255, 255, 0)    # Yellow
        }

        # Iterate through the world grid
        for i in range(self.config.get_int("WORLD_SIZE_X")):
            for j in range(self.config.get_int("WORLD_SIZE_Y")):
                entity = world.get_entity(i,j)  # Get the entity at cell (i, j)
                if entity:  # If the cell is not empty
                    entity_type = type(entity).__name__  # Get the entity's type
                    if entity_type in colors:
                        x = self.config.get_int("WORLD_POS_X") + i
                        y = self.config.get_int("WORLD_POS_Y") + j

                        # Draw a single pixel at the calculated position with the corresponding color
                        surface.set_at((x, y), colors[entity_type])


    def renderScreen(self, events):
        
        #self.screen.fill((0, 0, 0))  # Clear the main screen
        if self.gameStatus.fasePartita == self.config.get("FASE_INIZIO"):
            # Draw the title screen
            self.screen.blit(self.titolo, self.titolo_rect)
            self.start_button.update(events)
            self.start_button.render()
        elif self.gameStatus.fasePartita == self.config.get("FASE_GIOCO"):

            # Create a clean copy of the background surface
            background_copy = self.background.copy()

            # Draw the world grid on the copy
            spazio_world = pygame.Rect(
                self.config.get_int("WORLD_POS_X"),
                self.config.get_int("WORLD_POS_Y"),
                self.config.get_int("WORLD_SIZE_X"),
                self.config.get_int("WORLD_SIZE_Y"),
            )
            pygame.draw.rect(background_copy, (0, 0, 0), spazio_world)

            self.draw_entities(self.gameStatus.world, background_copy)

            # Draw graphs on the copy
            graph_x = self.config.get_int("GRAPH_X")
            self.draw_graph(
                background_copy,
                self.gameStatus.plant_counts,
                "green",
                graph_x,
                self.config.get_int("MARGIN"),
                "Plants: " + str(self.gameStatus.plant_counts[-1]),
            )
            self.draw_graph(
                background_copy,
                self.gameStatus.prey_counts,
                "green",
                graph_x,
                self.config.get_int("MARGIN") + 200,
                "Prey: " + str(self.gameStatus.prey_counts[-1]),
            )
            self.draw_graph(
                background_copy,
                self.gameStatus.predator_counts,
                "green",
                graph_x,
                self.config.get_int("MARGIN") + 400,
                "Predator: "+ str(self.gameStatus.predator_counts[-1]),
            )
            self.draw_graph(
                background_copy,
                self.gameStatus.food_counts,
                "green",
                graph_x,
                self.config.get_int("MARGIN") + 600,
                "Food: "+ str(self.gameStatus.food_counts[-1]),
            )

            # Draw counters on the copy
            self.draw_counters(
                background_copy,
                self.gameStatus.tick,
                self.gameStatus.elapsed_time,
                self.config.get_int("COUNTER_X"),
                self.config.get_int("COUNTER_Y"),
            )

            # Draw the copy to the main screen
            self.screen.blit(background_copy, self.background_rect)

            # Update and render the exit button
            self.exit_button.update(events)
            self.exit_button.render()


        pygame.display.update()  # Update the display

