from landmark import Landmark


class Finger:
    def __init__(self, up, middle_up, middle_down, down):
        self.up = Landmark(up.x, up.y, up.z)
        self.middle_up = Landmark(middle_up.x, middle_up.y, middle_up.z)
        self.middle_down = Landmark(middle_down.x, middle_down.y, middle_down.z)
        self.down = Landmark(down.x, down.y, down.z)

    def get_dict(self):
        return {
            'up': self.up.get_dict(),
            'middle_up': self.middle_up.get_dict(),
            'middle_down': self.middle_down.get_dict(),
            'down': self.down.get_dict()
        }
