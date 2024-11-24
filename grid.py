import random 

class Grid():
    def __init__(self, width, height, generator = ''):
        self.width = width
        self.height = height
        if generator == 'backtrack':
            self.grid = [[True] * (height+2) for _ in range(width+2)]
            x, y = 1, 1
            self.grid[x][y] = False

            stack = [(x, y)]
            while stack:
                x, y = stack.pop()
                neighbors = []
                for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
                    nx = x+dx
                    ny = y+dy
                    if 0 < nx < width+1 and 0 < ny < height+1 and self.grid[nx][ny]:
                        neighbors.append((nx, ny))
                if neighbors:
                    nx, ny = random.choice(neighbors)
                    self.grid[nx][ny] = False
                    self.grid[(x+nx)//2][(y+ny)//2] = False
                    stack.append((x, y))
                    stack.append((nx, ny))
        else:
            self.grid = [
                [
                    x == 0 or y == 0 or x == width + 1 or y == height + 1 or random.random() < 0.3
                    for y in range(0, height + 2)
                ] 
                for x in range(0, width + 2)
            ]
        
    def __getitem__(self, coordinate):
        return self.grid[coordinate[0] + 1][coordinate[1] + 1]