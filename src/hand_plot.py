from unicodedata import name
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

class HandPlot:
  def __init__(self, hand):
    self.hand = hand
    self.plotly_fig = go.Figure()

  def plot_landmarks(self):
    for lm in self.hand.landmarks:
      self.plotly_fig.add_trace(go.Scatter3d(
            x=[lm.get_x()], 
            y=[lm.get_y()], 
            z=[lm.get_z()]
          ))

  def plot_landmark(self, landmark, tag):
    self.plotly_fig.add_trace(go.Scatter3d(
          x=[landmark.get_x()], 
          y=[landmark.get_y()], 
          z=[landmark.get_z()],
          name=tag
        ))

  def plot_fingers_relation(self):
    landmarks = []
    for finger in self.hand.fingers:
      landmarks = self.hand.fingers[finger].get_landmarks()
      for i in range(0,3):
        self.plotly_fig.add_trace(go.Scatter3d(
            x=[landmarks[i].get_x(),landmarks[i+1].get_x()], 
            y=[landmarks[i].get_y(),landmarks[i+1].get_y()], 
            z=[landmarks[i].get_z(),landmarks[i+1].get_z()], 
            mode="lines"
          ))

  def plot_palm_relation(self):
    for (a,b) in self.hand.palm:
      self.plotly_fig.add_trace(go.Scatter3d(
          x=[a.get_x(),b.get_x()], 
          y=[a.get_y(),b.get_y()], 
          z=[a.get_z(),b.get_z()], 
          mode="lines"
        ))

  def plot_area(self):
    for (a,b) in self.hand.area:
      self.plotly_fig.add_trace(go.Scatter3d(
          x=[a.get_x(),b.get_x()], 
          y=[a.get_y(),b.get_y()], 
          z=[a.get_z(),b.get_z()], 
          mode="lines"
        ))

  def plot(self):
    #self.plot_landmark(self.hand.get_promedio_aritmetico(), 'promedio aritmetico')
    #self.plot_landmark(self.hand.get_promedio_geometrico(), 'promedio geometrico')


    self.plot_landmarks()
    #self.plot_area()
    self.plot_fingers_relation()
    self.plot_palm_relation()
    self.plotly_fig.show()
