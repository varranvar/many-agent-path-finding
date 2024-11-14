import pygame 
from grid import Grid

GRID_WIDTH = 10
GRID_HEIGHT = 10
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

pygame.init() 
canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Many Agent Path Finding") 
exit = False
  
grid = Grid(GRID_WIDTH, GRID_HEIGHT)
  
while not exit: 
    canvas.fill((0, 0, 0))
    
    rw = SCREEN_WIDTH / GRID_WIDTH
    rh = SCREEN_HEIGHT / GRID_HEIGHT
    
    print()
    for x in range(0, GRID_WIDTH):
        for y in range(0, GRID_HEIGHT):
            if grid[x, y]:
                px = x * rw
                py = y * rh
                pygame.draw.rect(canvas, (255, x * 10, y * 10), pygame.Rect(px, py, rw, rh)) 

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
            
    pygame.display.update() 