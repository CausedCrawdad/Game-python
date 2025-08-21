import pygame, os, maps

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")
PLAYER_DIR = os.path.join(ASSETS_DIR, "Player")

#imports the character sprite and manages its vector and velocity
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)

        self.image = pygame.image.load(os.path.join(PLAYER_DIR, "davidatras1.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direccion = pygame.math.Vector2()
        self.velocidad = 2
        
        self.Obstacles = obstacles
 #detects which key is being pressed to make the character move
    def Keybord(self):
        keys = pygame.key.get_pressed()
       
        if keys[pygame.K_UP]:
            self.direccion.y = -1
        elif keys[pygame.K_DOWN]:
            self.direccion.y = 1
        elif keys[pygame.K_w]:
            self.direccion.y = -1
        elif keys[pygame.K_s]:
            self.direccion.y = 1
        else:
            self.direccion.y = 0 

        if  keys[pygame.K_LEFT]:
            self.direccion.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direccion.x = 1
        elif keys[pygame.K_a]:
            self.direccion.x = -1
        elif keys[pygame.K_d]:
            self.direccion.x = 1
        else:
            self.direccion.x = 0
    def move(self, velocidad):
        if self.direccion.magnitude() != 0:
            self.direccion = self.direccion.normalize()
        
        self.rect.x  += self.direccion.x *  velocidad
        self.colisions("horizontal")
        
        self.rect.y += self.direccion.y * velocidad
        self.colisions("vertical")

    def colisions(self, direccion):
        if direccion == ("horizontal"):
            for sprite in self.Obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direccion.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direccion.x < 0:
                        self.rect.left = sprite.rect.right
        1
        if direccion == ("vertical"):
            for sprite in self.Obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direccion.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direccion.y < 0:
                        self.rect.top = sprite.rect.bottom
    
    def update(self):
        self.Keybord()
        self.move(self.velocidad)
    
