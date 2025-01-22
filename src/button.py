import pygame

from src.assetManager import AssetManager


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        screen,
        up: str,
        down: str,
        pos: tuple,
        callback,
        textColor,
        text_size,
        text_font="None",
        text: str = "",
        group: pygame.sprite.GroupSingle = [],
    ):
        pygame.sprite.Sprite.__init__(self, group)
        self.callback = callback
        self.pos = pos
        self.textColor = textColor
        self.text = text
        self.textSize = text_size
        self.text_font = text_font
        self.screen = screen

        self.assetManager = AssetManager()

        self.imageUp = self.assetManager.get_image(up)
        self.imageDown = self.assetManager.get_image(down)
        self.image = self.imageUp
        self.pressed = False
        self.rect = self.imageUp.get_rect(center=self.pos)
        self.render()

    def render(self):
        '''
        test_font = pygame.font.Font(self.text_font, self.textSize)
        button_text = test_font.render(self.text, False, self.textColor).convert_alpha()
        button_text_rect = button_text.get_rect(center=self.pos)
        '''
        if not self.pressed:
            self.image = self.imageUp
            self.rect = self.image.get_rect(center=self.pos)
            self.screen.blit(self.imageUp, self.rect)
        else:
            self.image = self.imageDown
            self.rect = self.image.get_rect(center=self.pos)
            self.screen.blit(self.image, self.rect)
        #self.screen.blit(button_text, button_text_rect)

    def get_rect(self):
        return self.rect

    def update(self, events):
        super().update(self)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.pressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.pressed = False
                if self.rect.collidepoint(event.pos):
                    self.callback()
