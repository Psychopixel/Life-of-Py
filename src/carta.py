import pygame

import gameStatus
from assetManager import AssetManager


class Carta(pygame.sprite.Sprite):
    def __init__(self, carta: str):
        pygame.sprite.Sprite.__init__(self)
        self.assetManager = AssetManager()
        self.carta = carta
        self.image = self.assetManager.load_image(carta + ".png")
        self.seme = gameStatus.SEMI[gameStatus.SEMI_BREVI.index(carta[0])]
        self.valore = int(carta[1:])
        if self.valore == 7 and self.seme == "Denari":
            self.nome = gameStatus.SETTEBELLO
        else:
            self.nome = str(gameStatus.VALORI[self.valore - 1]) + " di " + self.seme
        self.valorePrimiera = gameStatus.VALORI_PRIMIERA[self.valore - 1]

        self.rect = self.image.get_rect()
        self.selected = False
        self.visible = True
        self.rotated = False

    def getSeme(self):
        return self.seme

    def getValore(self):
        return self.valore

    def getValorePrimiera(self):
        return self.valorePrimiera

    def getNome(self):
        return self.nome

    def getImage(self):
        return self.image

    def getRect(self):
        self.rect = self.image.get_rect()
        return self.rect

    def invertSelection(self):
        self.selected = not self.selected

    def surface(self):
        return self.image.getSurface()

    def copy(self):
        return Carta(self.carta)

    def getVisible(self):
        return self.visible
