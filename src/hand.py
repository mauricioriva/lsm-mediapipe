import math
import pandas as pd

from Bezier import Bezier #plot
import bezier #features
import numpy as np

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
    self.m_distance = self.matrix_distance()
    self.m_corr = self.correlation_matrix()
    self.save_correlation_matrix()

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
      (self.landmarks[20], self.landmarks[19]),
      (self.landmarks[19], self.landmarks[18]),
      (self.landmarks[18], self.landmarks[17]),
      (self.landmarks[17], self.landmarks[0])
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

  def matrix_distance(self):
    md = []
    for i in range (0,21):
      row = []
      for j in range (0,21):
        row.append(0)
      md.append(row)
    for i in range(len(md)):
      for j in range(len(md[i])):
        md[i][j] = self.formula_distancia(
          self.landmarks[i].get_x(), self.landmarks[i].get_y(), self.landmarks[i].get_z(),
          self.landmarks[j].get_x(), self.landmarks[j].get_y(), self.landmarks[j].get_z()
        )
    return md

  def formula_distancia(self,x_1,y_1,z_1,x_2,y_2,z_2):
    return round(math.sqrt(
      (x_1 - x_2)**2 + (y_1 - y_2)**2 + (z_1 - z_2)**2
    ), 3)

  def correlation_matrix(self):
    return pd.DataFrame(self.m_distance).corr()

  def save_correlation_matrix(self):
    self.m_corr.to_csv('correlacion.csv')

  def bezier_plot_3d(self, points):
    t_points = np.arange(0, 1, 0.01)
    array_points = []
    for p in points:
      array_points.append(p.get_landmarks_array())
    points1 = np.array(array_points)
    curve3d = Bezier.Curve(t_points, points1)
    return curve3d

  def bezier_plot_2d(self, points):
    nodes2d = np.asfortranarray(lm.Landmark.separate_coords_only_xy(points))
    curve2d = bezier.Curve.from_nodes(nodes2d)
    return curve2d

  def bezier_triangle_plot_2d(self, points):
    nodes2d = np.asfortranarray(lm.Landmark.separate_coords_only_xy(points))
    triangle = bezier.Triangle(nodes2d, degree=2)
    return triangle

  def bezier_curve_features(self, points): # points = [landmark,landmark,landmark,...]
    ## 3D
    print('3D')
    nodes = np.asfortranarray(lm.Landmark.separate_coords(points))
    curve = bezier.Curve(nodes, 3)
    length = curve.length
    matrix = curve.to_symbolic()
    ## 2D
    print('2D')
    nodes2d = np.asfortranarray(lm.Landmark.separate_coords_only_xy(points))
    curve2d = bezier.Curve(nodes2d, 2)
    length2d = curve2d.length
    matrix2d = curve2d.to_symbolic()
    implicitize2d = curve2d.implicitize()
    ## Triangle
    print('Triangle')
    nodes2d = np.asfortranarray(lm.Landmark.separate_coords_only_xy(points))
    triangle = bezier.Triangle(nodes2d, degree=2)
    area = triangle.area
    matrix = triangle.to_symbolic()
    implicitize = triangle.implicitize()
