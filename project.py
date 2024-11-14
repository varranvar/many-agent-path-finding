import pygame 
import random
import math
from grid import Grid
from agent import Agent
from pathfinding import pathfind

GRID_WIDTH = 80
GRID_HEIGHT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
AGENT_COUNT = 10
TRANSITION_FRAMES = 100

# Initialize pygame window.
pygame.init() 
canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Many Agent Path Finding") 
exit = False
  
# Initalize grid and generate maze.
grid = Grid(GRID_WIDTH, GRID_HEIGHT)
# TODO: Generate maze.

# Pick goal location.
goal_x = 0
goal_y = 0
while True:
    goal_x = random.randint(0, GRID_WIDTH)
    goal_y = random.randint(0, GRID_HEIGHT)
    if not grid[(goal_x, goal_y)]:
        break

# Initialize and place agents.
agents = []
while(len(agents) < AGENT_COUNT):
    x = random.randint(0, GRID_WIDTH)
    y = random.randint(0, GRID_HEIGHT)
    if not grid[(x, y)]:
        agent = Agent(x, y, (goal_x, goal_y))
        agent.px = x
        agent.py = y
        agents.append(agent)
  
# Pathfind.
pathfind(grid, agents)
  
# Draw paths.
frame = 0
while not exit: 
    canvas.fill((0, 0, 0))
    
    
    # If not a transition frame, update the agent location.
    if frame == 0:
        for agent in agents:
            agent.px = agent.x
            agent.py = agent.y
            agent.take_next_step_in_path()
            
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
    transition = frame / TRANSITION_FRAMES
    for agent in agents:
        x = agent.x * rw
        y = agent.y * rh
        px = agent.px * rw
        py = agent.py * rh
        tx = px + (x - px) * transition
        ty = py + (y - py) * transition
        pygame.draw.rect(
            canvas, 
            (255 * (agent.x / GRID_WIDTH), 255 * (agent.y / GRID_HEIGHT), 255), 
            pygame.Rect(tx, ty, rw, rh)
        )     
        
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True

    pygame.display.update() 
    
    # Update transition frame.
    frame = (frame + 1) % TRANSITION_FRAMES