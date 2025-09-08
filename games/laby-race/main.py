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
TIME = 50  # Durée en secondes de l'animation
TOTAL_FRAMES = TIME * FPS
BASE_FILENAME = "laby-race"
DIR_OUTPUT = "laby-race"

# LABYRINTHE
MAZE_WIDTH, MAZE_HEIGHT = 7, 7  # Dimensions du labyrinthe
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


def generate_maze(width, height):
    # Maze generation with DFS on a grid with walls
    maze_h, maze_w = height * 2 + 1, width * 2 + 1
    maze = np.zeros((maze_h, maze_w), dtype=int)
    maze[1::2, 1::2] = 1  # Set cells as open
    visited = np.zeros((height, width), dtype=bool)
    stack = []

    def neighbors(cx, cy):
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        result = []
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny, nx]:
                result.append((nx, ny))
        np.random.shuffle(result)
        return result
    
    x, y = 0, 0
    stack.append((x, y))
    visited[y, x] = True

    while stack:
        cx, cy = stack[-1]
        nbs = neighbors(cx, cy)
        if nbs:
            nx, ny = nbs[0]
            # Remove wall between (cx,cy) and (nx,ny)
            maze[cy*2+1 + (ny-cy), cx*2+1 + (nx-cx)] = 1
            visited[ny, nx] = True
            stack.append((nx, ny))
        else:
            stack.pop()

    # BFS pour trouver la cellule la plus éloignée de l'entrée
    from collections import deque
    start = (1, 1)  # (y, x) pour l'entrée
    visited_bfs = np.zeros_like(maze, dtype=bool)
    queue = deque()
    queue.append((start[0], start[1], 0))
    visited_bfs[start[0], start[1]] = True
    farthest = start
    max_dist = 0
    while queue:
        cy, cx, dist = queue.popleft()
        if dist > max_dist:
            max_dist = dist
            farthest = (cy, cx)
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < maze.shape[0] and 0 <= nx < maze.shape[1]:
                if not visited_bfs[ny, nx] and maze[ny, nx] == 1:
                    visited_bfs[ny, nx] = True
                    queue.append((ny, nx, dist+1))

    entry_pos = start
    exit_pos = farthest
    maze[entry_pos] = 2  # 2 = entrée
    maze[exit_pos] = 3   # 3 = sortie
    return maze, entry_pos, exit_pos



if __name__ == "__main__":
    
    support = init_pygame() 
    # Création du répertoire pour les frames
    if not os.path.exists("Frames"):
        os.makedirs("Frames")
        
    # variables de l'animation

    maze, entry, exit = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    maze_h, maze_w = maze.shape
    cell_draw_size = max(1, int(CELL_SIZE // 2))
    offset_x = int((WIDTH - maze_w * cell_draw_size) // 2)
    offset_y = int((HEIGHT - maze_h * cell_draw_size) // 2)

    
    
    for frame in range(TOTAL_FRAMES):  # -3*FPS pour laisser du temps à la fin
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for y in range(maze_h):
            for x in range(maze_w):
                rect = pygame.Rect(
                    offset_x + x * cell_draw_size,
                    offset_y + y * cell_draw_size,
                    cell_draw_size,
                    cell_draw_size
                )
                if maze[y, x] == 2:
                    color = (0, 255, 0)  # Entrée en vert
                elif maze[y, x] == 3:
                    color = (255, 0, 0)  # Sortie en rouge
                elif maze[y, x] == 1:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)
                pygame.draw.rect(support, color, rect)

        if SHOW_WINDOW:
            pygame.display.flip()
            
        support.fill((0, 0, 0))
            
            
            
            
        saveFrame(RECORDING, frame, support, BASE_FILENAME, TIME, FPS)
    
    
    
    pygame.quit()
    
    if RECORDING:
        createMovieFromFrame(TOTAL_FRAMES, BASE_FILENAME, DIR_OUTPUT, FPS)