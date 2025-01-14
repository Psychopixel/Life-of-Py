import pygame

import gameStatus as gs
from assetManager import AssetManager
from button import Button
from event import Event
from gameStatus import GameStatus


class Gui:
    def __init__(self, screen):
        self.assetManager = AssetManager()
        self.screen = screen
        self.gameStatus = GameStatus()
        self.exit = Event()
        self.calare = Event()
        self.prendi = Event()
        self.restart = Event()
        self.start = Event()
        self.titolo = self.assetManager.load_image("copertina.png")
        self.titolo_rect = self.titolo.get_rect()
        self.background = self.assetManager.load_image("tavolo.png")
        self.startButtonGroup = pygame.sprite.GroupSingle()
        self.start_button = Button(
            self.screen,
            "startButton_up.png",
            "startButton_down.png",
            gs.START_POS,
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
            gs.EXIT_POS,
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

    def renderScreen(self, events, tableCard):
        # self.screen.fill((30, 120, 0))
        self.screen.blit(self.background, self.background.get_rect())

        if self.gameStatus.fasePartita == gs.FASE_INIZIO:
            self.screen.blit(self.titolo, self.titolo_rect)
            """ self.exit_button.update(events)
            self.exit_button.render()
            """
            self.start_button.update(events)
            self.start_button.render() 
        elif self.gameStatus.fasePartita == gs.FASE_GIOCO:
            self.exit_button.update(events)
            self.exit_button.render() 
            pass
        else:
            pass

        pygame.display.update()
