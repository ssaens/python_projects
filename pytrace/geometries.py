import entity
from vec import vec3, solve_quadratic

class Sphere(entity.Geometry):

    def __init__(self, radius):
        super().__init__()
        self.radius = radius

    def intersect(self, ray):
        a = ray.d * ray.d
        b = 2 * (ray.d * (ray.o - self.position))
        c = (ray.o - self.position) * (ray.o - self.position) - self.radius ** 2
        ts = solve_quadratic(a, b, c)
        if ts:
            closest = ts[0]
            return closest

    def get_surface_data(self, p):
        normal = (p - self.position).unit()
        texture = vec3(1, 0, 0)
        return normal, texture
