
WIDTH = 1000
HEIGHT = 1000

def Grid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [
            [
                x == 0 or y == 0 or x == width - 1 or y == height - 1
                for y in range(0, height + 2)
            ] 
            for x in range(0, width + 2)
        ]
         
    def __getitem__(self, coordinate):
        return self.grid[coordinate.x + 1][coordinate.y + 1]
    
    
grid = Grid(WIDTH, HEIGHT)


