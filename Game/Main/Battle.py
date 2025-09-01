import pygame, sys, constantes, math, random
# Importa ahora las clases Player y Enemy directamente, ya que heredan de Sprite
from Player import Player 
from enemy import Enemy
from constantes import *

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "Assets")
PLAYER_DIR = os.path.join(ASSETS_DIR, "Player")

class Battle_Options:
    def __init__(self,text,position, size, fonts):
        self.text = text
        self.position = position
        self.size = size
        self.font = fonts['default']
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.is_selected = False
        self.normal_color = (100, 100, 100, 100)
        self.selected_color = (200, 200, 0, 220)
        self.text_color = White
    
    def draw(self, surface):
        
        option_surface = pygame.Surface(self.size, pygame.SRCALPHA)

        color = self.selected_color if self.is_selected else self.normal_color
        pygame.draw.rect(option_surface, color,(0, 0, self.size[0], self.size[1]), border_radius=10)
        pygame.draw.rect(option_surface, Black,(0, 0, self.size[0], self.size[1]), 2, border_radius=10)


        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.size[0]//2, self.size[1]//2 ))
        option_surface.blit(text_surf, text_rect)

        surface.blit(option_surface, self.position)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

class battle:
    def __init__(self, player, enemy, enemy_frames, bg_surf, fonts):
        self.display_surface = pygame.display.get_surface()
        self.bg_surf = bg_surf
        self.enemy_frames = enemy_frames
        self.battle_data = {'player': player, 'enemy': enemy}
        self.battle_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.fonts = fonts
        self.setup()
        self.running = True
        player.set_battle_state(True)
        self.battle_options = []
        self.option_radius = 120
        self.selected_option = None
        self.setup_battle_options()
        self.clock = pygame.time.Clock() 
        self.battle_state = "selection"
        self.player_choice = None
        self.enemy_choice = None
        self.battle_result = None
        self.result_timer = 0
        self.result_duration = 2000
        self.player_lives = 3 
        self.enemy_lives = 3
        self.life_icon = self.battle_data["player"].battle_sprite
        self.life_icon = pygame.transform.scale(self.life_icon, (48,48))
        
        self.defeat_animation = []
        self.defeat_animation_path = os.path.join(ASSETS_DIR, "Game Over")
        self.load_defeat_animation()
        self.defeat_animation_index = 0 
        self.defeat_animation_speed = 0.7
        self.defeat_animation_timer = 0
        self.show_defeat_animation = False

    def load_defeat_animation(self):
        if os.path.exists(self.defeat_animation_path):
            try:
                image_files = []
                for _, _, files in os.walk(self.defeat_animation_path):
                    for image in files:
                        if image.lower().endswith(('.png','.jpg','.jpeg', 'bmp')):
                            image_files.append(image)
                image_files.sort()

                self.defeat_animation = []
                for image_files in image_files:
                    full_path = os.path.join(self.defeat_animation_path, image_files)
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    self.defeat_animation.append(image_surf)

            except Exception as e:
                self.create_fallback_animation()
        else:
            self.create_fallback_animation()
    def create_fallback_animation(self):
        for i in range(5):
            surf = pygame.Surface((200, 200),pygame.SRCALPHA)
            color = (255, 0, 0, 200 - i * 40)
            pygame.draw.circle(surf,color,(100,100), 80 - i * 15)
            text = self.fonts['default'].render("GAME OVER", True, White)
            text_rect = text.get_rect(center=(100,100))
            surf.blit(text,text_rect)
            self.defeat_animation.append(surf)

    def update_defeat_animation(self, dt):
        if not self.show_defeat_animation or not self.defeat_animation:
            return
        if self.defeat_animation_index < len(self.defeat_animation) - 1:
            
            self.defeat_animation_timer += dt * 1000 
            if self.defeat_animation_timer >= 200:
                self.defeat_animation_timer = 0
                self.defeat_animation_index += self.defeat_animation_speed

            if self.defeat_animation_index >= len(self.defeat_animation) - 1:
                self.defeat_animation_index = len(self.defeat_animation) - 1

    def draw_defeat_animation(self):
        if not self.show_defeat_animation or not self.defeat_animation:
            return
        denug_text = self.fonts['default'].render(f"Frame:{int(self.defeat_animation_index)}/{len(self.defeat_animation)-1}",True, White)
        self.display_surface.blit(denug_text,(10,10))
        overlay = pygame.Surface((constantes.width, constantes.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.display_surface.blit(overlay,(0, 0))

        
        current_frame = self.defeat_animation[int(self.defeat_animation_index)]
        frame_rect = current_frame.get_rect(center=(width // 2, height // 2))
        self.display_surface.blit(current_frame, frame_rect)
    
        if self.defeat_animation_index >= len(self.defeat_animation) - 1:
            continue_text = self.fonts["default"].render("Presiona ESC para continuar", True, White)
            self.display_surface.blit(continue_text,(width // 2 - continue_text.get_width() // 2, 100))
    def setup(self):
        # Aquí el código ya no crea nuevos sprites
        # Simplemente los añade a los grupos para que se dibujen
        self.battle_data["player"].in_battle = True
        
        self.battle_data["player"].set_battle_state(True)
        pos = Battle_positions['izq']['center']
        self.battle_data['player'].rect.center = pos
        self.battle_sprites.add(self.battle_data['player'])
                
        pos = Battle_positions['der']['center']
        self.battle_data['enemy'].rect.center = pos
        self.battle_data["enemy"].set_battle_scale(True)
        self.battle_sprites.add(self.battle_data['enemy'])
    
    def setup_battle_options(self):
        options_width = 120
        options_heigth = 40
        player_center = self.battle_data["player"].rect.center
        
        options = ["Tijeras", "Piedra", "Papel"]
        
        for i, options_text in enumerate(options):
            angle = 2 * math.pi * i / len(options) - math.pi / 2
            x = player_center[0] + self.option_radius * math.cos(angle) - options_width / 2
            y = player_center[1] + self.option_radius * math.sin(angle) - options_heigth / 2 

            option = Battle_Options(options_text, (x, y), (options_width, options_heigth), self.fonts)

            self.battle_options.append(option)

    def handle_player_movement(self):
        if self.battle_state != "selection":
            return
        
        keys = pygame.key.get_pressed()
        player = self.battle_data["player"]
        speed = 4
        
        old_x, old_y = player.rect.x, player.rect.y
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.rect.x -= speed
            player.status = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.rect.x += speed
            player.status = "right"
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            player.rect.y -= speed
            player.status = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.rect.y += speed
            player.status = "down"

        min_x = 50 
        max_x = width - 900 - player.rect.width
        min_y = 200 
        max_y = height - 150 - player.rect.height

        player.rect.x = max(min_x, min(player.rect.x, max_x))
        player.rect.y = max(min_y, min(player.rect.y, max_y))

        self.check_options_collisions()
        
    def check_options_collisions(self):
        player = self.battle_data["player"]
        self.selected_option = None

        for option in self.battle_options:
            if option.check_collision(player.rect):
                option.is_selected = True
                self.selected_option = option
            else:
                 option.is_selected = False
    def handle_selection(self):
        if self.battle_state != "selection" or not self.selected_option:
            return
        
        option_text = self.selected_option.text
        self.player_choice = option_text
        self.enemy_choice = self.get_enemy_choice()

        self.determine_battle_result()
        
        self.battle_state = "result"
        self.result_timer = pygame.time.get_ticks()

    def get_enemy_choice(self):
        options = ["Tijeras", "Piedra", "Papel"]
        return random.choice(options)

    def determine_battle_result(self):
        if self.player_choice == self.enemy_choice:
            self.battle_result = "empate"
        elif(self.player_choice == "Piedra" and self.enemy_choice == "Tijeras") or (self.player_choice == "Papel" and self.enemy_choice == "Piedra") or (self.player_choice == "Tijeras" and self.enemy_choice == "Papel"):
            self.battle_result = "Victoria"
            self.enemy_lives -= 1
        else:
            self.battle_result = "Derrota"
            self.player_lives -= 1
            if self.player_lives <= 0:
                self.show_defeat_animation = True
                self.defeat_animation_index = 0
                self.defeat_animation_timer = 0

    def execute_Tijeras(self):
        self.player_choice = "Tijeras"
        self.handle_selection()
    def execute_Piedra(self):
        self.player_choice = "Piedra"
        self.handle_selection()
    def execute_Papel(self):
        self.player_choice = "Papel"
        self.handle_selection()
    
    def draw_battle_info(self):
        info_font = self.fonts["default"]
        if self.battle_state == "selection":
            text = info_font.render("Elige Tu Accion", True, White)
            
            self.display_surface.blit(text,(width // 2 - text.get_width() // 2, 50))
        elif self.battle_state == "result":
            player_text = info_font.render(f"Jugador:{self.player_choice}", True, White)
            enemy_text = info_font.render(f"Enemigo:{self.enemy_choice}",True, White)

            self.display_surface.blit(player_text,(width // 4 - player_text.get_width()//2 , 50))
            self.display_surface.blit(enemy_text,(3 * width // 4 - enemy_text.get_width()//2, 50 ))

            if self.battle_result == "Victoria":
                result_text = info_font.render("Victoria", True, Orange)

            elif self.battle_result == "Derrota":
                result_text = info_font.render("Derrota", True, Blue)
            else:
                result_text = info_font.render("Empate",True, White)
            
            self.display_surface.blit(result_text,(width // 2 - result_text.get_width() // 2, 100))

        elif self.battle_state == "end":
            if self.battle_result == "Victoria":
                end_text = info_font.render("Has Ganado La Batalla", True, Orange)
            else:
                end_text = info_font.render("Has Perdido La Batalla", True, Blue)
            
            self.display_surface.blit(end_text,(width // 2 - end_text.get_width() // 2, 50))
            continue_text = info_font.render("Presiona ESPACIO para continuar", True, White)
            self.display_surface.blit(continue_text, (width // 2 - continue_text.get_width() // 2, 100))
    def draw_lives(self):
        enemy_lives_icon = self.life_icon.copy()
        enemy_lives_icon.fill(White, special_flags=pygame.BLEND_RGB_MAX)
        papel_pos = None
        piedra_pos = None
        
        enemy_name = self.fonts["default"].render("Dragon", True, White)
        self.display_surface.blit(enemy_name,(width - 320 + 120,220 ))

        for option in self.battle_options:
            if option.text == "Papel":
                papel_pos = option.rect.center

            elif option.text == "Piedra":
                piedra_pos = option.rect.center

        if papel_pos and piedra_pos:
            lives_x = (papel_pos[0] + piedra_pos[0]) // 2 - 85
            lives_y = (papel_pos[1] + piedra_pos[1]) // 2 + 50

            for i in range(self.player_lives):
                self.display_surface.blit(self.life_icon, (lives_x + 40 + i * 25, lives_y - 10))
            
        for i in range(self.enemy_lives):
            self.display_surface.blit(enemy_lives_icon,(width - 330 + 120 + i * 25, 250))

    def update_battle_state(self):
        if self.battle_state == "result":
            current_time = pygame.time.get_ticks()
            if current_time - self.result_timer > self.result_duration:
                if self.player_lives <= 0 or self.enemy_lives <= 0:
                    self.battle_state = "end"
                    if self.player_lives <= 0:
                        self.battle_result = "Derrota"
                    else:
                        self.battle_result = "Victoria"
                else:
                    self.battle_state = "selection"

    def handle_battle_end(self):
        keys = pygame.key.get_pressed()
        
        can_exit = not self.show_defeat_animation or self.defeat_animation_index >= len(self.defeat_animation) - 1

        if (keys[pygame.K_SPACE] and can_exit) or (self.defeat_animation and can_exit and self.defeat_animation_index >= len(self.defeat_animation) -1):

            self.running = False
            
            if self.battle_result == "Victoria":
                self.battle_data["enemy"].kill()
                self.battle_data["enemy"].is_eliminated = True
                self.battle_data["enemy"].is_in_battle = False
            else:
                pass

            self.battle_data["player"].set_battle_state(False)
            self.battle_data["enemy"].set_battle_scale(False)
            self.battle_data["enemy"].is_in_battle = False

    def update(self, dt):
        scale_bg = pygame.transform.scale(self.bg_surf, (constantes.width, constantes.height))
        self.display_surface.blit(scale_bg, (0, 0))
        
        self.update_defeat_animation(dt)
        if not self.show_defeat_animation:
            if self.battle_state == "selection":
                for option in self.battle_options:
                    option.draw(self.display_surface)
            self.battle_sprites.update()
            self.battle_sprites.draw(self.display_surface)
            self.draw_lives()
            self.draw_battle_info()
            self.update_battle_state()

        if self.battle_state == "end":

            self.handle_battle_end()
        
        self.draw_defeat_animation()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        self.battle_data["player"].set_battle_state(False)
                        self.battle_data["enemy"].set_battle_scale(False)
                        self.battle_data["enemy"].is_in_battle = False
                        self.running = False
                        return "Escape"
                    if event.key == pygame.K_SPACE and self.battle_state == "selection":
                        self.handle_selection()
                    if event.key == pygame.K_SPACE  and self.battle_state == "end":
                        self.handle_battle_end()
            self.handle_player_movement()
            self.update(dt)
            pygame.display.flip()

        self.battle_data["player"].set_battle_state(False)
        self.battle_data["enemy"].set_battle_scale(False)
        self.battle_data["enemy"].is_in_battle = False
        return self.battle_result
