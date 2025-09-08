import pygame
import sys
import numpy as np
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Recording.Recording import createMovieFromFrame, saveFrame


#### CONSTANTES

# DEBUG
SHOW_WINDOW = True  # True pour afficher la fenêtre Pygame, False pour ne pas l'afficher
RECORDING = False  # True pour enregistrer les frames, False pour ne pas enregistrer

# GENERIQUE
WIDTH, HEIGHT =1080/2, 1920/3
FPS = 60
TIME = 5  # Durée en secondes de l'animation
TOTAL_FRAMES = TIME * FPS
BASE_FILENAME = "laby-race"
DIR_OUTPUT = "laby-race"

# LABYRINTHE
MAZE_WIDTH, MAZE_HEIGHT = 10, 10  # Dimensions du labyrinthe
CELL_SIZE = (WIDTH) // MAZE_WIDTH  # Taille d'une cellule en pixel
LABY_POS = (HEIGHT - MAZE_HEIGHT * CELL_SIZE) // 2


# Initialisation de Pygame sans fenêtre visible
def init_pygame():
    if SHOW_WINDOW:
        pygame.init()
        support = pygame.display.set_mode((WIDTH, HEIGHT))
    else:
        # Pour éviter l'affichage d'une fenêtre
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        support = pygame.Surface((WIDTH, HEIGHT))  # Pas de fenêtre, juste une surface
    pygame.display.set_caption("laby-race")
    return support

if __name__ == "__main__":
    
    support = init_pygame() 
    # Création du répertoire pour les frames
    if not os.path.exists("Frames"):
        os.makedirs("Frames")
        
    # variables de l'animation

    for frame in range(TOTAL_FRAMES):  # -3*FPS pour laisser du temps à la fin
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # pygame.draw.rect(support, (255, 255, 255), (0, LABY_POS, MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE))
        
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                rect = pygame.Rect(
                    x * CELL_SIZE,
                    LABY_POS + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(support, (255, 255, 255), rect, 1)

        if SHOW_WINDOW:
            pygame.display.flip()
            
        support.fill((0, 0, 0))
            
            
            
            
        saveFrame(RECORDING, frame, support, BASE_FILENAME, TIME, FPS)
    
    
    
    pygame.quit()
    
    if RECORDING:
        createMovieFromFrame(TOTAL_FRAMES, BASE_FILENAME, DIR_OUTPUT, FPS)