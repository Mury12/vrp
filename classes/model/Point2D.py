import math


class Point2D:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distanceTo(self, next_c):
        return math.sqrt((next_c.x - self.x) ** 2 + (next_c.y - self.y) ** 2)

    def __repr__(self):
        return "".join(["Position: (", str(self.x), ", ", str(self.y), ")"])
