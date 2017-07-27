from vec import vec3

def virtual(f):
    def err(*args):
        raise Exception('{} should not be called directly and must be overriden in the base class'.format(f.__name__))
    return err

class Entity:

    class NAMES:
        NONE = 'none'
        LIGHT = 'light'
        GEOMETRY = 'geometry'
        CAMERA = 'camera'

    def __init__(self):
        self._position = vec3()
        self._rotation = vec3()
        self._scale = vec3()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale


class Light(Entity):
    name = Entity.NAMES.LIGHT

    def __init__(self, color=vec3(1, 1, 1)):
        super().__init__()
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color


class Geometry(Entity):
    name = Entity.NAMES.GEOMETRY

    def __init__(self):
        super().__init__()

    @virtual
    def intersect(self, ray):
        return None

    @virtual
    def get_surface_data(self, p):
        return None


class Camera(Entity):
    name = Entity.NAMES.CAMERA

    def __init__(self):
        super().__init__()


class PerspectiveCamera(Camera):

    def __init__(self, fov, ar, n_clip, f_clip):
        super().__init__()
        self._fov = fov
        self._ar = ar
        self._n_clip = n_clip
        self._f_clip = f_clip


class Scene:
    def __init__(self):
        self.entities = {val: [] for key, val in Entity.NAMES.__dict__.items() \
                                              if not key.startswith('__')}

    def add_entity(self, entity):
        self.entities[entity.name].append(entity)


class Renderer:
    def __init__(self):
        pass

    def render(self, camera, scene):
        pass

class Ray:
    def __init__(self, origin, direction):
        self.o = origin
        self.d = direction
