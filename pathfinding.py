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

        
def a_star_naively_optimized(grid, agents):
    paths = {}
    for agent in agents:
        agent.path = []
        visited = {(agent.x, agent.y) : (0, 0, None, None)}
        queue = [(0, agent.x, agent.y)]
        
        while len(queue) > 0:
            (_, x, y) = heappop(queue)
            
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

        
def a_star_optimized(grid, agents):
    paths = {(agents[0].goal) : (0, None, None)}

    for agent in agents:
        agent.path = []
        visited = {(agent.x, agent.y) : (0, 0, None, None)}
        queue = [(0, agent.x, agent.y)]
        
        while len(queue) > 0:
            (_, x, y) = heappop(queue)

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


def a_star_optimized_many_agent(grid, agents):
    paths = {}
    count = 0
    for agent in agents:
        count += 1
        agent.path = []
        visited = {(agent.x, agent.y) : (0, 0, None, None)}
        queue = [(0, agent.x, agent.y)]
        
        while len(queue) > 0:
            (_, x, y) = heappop(queue)

            # Check if goal is satisfied.
            if x == agent.goal[0] and y == agent.goal[1]:
                agent.path = [(x, y)]
                
                # Trace path from visited nodes.
                while True:
                    cx, cy = agent.path[0]
                    _, _, px, py = visited[(cx, cy)]
                    
                    if px is None or py is None:
                        break
                    
                    # If the two are more than one move away, it most be a path.
                    if px != cx and py != cy:
                        shortcut = [(px, py)]
                        while True:
                            (_, next) = paths[(px, py)][(cx, cy)]
                            if next == (cx, cy):
                                break
                            
                            shortcut.append(next)
                            px, py = next
                            
                        agent.path = shortcut + agent.path
                    else:
                        agent.path.insert(0, (px, py))

                        
                # Record new path.
                for i in range(0, len(agent.path) // 2):
                    s = agent.path[i]
                    if not s in paths:
                        paths[s] = {}
                    destinations = paths[s]
                    
                    for j in range(i + 1 + len(agent.path) // 2, len(agent.path)): # TODO: Reverse entry as well
                        e = agent.path[j]        
                        if s == e:
                            continue

                        if not e in destinations:
                            # Store path.
                            dist = j - i
                            destinations[e] = (dist, agent.path[i + 1])
                            
                            # Store reverse path.
                            if not e in paths:
                                paths[e] = {}
                                
                            if not s in paths[e]:
                                paths[e][s] = (dist, agent.path[j - 1])
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
                        
            # Add path.
            if (x, y) in paths:
                for destination, (dist, _) in paths[(x, y)].items():
                    if dist > 1:
                        g = visited[(x, y)][1] + dist
                        h = heuristic(destination[0], destination[1], agent.goal[0], agent.goal[1])
                        f = g + h
                        if not destination in visited or visited[destination][0] > f:
                            visited[destination] = (f, g, x, y)
                            heappush(queue, (f, destination[0], destination[1]))
                            
                            
                            
       
def a_star_optimized_reduced(grid, agents):
    
    # Find corners.
    corners = []
    for x in range(grid.width):
        for y in range(grid.height):
            if not grid[(x, y)]:
                n = grid[(x, y + 1)]
                nw = grid[(x - 1, y + 1)]
                w = grid[(x - 1, y)]
                sw = grid[(x - 1, y - 1)]
                s = grid[(x, y - 1)]
                se = grid[(x + 1, y - 1)]
                e = grid[(x + 1, y)]
                ne = grid[(x + 1, y + 1)]
                
                corner = \
                    (not n and not w and nw) or \
                    (not w and not s and sw) or \
                    (not s and not e and se) or \
                    (not e and not n and ne)
                
                if corner:
                    corners.append((x, y))
                    
    # Find edges between corners.
    edges = {}
    for corner in corners:
        edges[corner] = []
        
    for i in range(len(corners)):
        (x1, y1) = corners[i]
        for j in range(i + 1, len(corners)):
            (x2, y2) = corners[j]
                    
            if exists_clear_path(grid, x1, y1, x2, y2):
                dist = abs(x1 - x2) + abs(y1 - y2)
                edges[(x1, y1)].append((dist, x2, y2))
                edges[(x2, y2)].append((dist, x1, y1))
                
    # Find edges between goal and corners.
    (gx, gy) = agents[0].goal
    if not (gx, gy) in edges:
        edges[(gx, gy)] = []
        for i in range(len(corners)):
            (x, y) = corners[i]
            
            if exists_clear_path(grid, x, y, gx, gy):
                dist = abs(x - gx) + abs(y - gy)
                edges[(x, y)].append((dist, gx, gy))
                edges[(gx, gy)].append((dist, x, y))
                
    
    paths = {(gx, gy) : (0, None, None)}

    for agent in agents:
        # Find edges between the agent starting point and the corners.
        if not (agent.x, agent.y) in edges:
            edges[(agent.x, agent.y)] = []
            for i in range(len(corners)):
                (x, y) = corners[i]
                
                if exists_clear_path(grid, x, y, agent.x, agent.y):
                    dist = abs(x - agent.x) + abs(y - agent.y)
                    edges[(x, y)].append((dist, agent.x, agent.y))
                    edges[(agent.x, agent.y)].append((dist, x, y))
        
        agent.path = []
        visited = {(agent.x, agent.y) : (0, 0, None, None)}
        queue = [(0, agent.x, agent.y)]
        
        while len(queue) > 0:
            (_, x, y) = heappop(queue)

            # Check if goal is satisfied.
            overlap = (x, y) in paths
            if x == gx and y == gy or overlap:
                agent.path = [(x, y)]
                
                # Reuse path if there is overlap with already seen paths.
                if overlap:
                    while True:
                        x, y = agent.path[-1]
                        _, px, py = paths[(x, y)]
                        if px is None or py is None:
                            break
                        agent.path = agent.path + get_path(x, y, px, py)
                        agent.path.append((px, py))
                
                # Trace path from visited nodes.
                while True:
                    x, y = agent.path[0]
                    _, _, px, py = visited[(x, y)]
                    if px is None or py is None:
                        break
                    
                    agent.path = get_path(px, py, x, y) + agent.path
                    dist = abs(x - px) + abs(y - py)
                    paths[(px, py)] = (paths[(x, y)][0] + dist, x, y)
                    
                break
            
            # Add neighbors.
            for (dist, nx, ny) in edges[(x, y)]:
                if not grid[(nx, ny)]:
                    g = visited[(x, y)][1] + dist
                    f = g
                    if (nx, ny) in paths:
                        f += paths[(nx, ny)][0]
                    else:
                        f += heuristic(nx, ny, agent.goal[0], agent.goal[1])
                        
                    if not (nx, ny) in visited or visited[(nx, ny)][0] > f:
                        visited[(nx, ny)] = (f, g, x, y)
                        heappush(queue, (f, nx, ny))

def exists_clear_path(grid, x1, y1, x2, y2):
    m = 2 * (y2 - y1) 
    slope_error = m - (x2 - x1) 
  
    y = y1 
    for x in range(x1, x2 + 1): 
        if grid[(x, y)]:
            return False
        
        slope_error += m 
        if (slope_error >= 0): 
            y = y + 1
            slope_error = slope_error - 2 * (x2 - x1) 
       
    return True

def get_path(x0, y0, x1, y1):
    path = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    x, y = x0, y0

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    
    if dx > dy:
        error = dx / 2.0
        while x != x1:
            path.append((x, y))
            error -= dy
            if error < 0:
                y += sy
                error += dx
            x += sx
    else:
        error = dy / 2.0
        while y != y1:
            path.append((x, y))
            error -= dx
            if error < 0:
                x += sx
                error += dy
            y += sy

    return path