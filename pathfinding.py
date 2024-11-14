import heapq
import random
from grid import Grid
from agent import Agent

def pathfind(grid, agents):
    
    # Find corners.
    
    
    
    # Random movement.
    for agent in agents:
        agent.path = []
        cx = agent.x
        cy = agent.y
        
        count = 100
        while count > 0:
            direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            nx = cx + direction[0]
            ny = cy + direction[1]

            if not grid[(nx, ny)] and random.random() < 0.01:
                agent.path.append((nx, ny))
                cx = nx
                cy = ny
                count -= 1
        