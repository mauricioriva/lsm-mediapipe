import landmark as lm
import finger as fn
import hand_plot as hp

class Hand:
  def __init__(self,mediapipe_hand_landmarks):
    self.mediapipe_hand_landmarks = mediapipe_hand_landmarks
    self.landmarks = lm.Landmark.extract_coords(mediapipe_hand_landmarks)
    self.fingers = self.construct_fingers()
    self.base = self.landmarks[0]
    self.palm = self.construct_palm()

  def construct_palm(self):
    return [
      (self.landmarks[0], self.landmarks[1]),
      (self.landmarks[0], self.landmarks[5]),
      (self.landmarks[0], self.landmarks[17]),
      (self.landmarks[5], self.landmarks[9]),
      (self.landmarks[9], self.landmarks[13]),
      (self.landmarks[13], self.landmarks[17]),
      (self.landmarks[0], self.landmarks[9]),
      (self.landmarks[0], self.landmarks[13]),
    ]

  def construct_fingers(self):
    i = 1
    fingers_dict = { }
    finger_names = ['thumb', 'index', 'middle', 'ring', 'little']
    for finger in finger_names:
      fingers_dict[finger] = fn.Finger(
        self.landmarks[i],
        self.landmarks[i+1],
        self.landmarks[i+2],
        self.landmarks[i+3]
      )
      i = i+4
    return fingers_dict
