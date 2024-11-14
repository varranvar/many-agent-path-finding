class Agent():
    def __init__(self, x ,y, goal):
        self.x = x
        self.y = y
        self.goal = goal
        self.path = []
        
    def take_next_step_in_path(self):
        if len(self.path) > 0:
            (nx, ny) = self.path.pop(0)
            self.x = nx
            self.y = ny


