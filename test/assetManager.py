import os

import pygame
from pathlib import Path


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class AssetManager:
    def __init__(self, base_path="assett/"):
        # Ottieni la directory dello script
        script_directory = Path(__file__).resolve().parent

        # Costruisci il percorso completo della cartella self.base_path
        self.base_path = script_directory / base_path

        self.images = {}  # Dictionary to store loaded images
        self.lista_immagini = self.elenca_png()

    def load_all_images(self):
        for i in range(len(self.lista_immagini)):
            self.load_image(self.lista_immagini[i]).convert_alpha()

    def load_image(self, filename):
        """Load an image and return the image object."""
        if filename in self.images:
            return self.images[filename]

        try:
            image = pygame.image.load(self.base_path.as_posix() + os.sep + filename)
            self.images[filename] = image
            return image
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
            return None

    def get_image(self, filename):
        """Retrieve a loaded image, or load it if not yet loaded."""
        if filename not in self.images:
            return self.load_image(filename)
        return self.images[filename]

    def elenca_png(self):
        """
        Ritorna una lista di tutti i file .png nella cartella specificata.
        """
        # Ottieni la directory dello script
        cartella = self.base_path

        # Verifica se la cartella esiste
        if not cartella.exists():
            print(f"La cartella {cartella} non esiste.")
            return []

        # Verifica se è una directory
        if not cartella.is_dir():
            print(f"{cartella} non è una cartella.")
            return []

        # Ritorna la lista dei file .png nella cartella
        return [
            f.name
            for f in cartella.iterdir()
            if f.is_file() and f.suffix.lower() == ".png"
        ]
'''
        return [
            f
            for f in os.listdir(cartella)
            if os.path.isfile(os.path.join(cartella, f)) and f.endswith(".png")
        ]
        '''
