import pygame, os, constantes, sys
from Level import Level

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")
MUSIC_DIR = os.path.join(ASSETS_DIR, "Music")

class Nombre:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((constantes.width, constantes.height))
        pygame.display.set_caption("MONDONGO")
        self.clock = pygame.time.Clock()
        self.estado_actual = constantes.state_of_game["intro"]
        self.font = pygame.font.Font(None, 40)
        self.dt = 0
        # Carga la imagen de fondo una sola vez al inicio
        self.intro_background = pygame.image.load(os.path.join(ASSETS_DIR, 'persona3.jpg'))
        self.level = None
    
    def intro_screen(self):
        title = self.font.render('Risk Of Rain 2', True, constantes.Black)
        title_rect = title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))
        play_button = Button(self.screen.get_width() / 2 - 50, self.screen.get_height() / 2, 100, 50, constantes.White, constantes.Black, 'play', 32)
        try:
            self.musica_de_Fondo = pygame.mixer.music.load(os.path.join(MUSIC_DIR, "no, no es undertale.mp3"))
            pygame.mixer.music.play(loops=-1, fade_ms=7000)
        except:
            print("no se encontro la musica")
        while self.estado_actual == constantes.state_of_game["intro"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.estado_actual = constantes.state_of_game["Exit"]
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_button.is_pressed(event.pos):
                        self.estado_actual = constantes.state_of_game["Game"]

            # Redimensiona la imagen para que coincida con el tamaño de la pantalla
            scaled_background = pygame.transform.scale(self.intro_background, (constantes.width, constantes.height))
            # Dibuja la imagen redimensionada en la pantalla
            self.screen.blit(scaled_background, (0, 0))

            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            
            pygame.display.update()
            self.clock.tick(constantes.FPS)
    
    def pause_menu(self):
        overlay = pygame.Surface((constantes.width, constantes.height), pygame.SRCALPHA)
        overlay.fill(constantes.Grey)
        self.screen.blit(overlay,(0,0))
        
        resume_buttom = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 - 80, 200, 50,constantes.White, constantes.Green, 'Resume', 32 )
        menu_buttom = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2, 200, 50, constantes.White, constantes.Blue, "Menu Principal", 32 )
        exit_buttom = Button(self.screen.get_width()/ 2 - 100, self.screen.get_height() / 2 + 80, 200, 50, constantes.White, constantes.Blue, "Exit", 32 )
    
        title = self.font.render("Game Paused", True, constantes.Gold)
        title_rect = title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))
         
        pygame.mixer.music.pause()        
        try: 
            music_pause = pygame.mixer.music.load(os.path.join(MUSIC_DIR, ""))
        except:
            print("no se encontro la musica")
        while self.estado_actual == constantes.state_of_game["Pause"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.estado_actual = constantes.state_of_game["Exit"]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.estado_actual = constantes.state_of_game["Game"]
                        pygame.mixer.music.unpause()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if resume_buttom.is_pressed(event.pos):
                        self.estado_actual = constantes.state_of_game["Game"]
                        pygame.mixer_music.unpause()
                    elif menu_buttom.is_pressed(event.pos):
                        self.estado_actual = constantes.state_of_game["intro"]
                        if self.level:
                            self.level = None
                    elif exit_buttom.is_pressed(event.pos):
                        self.estado_actual = constantes.state_of_game["Exit"] 
       
            self.screen.blit(title, title_rect)
            self.screen.blit(resume_buttom.image, resume_buttom.rect)
            self.screen.blit(menu_buttom.image, menu_buttom.rect)
            self.screen.blit(exit_buttom.image, exit_buttom.rect)

            pygame.display.update()
            self.clock.tick(constantes.FPS)

    def run_game(self):
        if  not self.level:
            self.level = Level()
            pygame.mixer.music.pause()
            self.musica_de_juego = pygame.mixer.music.load(os.path.join(MUSIC_DIR, "No es undertale.mp3"))
            pygame.mixer.music.play(loops=-1, fade_ms=6000)

        while self.estado_actual == constantes.state_of_game["Game"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.estado_actual = constantes.state_of_game["Exit"]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.pause()
                        self.estado_actual = constantes.state_of_game["Pause"]
                        self.pause_menu()
                        continue
            
            self.screen.fill(constantes.Black)
            self.level.run()
            pygame.display.update()
            self.dt = self.clock.tick(constantes.FPS) / 1000

    def run(self):
        while self.estado_actual != constantes.state_of_game["Exit"]:
            if self.estado_actual == constantes.state_of_game["intro"]:
                self.intro_screen()
            elif self.estado_actual == constantes.state_of_game["Game"]:
                self.run_game()
            elif self.estado_actual == constantes.state_of_game["Pause"]:
                self.pause_menu()        
    
        pygame.quit()
        sys.exit()

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font(None, fontsize)
        self.content = content
        self.width = width
        self.height = height
        self.x = x 
        self.y = y 
        self.fg = fg
        self.fg = fg
        self.bg = bg
        self.hover_bg = (min(bg[0] + 30, 255), min(bg[1] + 30, 255), min(bg[2] + 30, 255))
        self.image = pygame.Surface((width, height))
        self.image.fill(bg)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = self.font.render(self.content, True, fg)
        self.text_rect = self.text.get_rect(center=(width/2, height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)
    
    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.image.fill(self.hover_bg)
        else:
            self.image.fill(self.bg)
        

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height/ 2 ))
        self.image.blit(self.text, self.text_rect)

if __name__ == "__main__":
    game = Nombre()
    game.run()
