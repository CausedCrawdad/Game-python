import pygame, sys
# Importa ahora las clases Player y Enemy directamente, ya que heredan de Sprite
from Player import Player 
from enemy import Enemy
from constantes import *

class battle:
    def __init__(self, player, enemy, enemy_frames, bg_surf, fonts):
        self.display_surface = pygame.display.get_surface()
        self.bg_surf = bg_surf
        self.enemy_frames = enemy_frames
        self.battle_data = {'player': player, 'enemy': enemy}
        self.battle_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.fonts = fonts
        self.setup()
        self.running = True

    def setup(self):
        # Aquí el código ya no crea nuevos sprites
        # Simplemente los añade a los grupos para que se dibujen
        pos = Battle_positions['izq']['center']
        self.battle_data['player'].rect.center = pos
        self.battle_sprites.add(self.battle_data['player'])
        
        pos = Battle_positions['der']['center']
        self.battle_data['enemy'].rect.center = pos
        self.battle_sprites.add(self.battle_data['enemy'])
    
    def update(self, dt):
        self.display_surface.blit(self.bg_surf, (0, 0))
        self.battle_sprites.update(dt)
        self.battle_sprites.draw(self.display_surface)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            self.update(1)
            pygame.display.flip()