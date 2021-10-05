class Landmark:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }
