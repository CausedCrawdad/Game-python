import pygame, os
from constantes import import_folder  # Importa la función desde constantes

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")
PLAYER_DIR = os.path.join(ASSETS_DIR, "Player")

#imports the character sprite and manages its vector and velocity
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)

        self.battle_sprite = pygame.image.load(os.path.join(ASSETS_DIR, "david_heart.png")).convert_alpha()
        self.battle_sprite = pygame.transform.scale(self.battle_sprite, (64, 64))
        self.import_player_assets()
        self.status = 'down' 
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direccion = pygame.math.Vector2()
        self.velocidad = 6
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.Obstacles = obstacles
        self.in_battle = False
        self.pre_battle_status = None
        self.pre_battle_image = None

               
    def Keybord(self):
        
        if hasattr(self, "in_battle") and self.in_battle:
            return

        keys = pygame.key.get_pressed()
       
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direccion.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direccion.y = 1
            self.status = 'down_idle'
        else:
            self.direccion.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direccion.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direccion.x = 1
            self.status = 'right'
        else:
            self.direccion.x = 0

    def get_status(self):
        #Player is idle
        if self.direccion.x == 0 and self.direccion.y == 0:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'
                self.frame_index = 0
        
        #player is not idle
        else:
            if 'idle' in self.status:
                self.status = self.status.replace('_idle', '')

    def move(self, velocidad):
        if self.direccion.magnitude() != 0:
            self.direccion = self.direccion.normalize()
        
        self.rect.x += self.direccion.x * velocidad
        self.colicion_detection('horizontal')
        self.rect.y += self.direccion.y * velocidad
        self.colicion_detection('vertical')
    
    def colicion_detection(self, direccion):
        if direccion == ("horizontal"):
            for sprite in self.Obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direccion.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direccion.x < 0:
                        self.rect.left = sprite.rect.right
        
        if direccion == ("vertical"):
            for sprite in self.Obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direccion.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direccion.y < 0:
                        self.rect.top = sprite.rect.bottom
    
    def update(self):
        if not hasattr(self, 'in_battle') or not self.in_battle:
            self.Keybord()
            self.move(self.velocidad)
            self.get_status()
        self.animate()
    
    def set_battle_state(self, in_battle):
        self.in_battle = in_battle
        if in_battle:
            self.pre_battle_status = self.status
            self.pre_battle_image = self.image.copy()
            self.image = self.battle_sprite
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)
        else:
            if self.pre_battle_status:
                self.status = self.pre_battle_status
            if self.pre_battle_image:
                self.image = self.pre_battle_image
                old_center = self.rect.center
                self.rect = self.image.get_rect(center=old_center)
            self.frame_index = 0
    def import_player_assets(self):
        character_path = os.path.join(ASSETS_DIR, 'Player')
        self.animations = {'up': [],'down': [],'left': [],'right': [],'right_idle': [],'left_idle': [],'up_idle': [],'down_idle': []}
        
        for animation in self.animations.keys():
            full_path = os.path.join(character_path, animation)
            
            if os.path.exists(full_path):
                self.animations[animation] = import_folder(full_path)

    def animate(self):
        
        if self.in_battle:
            return
        
        animation = self.animations[self.status]
        
        
        if len(animation) == 0:
            idle_status = self.status + '_idle'
            if idle_status in self.animations and len(self.animations[idle_status]) > 0:
                animation = self.animations[idle_status]
            else:
                return 
        
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
