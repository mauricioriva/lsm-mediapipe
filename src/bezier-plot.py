from Bezier import Bezier
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

t_points = np.arange(0, 1, 0.01) #................................. Creates an iterable list from 0 to 1.
points1 = np.array([[0, 0, 0], [0.4, -1, 1], [0.6, 1, 2], [1, 0, 3]]) #.... Creates an array of coordinates.
curve1 = Bezier.Curve(t_points, points1) #......................... Returns an array of coordinates.

plt.figure()
plt.plot(
	curve1[:, 0],   # x-coordinates.
	curve1[:, 1],    # y-coordinates.
	curve1[:, 2]
)

plt.plot(
	points1[:, 0],  # x-coordinates.
	points1[:, 1],  # y-coordinates.
	points1[:, 2],
	'ro:'           # Styling (red, circles, dotted).
)

plt.grid()

plotly_fig = go.Figure()


plotly_fig.add_traces(go.Scatter3d(
	x=curve1[:, 0],
	y=curve1[:, 1],
	z=curve1[:, 2],
	mode="lines",
))

plotly_fig.show()
plt.show()
