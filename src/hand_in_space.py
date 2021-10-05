from enum import Enum


class HandOrientation(Enum):
    palm = 'palm'
    back = 'back'
    mid = 'mid'

    def __str__(self):
        return self.value

    @staticmethod
    def from_string(s):
        try:
            return HandOrientation[s]
        except KeyError:
            raise ValueError()


class HandType(Enum):
    left = 'left'
    right = 'right'

    def __str__(self):
        return self.value

    @staticmethod
    def from_string(s):
        try:
            return HandType[s]
        except KeyError:
            raise ValueError()


class HandDirection(Enum):
    earth_base = 'earth_base'
    sky_base = 'sky_base'
    camera_base = 'camera_base'
    person_base = 'person_base'

    def __str__(self):
        return self.value

    @staticmethod
    def from_string(s):
        try:
            return HandDirection[s]
        except KeyError:
            raise ValueError()
