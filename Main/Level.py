import pygame, constantes, maps, os
from Tiles_maps import Tile_Grass, Tiles_Grass1
from Player import Player

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.sprites = YGroupCamera()
        self.obstacles = pygame.sprite.Group()
        self.createmap()
    
    def createmap(self):
        for row_index, row in enumerate(maps.map1):
            for col_index, col in enumerate(row):
                if col == 1:
                    x = col_index * 32
                    y = row_index * 32
                    Tile_Grass((x,y), [self.sprites, self.obstacles])          
                if col == 9:
                    player_x = col_index * 32
                    Player_y = row_index * 32 
                    self.Player = Player((player_x, Player_y),[self.sprites], self.obstacles)
    
    def run(self):
        self.sprites.draw(self.Player)
        self.sprites.update()

class YGroupCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_size()[0] // 2 
        self.half_height = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.ground = pygame.image.load(os.path.join(ASSETS_DIR, "underground.png")).convert_alpha()
        self.ground_rect = self.ground.get_rect(topleft=(0,0))

        #Zoom
        self.zoom_scale = 1 
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
        
        #Ground
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
