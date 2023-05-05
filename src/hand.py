import math
import pandas as pd

from Bezier import Bezier #plot
import bezier #features
import numpy as np
import sympy

import landmark as lm
import finger as fn
import bezier_curve as bz

class Hand:
  def __init__(self,mediapipe_hand_landmarks):
    self.landmarks = Hand.linear_transformation_origin(
      lm.Landmark.extract_coords(mediapipe_hand_landmarks))
    self.fingers = self.construct_fingers()
    self.base = self.landmarks[0]
    self.palm = self.construct_palm()
    self.area = self.construct_area()
    #self.m_distance = self.matrix_distance()
    #self.m_corr = self.correlation_matrix()
    #self.save_correlation_matrix()

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

  # De la base a todos los demas
  # Las puntas de los dedos y la base
  def matrix_distance(self):
    labels = []
    md = []
    c = 0
    for l in self.landmarks:
      labels.append('d_0_' + str(c))
      md.append(self.formula_distancia(0, 0, 0, l.get_x(), l.get_y(), l.get_z()))
    labels.pop(0)
    md.pop(0)
    landmark_pairs = [(4, 8), (4, 12), (4, 16), (4, 20), (8, 12), (8, 16), (8, 20), (12, 16), (12, 20), (16, 20)]
    for (i,j) in landmark_pairs:
      labels.append('d_' + str(i) + '_' + str(j))
    md.extend([self.formula_distancia(self.landmarks[a].get_x(), self.landmarks[a].get_y(), self.landmarks[a].get_z(),
                                      self.landmarks[b].get_x(), self.landmarks[b].get_y(), self.landmarks[b].get_z())
                    for a, b in landmark_pairs])
    return (md, labels)

  def formula_distancia(self,x_1,y_1,z_1,x_2,y_2,z_2):
    return round(math.sqrt(
      (x_1 - x_2)**2 + (y_1 - y_2)**2 + (z_1 - z_2)**2
    ), 5)

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

  def bezier_curve_3d(self, landmarks): #point type Landmark
    nodes = np.asfortranarray(lm.Landmark.separate_coords(landmarks))
    curve = bezier.Curve.from_nodes(nodes)
    return curve

  def bezier_curve_2d(self, landmarks): #point type Landmark
    nodes = np.asfortranarray(lm.Landmark.separate_coords_only_xy(landmarks))
    curve = bezier.Curve.from_nodes(nodes)
    return curve

  def bezier_triangle_2d(self,landmarks):
    nodes = np.asfortranarray(lm.Landmark.separate_coords_only_xy(landmarks))
    triangle = bezier.Triangle(nodes, degree=2)
    return triangle

  def bezier_triangle_3d(self,landmarks):
    nodes = np.asfortranarray(lm.Landmark.separate_coords(landmarks))
    triangle = bezier.Triangle(nodes, degree=2)
    return triangle

  def bezier_curve_features(self): # points = [landmark,landmark,landmark,...]
    features = {}
    t_values = np.linspace(0, 1, 10)
    t = sympy.symbols('t')
    c = 0
    for l in self.landmarks:
      features['x_' + str(c)] = [l.get_x()]
      features['y_' + str(c)] = [l.get_y()]
      features['z_' + str(c)] = [l.get_x()]
      c = c + 1
    for finger in self.fingers: #Finger Curves
      landmarks = self.fingers[finger].get_landmarks()
      k = bz.BezierCurve(landmarks).get_curvature()
      (x,y,z) = bz.BezierCurve(landmarks).get_rotation()
      for i in t_values:
        features[finger + '_curv_' + str(i)] = [float(round(k.subs(t,i),5))] # Curvature
        features[finger + '_rot_x_' + str(i)] = [float(round(x.subs(t,i),5))] # Rotation X
        features[finger + '_rot_y_' + str(i)] = [float(round(y.subs(t,i),5))] # Rotation Y
        features[finger + '_rot_z_' + str(i)] = [float(round(z.subs(t,i),5))] # Rotation Z
      curve3d = self.bezier_curve_3d(landmarks)
      features[finger + '_length'] = [float(round(curve3d.length,5))]
    for j in range(1,5): #Horizontal Curves
      landmarks = [self.landmarks[index] for index in [j+4,j+8,j+12,j+16]]
      k = bz.BezierCurve(landmarks).get_curvature()
      for i in t_values:
        features['h_' + str(j) + '_curv_' + str(i)] = [float(round(k.subs(t,i),5))] # Curvature
        features['h_' + str(j) + '_rot_x_' + str(i)] = [float(round(x.subs(t,i),5))] # Rotation X
        features['h_' + str(j) + '_rot_y_' + str(i)] = [float(round(y.subs(t,i),5))] # Rotation Y
        features['h_' + str(j) + '_rot_z_' + str(i)] = [float(round(z.subs(t,i),5))] # Rotation Z
      curve3d = self.bezier_curve_3d(landmarks)
      features['h_' + str(j) + '_length'] = [float(round(curve3d.length,5))]
    #Triangle 2D
    landmarks = [self.landmarks[index] for index in [0,20,16,12,8,4]]    
    triangle2d = self.bezier_triangle_2d(landmarks)
    features['triangle_area'] = [float(round(triangle2d.area,5))]
    #Matrix Distance
    (md, labels) = self.matrix_distance()
    c = 0
    for l in labels:
      features[l] = [md[c]]
      c = c + 1
    return pd.DataFrame.from_dict(features)
