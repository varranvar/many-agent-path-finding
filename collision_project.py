import pygame 
import random
import time
from grid import Grid
from agent import Agent
from pathfinding import *

GRID_WIDTH = 400
GRID_HEIGHT = 250
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
AGENT_COUNT = 100
TRANSITION_FRAMES = 0
agent_states = set()

# Initialize pygame window.
pygame.init()
canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Many Agent Path Finding with Collisions") 
exit = False

# Initalize grid and generate maze.
grid = Grid(GRID_WIDTH, GRID_HEIGHT, generator='wilson')
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
print("Initializing agents...")
agents = []
while(len(agents) < AGENT_COUNT):
    x = random.randint(0, GRID_WIDTH)
    y = random.randint(0, GRID_HEIGHT)
    if not grid[(x, y)] and (x, y) not in agent_states:
        agent = Agent(x, y, (goal_x, goal_y))
        agent.px = x
        agent.py = y
        agents.append(agent)
        agent_states.add((x, y))
  
agents_copy = agents.copy()

# Pathfind.
print("Pathfinding without optmization...")
start_time = time.perf_counter()
a_star_with_collision_avoidance(grid, agents_copy) 
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)

#print("Pathfinding with corner reduction...")
#start_time = time.perf_counter()
#a_star_optimized_reduced_straight(grid, agents) 
#end_time = time.perf_counter()
#elapsed_time = end_time - start_time
#print("Elapsed time: ", elapsed_time)

#corners = calculate_corners(grid)
  
# Draw paths.

print("Drawing...")
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
                pygame.draw.rect(canvas, (100, 100, 100), pygame.Rect(px, py, rw, rh)) 
            #elif (x, y) in corners:
            #    px = x * rw
            #    py = y * rh
            #    pygame.draw.rect(canvas, (100, 200, 200), pygame.Rect(px, py, rw, rh)) 
                
    # Draw agents.
    transition = 1 if TRANSITION_FRAMES == 0 else frame / TRANSITION_FRAMES
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
        
        gx = agent.goal[0] * rw
        gy = agent.goal[1] * rh
        pygame.draw.circle(
            canvas, 
            (255, 0, 0), 
            (gx + rw / 2, gy + rh / 3),
            rw / 2
        )     
        
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True

    pygame.display.update() 
    
    # Update transition frame.
    frame = 0 if TRANSITION_FRAMES == 0 else (frame + 1) % TRANSITION_FRAMES
