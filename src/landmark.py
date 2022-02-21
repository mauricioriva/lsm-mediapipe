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

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def get_z(self):
    return self.z

  def extract_coords(mediapipe_hand_landmarks):
    landmarks = []
    for i in range(0,21):
      landmarks.append(Landmark(
          mediapipe_hand_landmarks.landmark[i].x,
          mediapipe_hand_landmarks.landmark[i].y,
          mediapipe_hand_landmarks.landmark[i].z,
          ))
    return landmarks
