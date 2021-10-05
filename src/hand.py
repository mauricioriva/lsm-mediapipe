from finger import Finger
from landmark import Landmark
from hand_in_space import HandOrientation, HandDirection, HandType
from hand_state import HandState


class Hand:
    def __init__(self, media_pipe_landmarks,
                 orientation: HandOrientation = None,
                 direction: HandDirection = None,
                 hand_type: HandType = None,
                 state: HandState = None):
        self.index_finger = Finger(media_pipe_landmarks[1 - 4])
        self.middle_finger = Finger(media_pipe_landmarks[5 - 8])
        self.ring_finger = Finger(media_pipe_landmarks[9 - 12])
        self.little_finger = Finger(media_pipe_landmarks[13 - 16])
        self.thumb = Finger(media_pipe_landmarks[17 - 20])
        self.palm_base = Landmark(media_pipe_landmarks[21])
        self.orientation = orientation
        self.direction = direction
        self.type = hand_type
        self.state = state

    def set_orientation(self, orientation: HandOrientation):
        self.orientation = orientation

    def set_direction(self, direction: HandDirection):
        self.direction = direction

    def set_type(self, hand_type: HandType):
        self.type = hand_type

    def set_state(self, state: HandState):
        self.state = state

    def get_dict(self):
        return {
            'index_finger': self.index_finger.get_dict(),
            'middle_finger': self.middle_finger.get_dict(),
            'ring_finger': self.ring_finger.get_dict(),
            'little_finger': self.little_finger.get_dict(),
            'thumb': self.thumb.get_dict(),
            'palm_base': self.palm_base.get_dict()
        }
