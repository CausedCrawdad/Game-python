import pygame
import constantes
import sys
from Level import Level


# Inicio del juego y eventos
class Nombre:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("iiii te chinge")
        self.level = Level()
    
    def run_the_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(constantes.Black)
            self.level.run()
            pygame.display.update()


if __name__ == "__main__":
    Nombre_preliminar = Nombre()
    Nombre_preliminar.run_the_game()
