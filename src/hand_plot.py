from unicodedata import name
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

class HandPlot:
  def __init__(self, hand):
    self.hand = hand
    self.plotly_fig = go.Figure()
    #Matplot
    self.matplotfig = plt.figure(figsize=(10,10))
    self.matplotax = self.matplotfig.add_subplot(111)

  def plot_landmarks(self):
    for lm in self.hand.landmarks:
      self.plotly_fig.add_trace(go.Scatter3d(
            x=[lm.get_x()], 
            y=[lm.get_y()], 
            z=[lm.get_z()]
          ))
      #Matplot
      self.matplotax.scatter(lm.get_x(),lm.get_y())

  def plot_landmark(self, landmark, tag):
    self.plotly_fig.add_trace(go.Scatter3d(
          x=[landmark.get_x()], 
          y=[landmark.get_y()], 
          z=[landmark.get_z()],
          name=tag
        ))
    #Matplot
    self.matplotax.scatter(landmark.get_x(),landmark.get_y())

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
        #Matplot
        self.matplotax.plot(
            np.linspace(landmarks[i].get_x(),landmarks[i+1].get_x()),
            np.linspace(landmarks[i].get_y(),landmarks[i+1].get_y())
          )

  def plot_palm_relation(self):
    for (a,b) in self.hand.palm:
      self.plotly_fig.add_trace(go.Scatter3d(
          x=[a.get_x(),b.get_x()], 
          y=[a.get_y(),b.get_y()], 
          z=[a.get_z(),b.get_z()], 
          mode="lines"
        ))
      #Matplot
      self.matplotax.plot(
          np.linspace(a.get_x(),b.get_x()),
          np.linspace(a.get_y(),b.get_y())
        )

  def plot_area(self):
    for (a,b) in self.hand.area:
      self.plotly_fig.add_trace(go.Scatter3d(
          x=[a.get_x(),b.get_x()], 
          y=[a.get_y(),b.get_y()], 
          z=[a.get_z(),b.get_z()], 
          mode="lines"
        ))

  def plot_bezier_fingers(self):
    for finger in self.hand.fingers:
      landmarks = self.hand.fingers[finger].get_landmarks()
      curve3d = self.hand.bezier_plot_3d(landmarks)
      self.plotly_fig.add_traces(go.Scatter3d(
          x=curve3d[:, 0],
          y=curve3d[:, 1],
          z=curve3d[:, 2],
          mode="lines",
        ))
      #Matplot
      curve2d = self.hand.bezier_plot_2d(landmarks)
      curve2d.plot(256, ax=self.matplotax)

  def plot_horizontal_curves(self):
    for i in range(1,5):
      curve3d = self.hand.bezier_plot_3d(
        [self.hand.landmarks[index] for index in [i,i+4,i+8,i+12,i+16]])
      self.plotly_fig.add_traces(go.Scatter3d(
          x=curve3d[:, 0],
          y=curve3d[:, 1],
          z=curve3d[:, 2],
          mode="lines",
        ))
      #Matplot
      curve2d = self.hand.bezier_plot_2d(
        [self.hand.landmarks[index] for index in [i,i+4,i+8,i+12,i+16]])
      curve2d.plot(256, ax=self.matplotax)

  def plot_bezier_triangle_2d(self):
    points = []
    points.append(self.hand.landmarks[0])
    points.append(self.hand.landmarks[20])
    points.append(self.hand.landmarks[16])
    points.append(self.hand.landmarks[12])
    points.append(self.hand.landmarks[8])
    points.append(self.hand.landmarks[4])    
    triangle = self.hand.bezier_triangle_plot_2d(points)
    triangle.plot(25,ax=self.matplotax)
  
  def plot(self):
    #self.plot_landmark(self.hand.get_promedio_aritmetico(), 'promedio aritmetico')
    #self.plot_landmark(self.hand.get_promedio_geometrico(), 'promedio geometrico')

    self.plot_landmarks()
    #self.plot_area()
    self.plot_fingers_relation()
    self.plot_palm_relation()
    #self.plot_bezier_fingers()
    #self.plot_horizontal_curves()

    #Matplot
    #self.plot_bezier_triangle_2d()

    #PLOT
    self.plotly_fig.show()

    #Matplot
    plt.show()
