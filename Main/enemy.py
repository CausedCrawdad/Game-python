import pygame, os, random
from constantes import import_folder
from sprites import Entity

# Directorios de recursos
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")
ENEMY_DIR = os.path.join(ASSETS_DIR, "Enemies")

# Ahora la clase Enemy hereda de la nueva clase base Entity
class Enemy(Entity):
    def __init__(self, pos, groups, name, player_sprite, obstacles):
        # Llama al constructor de la clase padre (Entity)
        super().__init__(pos, groups, obstacles)
        self.name = name
        self.player = player_sprite
        self.obstacles = obstacles
        
        # Carga los recursos del enemigo
        self.import_assets()
        self.status = 'idle'
        self.scale_factor = 1.0 
        self.battle_scale_factor = 3.0
        self.original_image = None
        self.original_rect = None
        self.seleted_sprite_index = -1 
        self.select_random_sprite()
        # Establece la primera imagen y su rectángulo
        if self.status in self.animations and self.animations[self.status] and self.seleted_sprite_index >= 0:
            self.map_sprite = self.animations[self.status][self.seleted_sprite_index]
            original_size = self.map_sprite.get_size()
            new_size = (int(original_size[0] * self.scale_factor), int(original_size[1] * self.scale_factor))
            self.image = pygame.transform.scale(self.map_sprite, new_size)

        else:
            self.image = pygame.Surface((32, 32))
            self.image.fill('red')
            print(f"Advertencia: No se encontraron animaciones para el enemigo '{self.name}' en el estado '{self.status}'.")
        

        self.rect = self.image.get_rect(topleft = pos)
        self.original_image = self.image.copy()
        self.original_rect = self.rect.copy()
        # Campo de visión
        self.vision_range = 100
        self.vision_rect = pygame.Rect(self.rect.centerx - self.vision_range, self.rect.centery - self.vision_range, self.vision_range * 2, self.vision_range * 2)
        
        # Atributos de combate
        self.is_in_battle = False
        self._battle_scaled = False

    def import_assets(self):
        # Define la estructura de las animaciones del enemigo y las carga
        full_path = os.path.join(ENEMY_DIR, "map_sprite")
        self.animations = {'idle': []}
        
        if os.path.exists(full_path):
            self.animations['idle'] = import_folder(full_path)
    def select_random_sprite(self):
        if self.status in self.animations and self.animations[self.status]:
            self.seleted_sprite_index = random.randint(0, len(self.animations[self.status])-1)
    
    def get_select_sprite(self):
        if (self.status in self.animations and self.animations[self.status] and self.seleted_sprite_index >= 0 and self.seleted_sprite_index < len(self.animations[self.status])):
            return self.animations[self.status][self.seleted_sprite_index]
        return None

    def check_for_player(self):
        # Actualiza la posición del rectángulo de visión
        self.vision_rect.center = self.rect.center
        
        # Comprueba si el jugador está dentro del campo de visión
        if self.vision_rect.colliderect(self.player.rect):
            self.start_battle()

    def start_battle(self):
        if not self.is_in_battle:
            print(f"¡Un {self.name} salvaje apareció!")
            self.is_in_battle = True
            self.set_battle_scale(True)

    def get_status(self):
        # Sobreescribe el método de la clase padre
        # Aquí puedes añadir lógica para cambiar el estado del enemigo,
        # como 'idle', 'pursuit', 'attack', etc.
        pass

    def set_battle_scale(self, scale=True):
        if scale:
            if not self._battle_scaled:
                self.original_image = self.image.copy()
                self.original_rect = self.rect.copy()

                selected_sprite = self.get_select_sprite()
                if selected_sprite:
                    original_size = selected_sprite.get_size()
                    new_size = (int(original_size[0] * self.battle_scale_factor), int(original_size[1] * self.battle_scale_factor))
                    self.image = pygame.transform.scale(self.original_image, new_size)

                old_center = self.rect.center
                self.rect = self.image.get_rect(center=old_center)
                self._battle_scaled = True
        else:
            if self._battle_scaled:
                self.image = self.original_image.copy()
                old_center = self.rect.center
                self.rect = self.original_rect.copy()
                self.rect.center = old_center
                self._battle_scaled = False

    def update(self):
        # Llama a los métodos para manejar la lógica de la clase
        self.check_for_player()
        if not self.is_in_battle:
            selected_sprite = self.get_select_sprite()
            if selected_sprite:
                original_size = selected_sprite.get_size()
                new_size = (int(original_size[0] * self.scale_factor), int(original_size[1] * self.scale_factor))
                self.image = pygame.transform.scale(selected_sprite, new_size)
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            if not self._battle_scaled:
                self.set_battle_scale(True)
