import math

import landmark as lm
import finger as fn
import hand_plot as hp

class Hand:
  def __init__(self,mediapipe_hand_landmarks):
    self.landmarks = Hand.linear_transformation_origin(
      lm.Landmark.extract_coords(mediapipe_hand_landmarks))
    self.fingers = self.construct_fingers()
    self.base = self.landmarks[0]
    self.palm = self.construct_palm()
    self.area = self.construct_area()

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

  def construct_area(self):
    return [
      (self.landmarks[0], self.landmarks[1]),
      (self.landmarks[1], self.landmarks[2]),
      (self.landmarks[2], self.landmarks[3]),
      (self.landmarks[3], self.landmarks[4]),
      (self.landmarks[4], self.landmarks[8]),
      (self.landmarks[8], self.landmarks[12]),
      (self.landmarks[12], self.landmarks[16]),
      (self.landmarks[16], self.landmarks[20]),
      (self.landmarks[0], self.landmarks[17]),
      (self.landmarks[17], self.landmarks[18]),
      (self.landmarks[18], self.landmarks[19]),
      (self.landmarks[19], self.landmarks[20])
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

  def get_promedio_aritmetico(self):
    x = []
    y = []
    z = []
    for landmark in self.landmarks:
      x.append(landmark.get_x())
      y.append(landmark.get_y())
      z.append(landmark.get_z())
    return lm.Landmark(
      sum(x) / len(x),
      sum(y) / len(y),
      sum(z) / len(z)
    )

  def get_promedio_geometrico(self):
    x = []
    y = []
    z = []
    for landmark in self.landmarks:
      x.append(landmark.get_x())
      y.append(landmark.get_y())
      z.append(landmark.get_z())
    return lm.Landmark(
      math.prod(x) ** (1/len(x)),
      math.prod(y) ** (1/len(y)),
      math.prod(z) ** (1/len(z))
    )

  def linear_transformation_origin(landmarks):
    new_landmarks = []
    for landmark in landmarks:
      new_landmarks.append(
        lm.Landmark(
          (landmark.get_x() - landmarks[0].get_x()) * -1, 
          (landmark.get_y() - landmarks[0].get_y()) * -1, 
          (landmark.get_z() - landmarks[0].get_z()) * -1
          ))
    return new_landmarks
