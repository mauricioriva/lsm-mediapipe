class Finger:
  def __init__(self, base, middle_down, middle_up, top):
    self.base = base
    self.middle_down = middle_down
    self.middle_up = middle_up
    self.top = top
  
  def get_landmarks(self):
    return [
      self.base,
      self.middle_down,
      self.middle_up,
      self.top
    ]

  def get_base(self):
    return self.base

  def get_middle_down(self):
    return self.middle_down

  def get_middle_up(self):
    return self.middle_up

  def get_top(self):
    return self.top
