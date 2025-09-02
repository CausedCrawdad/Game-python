import pygame, maps, os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")


class Tile_Grass(pygame.sprite.Sprite):
    def __init__(self, posicition, groups):
        super().__init__(groups)

        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "grass.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=posicition)

class Tile_Grass1(pygame.sprite.Sprite):
    def __init__(self, posicition, groups):
        super().__init__(groups)

        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "grass1.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=posicition)

class Tile_Grass2(pygame.sprite.Sprite):
    def __init__(self, posicition, groups):
        super().__init__(groups)

        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "grass2.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=posicition)
