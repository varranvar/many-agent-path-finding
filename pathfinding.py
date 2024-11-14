from heapq import *
import random
from grid import Grid
from agent import Agent

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def random_walk(grid, agents):
    
    
    for agent in agents:
        agent.path = []
        cx = agent.x
        cy = agent.y
        
        movements = 100
        while movements > 0:
            direction = random.choice(DIRECTIONS)
            nx = cx + direction[0]
            ny = cy + direction[1]
            movements -= 1

            if grid.is_valid(nx, ny) and not grid[(nx, ny)]:
                agent.path.append((nx, ny))
                cx = nx
                cy = ny

def heuristic(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(grid, agents):
    for agent in agents:
        visited = {(agent.x, agent.y) : (0, None, None)}
        queue = [(0, agent.x, agent.y)]
        
        while len(queue) > 0:
            (dist, x, y) = heappop(queue)
            
            # Check if goal is satisfied.
            if x == agent.goal[0] and y == agent.goal[1]:
                # Trace path.
                agent.path = [(x, y)]
                while True:
                    (_, px, py) = visited[agent.path[0]]
                    if px == None or py == None:
                        break
                    else:
                        agent.path.insert(0, (px, py))
                break
            
            # Add neighbors.
            for direction in DIRECTIONS:
                nx = x + direction[0]
                ny = y + direction[1]
                if not grid[(nx, ny)]:
                    g = dist + 1
                    h = heuristic(nx, ny, agent.goal[0], agent.goal[1])
                    f = g + h
                    
                    if not (nx, ny) in visited or visited[(nx, ny)][0] > f:
                        visited[(nx, ny)] = (g, x, y)
                        heappush(queue, (f, nx, ny))

        
