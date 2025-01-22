import pygame
from retro import Retro


class Posizione(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.carta = Retro()
        self.visible = True

    def setCarta(self, sprite:pygame.sprite):
        self.carta = sprite

    def setRetro(self):
        self.carta = Retro()

    def getVisible(self):
        return self.visible
    
    def setVisible(self, visible):
        self.visible = visible
    
    def rect(self):
        return self.carta.rect