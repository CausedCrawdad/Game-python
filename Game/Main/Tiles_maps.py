import pygame, maps, os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")


class Tile_Grass(pygame.sprite.Sprite):
    def __init__(self, posicition, groups):
        super().__init__(groups)

        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "grass.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=posicition)

class Tiles_Grass1(pygame.sprite.Sprite):
    def __init__(self, posicition, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load("Assets/grass1.png").convert_alpha()
        self.scale = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=posicition)
