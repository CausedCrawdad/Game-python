import pygame, constantes, maps, os
from Tiles_maps import Tile_Grass, Tile_Grass1, Tile_Grass2 
from Player import Player
from enemy import Enemy, boss

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")

class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.sprites = YGroupCamera()
        self.obstacles = pygame.sprite.Group()
        self.Player = None
        self.enemy_list = []
        self.createmap()
    
    def createmap(self):
        # PRIMER RECORRIDO: Crea solo al jugador para que exista para otras entidades
        for row_index, row in enumerate(maps.map1):
            for col_index, col in enumerate(row):
                if col == 9:
                    x = col_index * 32
                    y = row_index * 32 
                    self.Player = Player((x, y), [self.sprites], self.obstacles)
                    break
            if self.Player:
                break

        # SEGUNDO RECORRIDO: Ahora crea todas las demás entidades
        for row_index, row in enumerate(maps.map1):
            for col_index, col in enumerate(row):
                x = col_index * 32
                y = row_index * 32
                
                if col == 1:
                    Tile_Grass2((x, y), [self.sprites, self.obstacles])
                elif col == 8:
                    new_enemy = Enemy((x, y), [self.sprites], "dragon", self.Player, self.obstacles)
                    self.enemy_list.append(new_enemy)
                    new_enemy.is_eliminated = False
                    self.enemy = new_enemy
                elif col == 6:
                    Tile_Grass1((x,y), [self.sprites])

                if col == 7:
                    new_boss = boss((x,y), [self.sprites], "Final_boss",self.Player, self.obstacles)
                    self.enemy_list.append(new_boss)
                    new_boss.is_eliminated = False

    def run(self):
        enemy_triggered = None
        self.enemy_list = [enemy for enemy in self.enemy_list if not getattr(enemy,"is_eliminated",False)]

        for enemy in self.enemy_list:
            if enemy.is_in_battle:
                enemy_triggered = enemy
                break
        for enemy in self.enemy_list:
            if enemy_triggered and enemy != enemy_triggered:
                if enemy.is_in_battle:
                    enemy.is_in_battle = False 
                    enemy.set_battle_scale(False)

        if not enemy_triggered and self.Player:
            self.sprites.draw(self.Player)
            self.sprites.update()
        else:
            self.sprites.draw(self.Player)

        return enemy_triggered

class YGroupCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_size()[0] // 2 
        self.half_height = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.ground = pygame.image.load(os.path.join(ASSETS_DIR, "underground.png")).convert_alpha()
        self.ground_rect = self.ground.get_rect(topleft=(0,0))


        self.zoom_scale = 1.3 
        self.internal_surface_size = (2500,2500)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_width, self.half_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_width
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_height


    def zoom_keybord(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]and self.zoom_scale <= constantes.max_zoom:
            self.zoom_scale += 0.1        
        if keys[pygame.K_o] and self.zoom_scale >= constantes.min_zoom:
            self.zoom_scale -= 0.1
    def draw(self, Player):
        
        self.zoom_keybord()

        self.internal_surface.fill(constantes.Black)
        
        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surface.blit(self.ground,ground_offset)

        
        self.offset.x = Player.rect.centerx - self.half_width
        self.offset.y = Player.rect.centery - self.half_height
        for sprite in sorted(self.sprites(),key= lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surface.blit(sprite.image, offset_rect)
        
        scale_surface = pygame.transform.scale(self.internal_surface,self.internal_surface_size_vector * self.zoom_scale)
        scale_rect = scale_surface.get_rect(center=(self.half_width,self.half_height))       
        
        self.screen.blit(scale_surface,scale_rect)
