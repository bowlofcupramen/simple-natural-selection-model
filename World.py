"""w"""


class World:
    """w"""

    def __init__(self, width, height, duration):
        self.grid = []
        self.duration = duration
        for i in range(height):
            self.grid.append([])
            for _ in range(width):
                self.grid[i].append(0)

    def is_blocked(self, x, y):
        """a"""
        return not (0 <= x < self.get_width() and 0 <= y < self.get_height()) or self.grid[y][x] != 0

    def get_blocker(self, x, y):
        """a"""
        return self.grid[y][x]

    def get_width(self):
        """a"""
        return len(self.grid[0])

    def get_height(self):
        """a"""
        return len(self.grid)

    def get_density(self, x, y):
        """a"""
        num_thing = 0
        for i in range(5):
            for j in range(5):
                if 0 <= y - 2 + i < len(self.grid) and 0 <= x - 2 + j < len(self.grid):
                    if self.grid[y - 2 + i][x - 2 + j] != 0:
                        num_thing += 1
        return num_thing / 5 ** 2

    def kill(self, x, y: int):
        """a"""
        self.grid[y][x] = 0

    def move(self, thing, x, y):
        """a"""
        self.grid[y][x] = thing
        self.grid[int(thing.pos[1])][thing.pos[0]] = 0

    def clear(self):
        """a"""
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                self.grid[i][j] = 0
