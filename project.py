import pygame 
import random
from grid import Grid
from agent import Agent

GRID_WIDTH = 30
GRID_HEIGHT = 30
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
AGENT_COUNT = 4

# Initialize pygame window.
pygame.init() 
canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Many Agent Path Finding") 
exit = False
  
# Initalize grid and generate maze.
grid = Grid(GRID_WIDTH, GRID_HEIGHT)
# TODO: Generate maze.

# Initialize and place agents.
agents = []
while(len(agents) < AGENT_COUNT):
    x = random.randint(0, GRID_WIDTH)
    y = random.randint(0, GRID_HEIGHT)
    if not grid[(x, y)]:
        agents.append(Agent(x, y))
  
while not exit: 
    canvas.fill((0, 0, 0))
    
    # Update agents.
    for agent in agents:
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nx = agent.x + direction[0]
        ny = agent.y + direction[1]

        if not grid[(nx, ny)] and random.random() < 0.001:
            agent.x = nx
            agent.y = ny
    
    
    rw = SCREEN_WIDTH / GRID_WIDTH
    rh = SCREEN_HEIGHT / GRID_HEIGHT
    
    # Draw walls.
    for x in range(0, GRID_WIDTH):
        for y in range(0, GRID_HEIGHT):
            if grid[(x, y)]:
                px = x * rw
                py = y * rh
                pygame.draw.rect(canvas, (255, 255 * (x / GRID_WIDTH), 255 * (y / GRID_HEIGHT)), pygame.Rect(px, py, rw, rh)) 

    # Draw agents.
    for agent in agents:
        px = agent.x * rw
        py = agent.y * rh
        pygame.draw.rect(canvas, (255 * (agent.x / GRID_WIDTH), 255 * (agent.y / GRID_HEIGHT), 255), pygame.Rect(px, py, rw, rh)) 
        
        
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
            
    pygame.display.update() 