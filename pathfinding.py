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
        agent.path = []
        visited = {(agent.x, agent.y) : (0, 0, None, None)}
        queue = [(0, agent.x, agent.y)]
        
        while len(queue) > 0:
            (_, x, y) = heappop(queue)
            
            # Check if goal is satisfied.
            if x == agent.goal[0] and y == agent.goal[1]:
                # Trace path.
                agent.path = [(x, y)]
                while True:
                    (_, _, px, py) = visited[agent.path[0]]
                    if px is None or py is None:
                        break
                    else:
                        agent.path.insert(0, (px, py))
                break
            
            # Add neighbors.
            for direction in DIRECTIONS:
                nx = x + direction[0]
                ny = y + direction[1]
                if not grid[(nx, ny)]:
                    g = visited[(x, y)][1] + 1
                    h = heuristic(nx, ny, agent.goal[0], agent.goal[1])
                    f = g + h
                    
                    if not (nx, ny) in visited or visited[(nx, ny)][0] > f:
                        visited[(nx, ny)] = (f, g, x, y)
                        heappush(queue, (f, nx, ny))

        
def a_star_naive_overlap(grid, agents):
    paths = {}
    for agent in agents:
        agent.path = []
        visited = {(agent.x, agent.y) : (0, 0, None, None)}
        queue = [(0, agent.x, agent.y)]
        
        while len(queue) > 0:
            (dist, x, y) = heappop(queue)
            
            # Check if goal is satisfied.
            overlap = (x, y) in paths
            if x == agent.goal[0] and y == agent.goal[1] or overlap:
                agent.path = [(x, y)]
                
                # Reuse path if there is overlap with already seen paths.
                if overlap:
                    while True:
                        if agent.path[-1] in paths:
                            agent.path.append(paths[agent.path[-1]])
                        else:
                            break
                      
                
                # Trace path from visited nodes.
                while True:
                    (_, _, px, py) = visited[agent.path[0]]
                    if px is None or py is None:
                        break
                    else:
                        paths[(px, py)] = agent.path[0]
                        agent.path.insert(0, (px, py))
                break
            
            # Add neighbors.
            for direction in DIRECTIONS:
                nx = x + direction[0]
                ny = y + direction[1]
                if not grid[(nx, ny)]:
                    g = visited[(x, y)][1] + 1
                    h = heuristic(nx, ny, agent.goal[0], agent.goal[1])
                    f = g + h
                    
                    if not (nx, ny) in visited or visited[(nx, ny)][0] > f:
                        visited[(nx, ny)] = (f, g, x, y)
                        heappush(queue, (f, nx, ny))

        
def a_star_overlap(grid, agents):
    paths = {(agents[0].goal) : (0, None, None)}
    count = 0
    for agent in agents:
        count += 1
        agent.path = []
        visited = {(agent.x, agent.y) : (0, 0, None, None)}
        queue = [(0, agent.x, agent.y)]
        
        while len(queue) > 0:
            (dist, x, y) = heappop(queue)

            # Check if goal is satisfied.
            overlap = (x, y) in paths
            if x == agent.goal[0] and y == agent.goal[1] or overlap:
                agent.path = [(x, y)]
                
                # Reuse path if there is overlap with already seen paths.
                if overlap:
                    while True:
                        _, px, py = paths[agent.path[-1]]
                        if px is None or py is None:
                            break
                        agent.path.append((px, py))
                
                # Trace path from visited nodes.
                while True:
                    x, y = agent.path[0]
                    _, _, px, py = visited[(x, y)]
                    if px is None or py is None:
                        break

                    agent.path.insert(0, (px, py))
                    paths[(px, py)] = (paths[(x, y)][0] + 1, x, y)
                    
                break
            
            # Add neighbors.
            for direction in DIRECTIONS:
                nx = x + direction[0]
                ny = y + direction[1]
                if not grid[(nx, ny)]:
                    g = visited[(x, y)][1] + 1
                    f = g
                    if (nx, ny) in paths:
                        f += paths[(nx, ny)][0]
                    else:
                        f += heuristic(nx, ny, agent.goal[0], agent.goal[1])
                        
                    if not (nx, ny) in visited or visited[(nx, ny)][0] > f:
                        visited[(nx, ny)] = (f, g, x, y)
                        heappush(queue, (f, nx, ny))

        