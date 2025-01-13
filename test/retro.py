import pygame

from assetManager import AssetManager


class Retro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.assetManager = AssetManager()
        self.image = self.assetManager.get_image("retro.png")

        self.rect = self.image.get_rect()
        self.visible = True

    def getImage(self):
        return self.image

    def rect(self):
        return self.rect

    def surface(self):
        return self.image.getSurface()

    def getVisible(self):
        return self.visible

    def invertVisible(self):
        self.visible = not self.visible
