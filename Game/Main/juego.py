import pygame, os, constantes, sys
from Level import Level

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")

class Nombre:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.screen = pygame.display.set_mode((constantes.width, constantes.height))
        pygame.display.set_caption("MONDONGO")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 40)
        # Carga la imagen de fondo una sola vez al inicio
        self.intro_background = pygame.image.load(os.path.join(ASSETS_DIR, 'persona3.jpg'))

    def intro_screen(self):
        intro = True
        title = self.font.render('MONDONGO', True, constantes.Black)
        title_rect = title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))

        play_button = Button(self.screen.get_width() / 2 - 50, self.screen.get_height() / 2, 100, 50, constantes.White, constantes.Black, 'play', 32)
        
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_button.is_pressed(event.pos):
                        intro = False
            # Redimensiona la imagen para que coincida con el tamaño de la pantalla
            scaled_background = pygame.transform.scale(self.intro_background, (constantes.width, constantes.height))
            # Dibuja la imagen redimensionada en la pantalla
            self.screen.blit(scaled_background, (0, 0))

            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            
            pygame.display.update()
            self.clock.tick(constantes.FPS)

    def run_game(self):
        self.level = Level()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            self.screen.fill(constantes.Black)
            self.level.run()
            pygame.display.update()
            self.clock.tick(constantes.FPS)

    def run(self):
        self.intro_screen()
        if self.running:
            self.run_game()

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font(None, fontsize)
        self.content = content
        self.image = pygame.Surface((width, height))
        self.image.fill(bg)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = self.font.render(self.content, True, fg)
        self.text_rect = self.text.get_rect(center=(width/2, height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)

if __name__ == "__main__":
    game = Nombre()
    game.run()