import pygame, os
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
        
        # Establece la primera imagen y su rectángulo
        if self.status in self.animations and self.animations[self.status]:
            self.image = self.animations[self.status][0]
        else:
            self.image = pygame.Surface((32, 32))
            self.image.fill('red')
            print(f"Advertencia: No se encontraron animaciones para el enemigo '{self.name}' en el estado '{self.status}'.")

        self.rect = self.image.get_rect(topleft = pos)

        # Campo de visión
        self.vision_range = 150
        self.vision_rect = pygame.Rect(self.rect.centerx - self.vision_range, self.rect.centery - self.vision_range, self.vision_range * 2, self.vision_range * 2)
        
        # Atributos de combate
        self.is_in_battle = False
    
    def import_assets(self):
        # Define la estructura de las animaciones del enemigo y las carga
        enemy_path = os.path.join(ENEMY_DIR, self.name)
        self.animations = {'idle': []}
        
        full_path = os.path.join(enemy_path, 'idle')
        if os.path.exists(full_path):
            self.animations['idle'] = import_folder(full_path)
    
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

    def get_status(self):
        # Sobreescribe el método de la clase padre
        # Aquí puedes añadir lógica para cambiar el estado del enemigo,
        # como 'idle', 'pursuit', 'attack', etc.
        pass

    def update(self):
        # Llama a los métodos para manejar la lógica de la clase
        self.check_for_player()
        
        # Llama al método de animación de la clase padre (Entity)
        self.animate()