import pygame, os
from os import walk
from random import uniform
from pygame.math import Vector2 as vector
def import_folder(path):
    surface_list = []
    for _, _, image_files in walk(path):
        for image in image_files:
            full_path = os.path.join(path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

#ESTADOS DE JUEGO
state_of_game = {
    "intro": 0,
    "Game": 1,
    "Pause": 2,
    "Game_over": 3,
    "Exit": 4,
    "battle": 5,
    "Config": 6,
}


ANIMATION_SPEED = 6
#FPS
FPS = 60
#Screen Size
width = 1280
height = 720
#Zoom
default_zoom = 1.0
min_zoom = 0.9
max_zoom = 1.4
zoom_scale_factor = 0.1
# Colores
Blue = (0, 0, 255)
White = (255, 255, 255)
Brown = (139, 69, 19)
Green = (0, 128, 0)
Black = (0, 0, 0)
Grey = (0, 0, 0, 0.3)
Gold = (255, 215, 0)
Orange = (254, 80, 0)

def import_folder(path):
    surface_list = []
    for _, _, image_files in walk(path):
        for image in image_files:
            full_path = os.path.join(path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

#posiciones de combate
Battle_positions = {
    'izq': {'center': (190, 400)},
    'der': {'center': (1110, 390)}
}




