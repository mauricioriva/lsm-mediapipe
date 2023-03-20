import sympy
import numpy as np

class BezierCurve:
  def __init__(self, landmarks) -> None:
    self.p0 = landmarks[0]
    self.p1 = landmarks[1]
    self.p2 = landmarks[2]
    self.p3 = landmarks[3]

  def get_bezier_equation(self):
    # B(t) = P0*(1-t)^3 + 3P1t*(1-t)^2 + 3P2t^2*(1-t) + P3*t^3
    t = sympy.symbols('t')
    x_t = self.p0.get_x()*(1-t)**3 + 3*self.p1.get_x()*t*(1-t)**2 + 3*self.p2.get_x()*t*t*(1-t) + self.p3.get_x()*t**3
    y_t = self.p0.get_y()*(1-t)**3 + 3*self.p1.get_y()*t*(1-t)**2 + 3*self.p2.get_y()*t*t*(1-t) + self.p3.get_y()*t**3
    z_t = self.p0.get_z()*(1-t)**3 + 3*self.p1.get_z()*t*(1-t)**2 + 3*self.p2.get_z()*t*t*(1-t) + self.p3.get_z()*t**3
    b_t = (sympy.simplify(x_t), sympy.simplify(y_t), sympy.simplify(z_t))
    return b_t

  def diff_bezier(self, b_t):
    t = sympy.symbols('t')
    (x_t, y_t, z_t) = b_t
    x_td = sympy.diff(x_t, t)
    y_td = sympy.diff(y_t, t)
    z_td = sympy.diff(z_t, t)
    b_td = (sympy.simplify(x_td), sympy.simplify(y_td), sympy.simplify(z_td))
    return b_td

  def get_curvature(self):
    t = sympy.symbols('t')
    b_t = self.get_bezier_equation()
    b_td = self.diff_bezier(b_t)
    b_tdd = self.diff_bezier(b_td)
    (x_td, y_td, z_td) = b_td
    (x_tdd, y_tdd, z_tdd) = b_tdd
    k = sympy.sqrt( (z_tdd*y_td - y_tdd*z_td)**2 + 
                                   (x_tdd*z_td - z_tdd*x_td)**2 + 
                                   (y_tdd*x_td - x_tdd*y_td)**2 ) / (x_td**2 + y_td**2 + z_td**2)**(3/2)
    t_values = np.linspace(0, 1, 1000)
    curvature_values = []
    for i in t_values:
      curvature_values.append(k.subs(t,i))
    return max(curvature_values)
