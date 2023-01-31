class Landmark:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def get_landmarks(self):
    return {
      'x': self.x,
      'y': self.y,
      'z': self.z
    }

  def get_landmarks_array(self):
    return [self.x, self.y, self.z]

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def get_z(self):
    return self.z

  def set_x(self,x):
    self.x = x

  def set_y(self,y):
    self.y = y

  def set_z(self,z):
    self.z = z

  def extract_coords(mediapipe_hand_landmarks):
    landmarks = []
    for i in range(0,21):
      landmarks.append(Landmark(
          mediapipe_hand_landmarks.landmark[i].x,
          mediapipe_hand_landmarks.landmark[i].y,
          mediapipe_hand_landmarks.landmark[i].z,
          ))
    return landmarks

  def separate_coords(landmarks_array):
    x_coords = []
    y_coords = []
    z_coords = []
    for landmark in landmarks_array:
      x_coords.append(landmark.get_x())
      y_coords.append(landmark.get_y())
      z_coords.append(landmark.get_z())
    return [ x_coords, y_coords, z_coords ]

  def separate_coords_only_xy(landmarks_array):
    x_coords = []
    y_coords = []
    for landmark in landmarks_array:
      x_coords.append(landmark.get_x())
      y_coords.append(landmark.get_y())
    return [ x_coords, y_coords ]
