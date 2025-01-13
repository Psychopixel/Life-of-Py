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
        self.background = self.assetManager.load_image("tavolo.png")
        self.titolo = self.assetManager.load_image("titolobackground.png")
        self.titolo_rect = self.titolo.get_rect()
        self.titolo_rect.center = gs.TITOLO_POS
        self.prendi_button = Button(
            self.screen,
            "prendi_up.png",
            "prendi_down.png",
            (self.screen.get_width() / 2, 720),
            self.onPrendiButtonClick,
            "black",
            30,
            "./assett/AdobeFangsongStd-Regular_0.otf",
            "",
        )
        self.exitButtonGroup = pygame.sprite.GroupSingle()
        self.exit_button = Button(
            self.screen,
            "offButton_up.png",
            "offButton_down.png",
            gs.EXIT_POS,
            self.onExitButtonClick,
            "black",
            30,
            "./assett/AdobeFangsongStd-Regular_0.otf",
            "",
            self.exitButtonGroup,
        )
        self.calare_button = Button(
            self.screen,
            "calare.png",
            "calare.png",
            ((gs.SCREEN_WIDTH / 2) + (gs.CARDSPACE * 2), gs.PLAYER_Y),
            self.onCalareButtonClik,
            "white",
            25,
            "./assett/AdobeFangsongStd-Regular_0.otf",
            "",
        )
        self.restartButtonGroup = pygame.sprite.GroupSingle()
        self.restart_button = Button(
            self.screen,
            "restart_up.png",
            "restart_down.png",
            gs.RESTART_POS,
            self.onRestartButtonClick,
            "black",
            30,
            "./assett/AdobeFangsongStd-Regular_0.otf",
            "",
            self.restartButtonGroup,
        )
        self.startButtonGroup = pygame.sprite.GroupSingle()
        self.start_button = Button(
            self.screen,
            "start_up.png",
            "start_down.png",
            gs.START_POS,
            self.onStartButtonClick,
            "black",
            30,
            "./assett/AdobeFangsongStd-Regular_0.otf",
            "",
            self.startButtonGroup,
        )

        # for seme in SEMI_BREVI:
        #     for n in range(1, 11):
        #         carta = Carta(seme + str(n))
        #         self.gameStatus.carte.append(carta)

        # random.shuffle(self.gameStatus.carte)

        # ---------------------------------------------
        self.playerCardPos = [
            (self.screen.get_width() / 2 - gs.CARDSPACE, gs.PLAYER_Y),
            (self.screen.get_width() / 2, gs.PLAYER_Y),
            (self.screen.get_width() / 2 + gs.CARDSPACE, gs.PLAYER_Y),
        ]

        self.aiCardPos = [
            (self.screen.get_width() / 2 - gs.CARDSPACE, gs.AI_Y),
            (self.screen.get_width() / 2, gs.AI_Y),
            (self.screen.get_width() / 2 + gs.CARDSPACE, gs.AI_Y),
        ]

        self.gameStatus.tablePos = []

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

    def AddSubscribersForCalareEvent(self, objMethod):
        self.calare += objMethod

    def RemoveSubscribersCalareEvent(self, objMethod):
        self.calare -= objMethod

    def AddSubscribersForPrendiEvent(self, objMethod):
        self.prendi += objMethod

    def RemoveSubscribersPrendiEvent(self, objMethod):
        self.prendi -= objMethod

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

    def createTablePos(self):
        if len(self.tableCard) == 0:
            return []
        num_objects = len(self.tableCard)
        # Calculate total width occupied by objects and spaces
        total_width = gs.CARD_WIDTH * num_objects + gs.TABLESPACE * (num_objects - 1)

        # Calculate starting position (left side of the first object)
        start_pos = (gs.SCREEN_WIDTH - total_width) / 2 + (gs.CARD_WIDTH / 2)

        # Calculate centers
        centers = []
        for i in range(num_objects):
            center = start_pos + i * (gs.CARD_WIDTH + gs.TABLESPACE)
            centers.append((center, gs.TABLE_Y))

        return centers

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
            self.exit_button.update(events)
            self.exit_button.render()
            self.start_button.update(events)
            self.start_button.render()
        elif self.gameStatus.fasePartita == gs.FASE_GIOCO:
            value_list = [
                self.gameStatus.tableCard[x].valore
                for x in range(0, len(self.gameStatus.tableCard))
            ]
            self.tableCard = tableCard
            cnt = 0
            for i in range(len(self.gameStatus.playerHand)):
                self.gameStatus.playerHand[cnt].rect.center = self.playerCardPos[i]
                self.screen.blit(
                    self.gameStatus.playerHand[cnt].getImage(),
                    self.gameStatus.playerHand[cnt].rect,
                )
                if self.gameStatus.playerHand[cnt].selected:
                    pygame.draw.rect(
                        self.screen, "red", self.gameStatus.playerHand[cnt].rect, 5
                    )
                cnt += 1

            cnt = 0
            for i in range(0, len(self.tableCard)):
                self.gameStatus.tablePos = self.createTablePos()
                self.tableCard[cnt].rect.center = self.gameStatus.tablePos[i]
                self.screen.blit(
                    self.tableCard[cnt].getImage(), self.tableCard[cnt].rect
                )
                if self.tableCard[cnt].selected:
                    pygame.draw.rect(self.screen, "purple", self.tableCard[cnt].rect, 5)
                cnt += 1
            if len(self.gameStatus.carte) > 0:
                self.gameStatus.pile.rect.center = gs.PILE_POS
                self.screen.blit(
                    self.gameStatus.pile.getImage(), self.gameStatus.pile.rect
                )
                test_font = pygame.font.Font(None, 55)
                pile_left = test_font.render(
                    f"{len(self.gameStatus.carte)}", False, "red"
                )
                pile_left_rect = pile_left.get_rect(center=gs.PILE_POS)
                pygame.draw.rect(self.screen, "black", pile_left_rect)
                pygame.draw.rect(self.screen, "black", pile_left_rect, 10)
                self.screen.blit(pile_left, pile_left_rect)

            if len(self.gameStatus.carteScopaPlayer) > 0:
                angle = self.generate_angles(len(self.gameStatus.carteScopaPlayer))
                for i in range(len(self.gameStatus.carteScopaPlayer)):
                    if not self.gameStatus.carteScopaPlayer[i].rotated:
                        pos = gs.SCOPE_PLAYER_POS
                        if len(angle) > 1:
                            if angle[i] == 180:
                                moveOffset = pygame.math.Vector2(0, 0)
                            else:
                                moveOffset = pygame.math.Vector2(0, 0)
                                if i < len(angle) / 2:
                                    xOffset = (len(angle) - (i + 1)) * -gs.SCOPE_SPACE
                                else:
                                    xOffset = i * gs.SCOPE_SPACE
                                moveOffset = pygame.math.Vector2(xOffset, 0)
                            pos = pos + moveOffset
                        self.gameStatus.carteScopaPlayer[i].rect.center = pos
                        if len(angle) > 1:
                            (
                                self.gameStatus.carteScopaPlayer[i].image,
                                self.gameStatus.carteScopaPlayer[i].rect,
                            ) = self.rotate(
                                self.gameStatus.carteScopaPlayer[i].image,
                                angle[i],
                                self.gameStatus.carteScopaPlayer[i].rect.midbottom,
                                gs.SCOPE_PLAYER_MOVE,
                            )
                        self.gameStatus.carteScopaPlayer[i].rotated = True
                    self.screen.blit(
                        self.gameStatus.carteScopaPlayer[i].getImage(),
                        self.gameStatus.carteScopaPlayer[i].rect,
                    )

            if len(self.gameStatus.carteScopaAi) > 0:
                angle = self.generate_angles(len(self.gameStatus.carteScopaAi), add=180)
                for i in range(len(self.gameStatus.carteScopaAi)):
                    if not self.gameStatus.carteScopaAi[i].rotated:
                        pos = gs.SCOPE_AI_POS
                        if len(angle) > 1:
                            if angle[i] == 180:
                                moveOffset = pygame.math.Vector2(0, 0)
                            else:
                                moveOffset = pygame.math.Vector2(0, 0)
                                if i < len(angle) / 2:
                                    xOffset = (len(angle) - (i + 1)) * gs.SCOPE_SPACE
                                else:
                                    xOffset = i * -gs.SCOPE_SPACE
                                moveOffset = pygame.math.Vector2(xOffset, 0)
                            pos = pos + moveOffset
                        self.gameStatus.carteScopaAi[i].rect.center = pos
                        (
                            self.gameStatus.carteScopaAi[i].image,
                            self.gameStatus.carteScopaAi[i].rect,
                        ) = self.rotate(
                            self.gameStatus.carteScopaAi[i].image,
                            angle[i],
                            self.gameStatus.carteScopaAi[i].rect.midbottom,
                            gs.SCOPE_AI_MOVE,
                        )
                        self.gameStatus.carteScopaAi[i].rotated = True
                    self.screen.blit(
                        self.gameStatus.carteScopaAi[i].getImage(),
                        self.gameStatus.carteScopaAi[i].rect,
                    )
            for i in range(0, len(self.gameStatus.aiCovered)):
                if self.gameStatus.aiCovered[i].getVisible():
                    self.gameStatus.aiCovered[i].carta.rect.center = self.aiCardPos[i]
                    self.screen.blit(
                        self.gameStatus.aiCovered[i].carta.getImage(),
                        self.gameStatus.aiCovered[i].carta.rect,
                    )
            for i in range(0, len(self.gameStatus.aiHand)):
                if self.gameStatus.aiHand[i].getVisible():
                    self.gameStatus.aiHand[i].rect.center = self.aiCardPos[i]
                    self.screen.blit(
                        self.gameStatus.aiHand[i].getImage(),
                        self.gameStatus.aiHand[i].rect,
                    )
            if len(self.gameStatus.player_captures) > 0:
                self.gameStatus.player_capturesImage.rect.center = gs.PRESE_PLAYER_POS
                self.screen.blit(
                    self.gameStatus.player_capturesImage.getImage(),
                    self.gameStatus.player_capturesImage.rect,
                )
                test_font = pygame.font.Font(None, 55)
                prese_player_number = test_font.render(
                    f"{len(self.gameStatus.player_captures) + len(self.gameStatus.carteScopaPlayer)}",
                    False,
                    "red",
                )
                prese_player_number_rect = prese_player_number.get_rect(
                    center=gs.PRESE_PLAYER_POS
                )
                pygame.draw.rect(self.screen, "black", prese_player_number_rect)
                pygame.draw.rect(self.screen, "black", prese_player_number_rect, 10)
                self.screen.blit(prese_player_number, prese_player_number_rect)

            if len(self.gameStatus.ai_captures) > 0:
                self.gameStatus.ai_capturesImage.rect.center = gs.PRESE_AI_POS
                self.screen.blit(
                    self.gameStatus.ai_capturesImage.getImage(),
                    self.gameStatus.ai_capturesImage.rect,
                )
                test_font = pygame.font.Font(None, 55)
                prese_ai_number = test_font.render(
                    f"{len(self.gameStatus.ai_captures) + len(self.gameStatus.carteScopaAi)}",
                    False,
                    "red",
                )
                prese_ai_number_rect = prese_ai_number.get_rect(center=gs.PRESE_AI_POS)
                pygame.draw.rect(self.screen, "black", prese_ai_number_rect)
                pygame.draw.rect(self.screen, "black", prese_ai_number_rect, 10)
                self.screen.blit(prese_ai_number, prese_ai_number_rect)

            self.prendi_button.update(events)
            if self.gameStatus.presa:
                self.prendi_button.render()

            self.exit_button.update(events)
            self.exit_button.render()

            if (
                not self.gameStatus.find_sum_in_list(
                    self.gameStatus.player_card_selected_value, value_list
                )
                and self.gameStatus.player_card_selected
            ):
                self.calare_button.update(events)
                self.calare_button.render()
            font = pygame.font.SysFont("Arial", 30)
            self.blit_text(
                self.screen,
                "Punti Ai: " + str(self.gameStatus.ai_total_points),
                gs.PUNTI_AI_POS,
                font,
                "white",
            )
            self.blit_text(
                self.screen,
                "Punti Player: " + str(self.gameStatus.player_total_points),
                gs.PUNTI_PLAYER_POS,
                font,
                "white",
            )

        elif self.gameStatus.fasePartita == gs.FASE_PUNTEGGIO:
            if self.gameStatus.endText != "":
                font = pygame.font.SysFont("Arial", 64)
                self.blit_text(
                    self.screen, self.gameStatus.endText, gs.END_TEXT_POS, font, "white"
                )
            self.exit_button.update(events)
            self.exit_button.render()
            pygame.time.set_timer(gs.NUOVA_MANO, 3000, 1)
        elif self.gameStatus.fasePartita == gs.FASE_FINE:
            font = pygame.font.SysFont("Arial", 64)
            self.blit_text(
                self.screen, self.gameStatus.endText, gs.END_TEXT_POS, font, "white"
            )
            self.restart_button.update(events)
            self.restart_button.render()
            self.exit_button.update(events)
            self.exit_button.render()
        else:
            pass

        pygame.display.update()
