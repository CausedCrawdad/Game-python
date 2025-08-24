import pygame, os
from os import walk

def import_folder(path):
    surface_list = []
    for _, _, image_files in walk(path):
        for image in image_files:
            full_path = os.path.join(path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list



#FPS
FPS = 1200
#Screen Size
width = 1280
height = 720
#Zoom
default_zoom = 1.0
min_zoom = 0.8
max_zoom = 2.0
zoom_scale_factor = 0.1
# Colores
Blue = (0, 0, 255)
White = (255, 255, 255)
Brown = (139, 69, 19)
Green = (0, 128, 0)
Black = (0, 0, 0)