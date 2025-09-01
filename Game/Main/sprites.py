import pygame
from constantes import ANIMATION_SPEED

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = ANIMATION_SPEED
        self.status = 'down' # Estado inicial predeterminado
        self.obstacles = obstacles
        self.animations = {} # Un diccionario para las animaciones

    def get_status(self):
        pass

    def animate(self):
        # 1. Obtener la lista de animaciones para el estado actua
        
        animation = self.animations.get(self.status)

        # 2. Verificar si la animación existe y no está vacía
        if animation is None or not animation:
            # Si no hay animación, el método termina para evitar el IndexError
            return

        # 3. Animar normalmente
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def update(self):
        self.get_status()
        self.animate()
