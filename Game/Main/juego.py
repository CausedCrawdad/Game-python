import pygame, os, constantes, sys, random
from Level import Level
from Battle import battle
from constantes import import_folder

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")
MUSIC_DIR = os.path.join(ASSETS_DIR, "Music")

class Nombre:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.random = random.randint(1,10000)
        self.mixer_initialized = False
        try:
            pygame.mixer.init()
            self.mixer_initialized = True
        except pygame.error:
            print("no se encontro un dispositivo de audio")
                
        self.music_position = 0
        self.screen = pygame.display.set_mode((constantes.width, constantes.height))
        pygame.display.set_caption("David Story")
        self.clock = pygame.time.Clock()
        self.estado_actual = constantes.state_of_game["intro"]
        self.font = pygame.font.Font(None, 40)
        self.dt = 0
        self.intro_background = pygame.image.load(os.path.join(ASSETS_DIR, 'persona3.jpg'))
        if self.random == 7463:
            self.intro_background = pygame.image.load(os.path.join(ASSETS_DIR, "solid.jpeg"))
        elif self.random == 5482: 
            self.intro_background = pygame.image.load(os.path.join(ASSETS_DIR, "ultrakill.jpeg"))
        elif self.random == 7784:  
            self.intro_background = pygame.image.load(os.path.join(ASSETS_DIR, "PERSONA.jpg"))
        self.level = None
        self.battle_instance = None
        self.enemy_frames = None
        self.bs_surf = None
        self.fonts = None

    def intro_screen(self):
        title = self.font.render('David Story', True, constantes.Black)
        title_rect = title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))
        play_button = Button(self.screen.get_width() / 2 - 50, self.screen.get_height() / 2, 100, 50, constantes.White, constantes.Black, 'play', 32)
        try:
            self.musica_de_Fondo = pygame.mixer.music.load(os.path.join(MUSIC_DIR, "no, no es undertale.mp3"))
            pygame.mixer.music.play(loops=-1, fade_ms=7000)
        except:
            print("no se encontro la musica")
        if self.random == 7463:
            title = self.font.render('Metal Gear Solid', True, constantes.Black)
            title_rect = title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))
            pygame.mixer.music.pause()
            self.musica_random = pygame.mixer.music.load(os.path.join(MUSIC_DIR,"solid.mp3"))
            pygame.mixer.music.play(loops=-1, fade_ms=7000)
        elif self.random == 5482:
            title = self.font.render('Ultrakill', True, constantes.Black)
            title_rect = title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))
            pygame.mixer.music.pause()
            self.music_random2 = pygame.mixer.music.load(os.path.join(MUSIC_DIR, "ultrakill.mp3"))
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(loops=-1, fade_ms=7000)
        elif self.random == 7784:
            title = self.font.render("PERSONA", True, constantes.Black)
            title_rect = title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))
            pygame.mixer.music.pause()
            self.music_random3 = pygame.mixer.music.load(os.path.join(MUSIC_DIR, "PERSONA.mp3"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(loops=-1,fade_ms=7000)

        while self.estado_actual == constantes.state_of_game["intro"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.estado_actual = constantes.state_of_game["Exit"]
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_button.is_pressed(event.pos):
                        self.estado_actual = constantes.state_of_game["Game"]

            scaled_background = pygame.transform.scale(self.intro_background, (constantes.width, constantes.height))
            self.screen.blit(scaled_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            
            pygame.display.update()
            self.clock.tick(constantes.FPS)
    
    def pause_menu(self):
        overlay = pygame.Surface((constantes.width, constantes.height), pygame.SRCALPHA)
        overlay.fill(constantes.Grey)
        self.screen.blit(overlay,(0,0))
        
        resume_buttom = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 - 80, 200, 50,constantes.White, constantes.Black, 'Resume', 28 )
        menu_buttom = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2, 200, 50, constantes.White, constantes.Black, "Menu Principal", 28 )
        exit_buttom = Button(self.screen.get_width()/ 2 - 100, self.screen.get_height() / 2 + 80, 200, 50, constantes.White,constantes.Black , "Exit", 28 )
    
        title = self.font.render("Game Paused", True, constantes.Orange)
        title_rect = title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))
        while self.estado_actual == constantes.state_of_game["Pause"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.estado_actual = constantes.state_of_game["Exit"]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.estado_actual = constantes.state_of_game["Game"]
                        pygame.mixer.music.set_volume(1.0)
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if resume_buttom.is_pressed(event.pos):
                        self.estado_actual = constantes.state_of_game["Game"]
                        pygame.mixer_music.set_volume(1.0)
                        return
                    elif menu_buttom.is_pressed(event.pos):
                        self.estado_actual = constantes.state_of_game["intro"]
                    elif exit_buttom.is_pressed(event.pos):
                        self.estado_actual = constantes.state_of_game["Exit"] 
                        return
            
            self.screen.blit(title, title_rect)
            self.screen.blit(resume_buttom.image, resume_buttom.rect)
            self.screen.blit(menu_buttom.image, menu_buttom.rect)
            self.screen.blit(exit_buttom.image, exit_buttom.rect)

            pygame.display.update()
            self.clock.tick(constantes.FPS)
    
    def run_battle(self):
        if self.battle_instance:
        
            if self.mixer_initialized:
                pygame.mixer.music.pause()

                try:
                    is_boss_battle = hasattr(self.battle_instance.battle_data['enemy'], 'is_boss') and self.battle_instance.battle_data['enemy'].is_boss
                    if is_boss_battle:
                        battle_music = pygame.mixer.Sound(os.path.join(MUSIC_DIR,"perfect.mp3"))
                    else:
                        battle_music = pygame.mixer.Sound(os.path.join(MUSIC_DIR, "The Hammer.mp3"))
                    battle_music.set_volume(0.5)
                    chanel = battle_music.play(loops=-1, fade_ms=6000)
                except:
                    print("No se encontro la musica")
        
            self.battle_instance.run()
            result = self.battle_instance.battle_result
            
            if self.mixer_initialized:
                pygame.mixer.music.unpause()
                try:
                    battle_music.stop()
                except:
                    pass
            return result
        return None
        
    def load_sprites_battle(self):

        enemy_path = os.path.join(ASSETS_DIR, "Enemies", "map_sprite")
        self.enemy_frames = import_folder(enemy_path)
        
        boss_path = os.path.join(ASSETS_DIR, "Enemies", "boss")
        if os.path.exists(boss_path):
            self.boss_frame = import_folder(boss_path)


        self.bs_surf = pygame.image.load(os.path.join(ASSETS_DIR, "background_bt.png")).convert_alpha()

        self.fonts = {
                'default': pygame.font.Font(None, 36),
                'title': pygame.font.Font(None, 42)
        }

    def run_game(self):
        if self.level is None:
            self.level = Level()
        
        if self.enemy_frames is None:
            self.load_sprites_battle()
        
        if self.mixer_initialized:
            try:
                pygame.mixer.music.pause()
                self.musica_de_juego = pygame.mixer.music.load(os.path.join(MUSIC_DIR, "No es undertale.mp3"))
                pygame.mixer.music.play(loops=-1, fade_ms=6000)
            except pygame.error:
                print("Error al cargar o reproducir música.")

        while self.estado_actual == constantes.state_of_game["Game"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.estado_actual = constantes.state_of_game["Exit"]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.mixer_initialized:
                            pygame.mixer.music.set_volume(0.2)
                        self.estado_actual = constantes.state_of_game["Pause"]
                        self.pause_menu()
                        continue
            
            enemy_triggered = self.level.run()

            if enemy_triggered:
                self.estado_actual = constantes.state_of_game["battle"]
                self.battle_instance = battle(self.level.Player, enemy_triggered, self.enemy_frames, self.bs_surf, self.fonts)
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
            elif self.estado_actual == constantes.state_of_game["battle"]:
                battle_result = self.run_battle()        
                if battle_result == "Derrota":
                    self.estado_actual = constantes.state_of_game["Exit"]
                elif battle_result == "Victoria" or "Escape":
                    self.estado_actual = constantes.state_of_game["Game"]
                    if self.mixer_initialized:
                        try:
                            pygame.mixer.music.unpause()
                        except:
                            pass
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
