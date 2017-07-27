import numpy as np
import numbers
from math import sqrt

def solve_quadratic(a, b, c):
    disc = b * b - 4 * a * c
    if disc < 0:
        return []
    elif disc == 0:
        return [-0.5 * b / a]
    q = -0.5 * (b + sqrt(disc)) if b > 0 else -0.5 * (b - sqrt(disc))
    x0 = q / a
    x1 = c / q
    if x0 > x1:
        return [x1, x0]
    return [x0, x1]

class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.vec = np.array([x, y, z])

    def create(v):
        return vec3(v[0], v[1], v[2])

    @property
    def x(self):
        return self.vec[0]

    @x.setter
    def x(self, x):
        self.vec[0] = x

    @property
    def y(self):
        return self.vec[1]

    @y.setter
    def y(self, y):
        self.vec[1] = y

    @property
    def z(self):
        return self.vec[2]

    @z.setter
    def z(self, z):
        self.vec[2] = z

    r, g, b = x, y, z

    def dot(self, o):
        return np.dot(self.vec, o.vec)

    def cross(self, o):
        return vec3.create(np.cross(self.vec, o.vec))

    def norm(self):
        return np.linalg.norm(self.vec)

    def normalize(self):
        self.vec = self.vec / self.norm()

    def unit(self):
        return vec3.create(self.vec / self.norm())

    def __add__(self, o):
        return vec3.create(self.vec + o.vec)

    def __sub__(self, o):
        return vec3.create(self.vec - o.vec)

    def __mul__(self, o):
        if isinstance(o, numbers.Number):
            return vec3.create(self.vec * o)
        elif isinstance(o, vec3):
            return self.dot(o)

    def __repr__(self):
        return 'vec3({0}, {1}, {2})'.format(self.x, self.y, self.z)
