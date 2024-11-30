import random
import time
from grid import Grid
from agent import Agent
from pathfinding import *

GRID_WIDTH = 400
GRID_HEIGHT = 250
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
ITERATIONS = 10
agent_counts = range(100, 1100, 100)

data = []

for agent_count in agent_counts:
    sum_a = 0
    sum_b = 0
    
    for i in range(ITERATIONS):
        print("ITERATION", i + 1)
        grid = Grid(GRID_WIDTH, GRID_HEIGHT)

        # Pick goal.
        goal_x = 0
        goal_y = 0
        while True:
            goal_x = random.randint(0, GRID_WIDTH)
            goal_y = random.randint(0, GRID_HEIGHT)
            if not grid[(goal_x, goal_y)]:
                break
            
            
        # Initialize and place agents.
        agents = []
        while(len(agents) < agent_count):
            x = random.randint(0, GRID_WIDTH)
            y = random.randint(0, GRID_HEIGHT)
            if not grid[(x, y)]:
                agent = Agent(x, y, (goal_x, goal_y))
                agent.px = x
                agent.py = y
                agents.append(agent)
        
        agents_copy = agents.copy()

        # Pathfind.
        start_time = time.perf_counter()
        a_star(grid, agents_copy) 
        end_time = time.perf_counter()
        elapsed_time_a = end_time - start_time
        sum_a += elapsed_time_a

        start_time = time.perf_counter()
        a_star_optimized(grid, agents) 
        end_time = time.perf_counter()
        elapsed_time_b = end_time - start_time
        sum_b += elapsed_time_b

    a = sum_a / ITERATIONS
    b = sum_b / ITERATIONS
    data.append((a, b))
    print(agent_count, a, b)
    

for i in range(len(data)):
    print(agent_counts[i], data[i][0], data[i][1])