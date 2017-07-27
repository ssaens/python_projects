import curses
import time
import entity
from vec import vec3
from geometries import Sphere
from math import sin, cos

import os

class Shades:
    NONE = ' '
    LIGHT = u'\u2591'
    MEDIUM = u'\u2592'
    DARK = u'\u2593'
    FULL = u'\u2588'

class RayRenderer(entity.Renderer):
    def __init__(self, width, height, frame_buffer):
        self.width = width
        self.height = height
        self.frame_buffer = frame_buffer

    def render(self, scene, camera):
        height, width = self.height, self.width
        cast = self.cast
        frame_buffer = self.frame_buffer
        for j in range(height):
            y = (j - height / 2) * Common.CELL_HEIGHT / Common.CELL_WIDTH
            for i in range(width):
                x = (i - width / 2)
                o = vec3(x, y, camera.position.z)
                d = vec3(x, y, camera.position.z - 1) - o
                color = cast(entity.Ray(o, d), scene)
                frame_buffer[j * width + i] = color

    def cast(self, ray, scene):
        t, e = self.trace(ray, scene.entities[entity.Entity.NAMES.GEOMETRY])
        if not e:
            return Shades.NONE
        intersection = ray.o + ray.d * t
        normal, tex = e.get_surface_data(intersection)
        return self.calc_light(intersection, normal, tex, scene.entities[entity.Entity.NAMES.LIGHT])

    def trace(self, ray, entities):
        t_near = float('inf')
        intersected_entity = None
        for entity in entities:
            t = entity.intersect(ray)
            if t and t < t_near:
                t_near = t
                intersected_entity = entity
        return t_near, intersected_entity

    def calc_light(self, intersection, normal, tex, lights):
        for light in lights:
            l = (light.position - intersection).unit()
            dot = l * normal
            if dot <= 0:
                return Shades.LIGHT
            if dot < .40:
                return Shades.MEDIUM
            if dot < .85:
                return Shades.DARK
            return Shades.FULL

class Common:
    TIMESTEP = 0.01
    CELL_WIDTH = 16
    CELL_HEIGHT = 38

class PyTrace:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height = curses.LINES
        self.width = curses.COLS
        self.frame_buffer = [' ' for _ in range(self.height * self.width)]
        self.frames = 0
        self.elapsed = 0
        self.fps_estimate = 0

        self.scene = entity.Scene()
        self.sphere = Sphere(30)
        self.sphere2 = Sphere(10)
        self.scene.add_entity(self.sphere)
        self.scene.add_entity(self.sphere2)
        self.light = entity.Light()
        self.t = 0
        self.sphere2.position.y = 10
        self.sphere2.position.x = cos(self.t) * 50
        self.sphere2.position.z = sin(self.t) * 50
        self.light.position.y = -50
        self.light.position.x = cos(self.t / 20) * 100
        self.light.position.z = sin(self.t / 20) * 100
        self.light.position.x = 200
        self.light.position.z = 100
        self.scene.add_entity(self.light)
        self.camera = entity.Camera()
        self.camera.position.z = 20
        self.renderer = RayRenderer(self.width, self.height, self.frame_buffer)


    def begin(self):
        accumulator = 0
        last = time.time()
        while True:
            curr = time.time()
            frame_time = curr - last
            last = curr
            self.update_framerate(frame_time)

            accumulator += frame_time
            while accumulator >= Common.TIMESTEP:
                # self.handle_input()
                self.update(Common.TIMESTEP)
                accumulator -= Common.TIMESTEP
            self.render()
            self.swap_buffer()

    def update(self, dt):
        self.light.position.x = cos(self.t / 20) * 100
        self.light.position.z = sin(self.t / 20) * 100
        self.sphere2.position.x = cos(self.t) * 50
        self.sphere2.position.z = sin(self.t) * 50
        self.sphere2.position.y = cos(self.t / 1.5) * 10
        self.t += dt / 5

    def render(self):
        self.renderer.render(self.scene, self.camera)
        string = 'fps: {:.2f}, elapsed: {:.2f}'.format(self.fps_estimate, self.elapsed)
        self.frame_buffer[0:len(string)] = string

    def swap_buffer(self):
        self.stdscr.addstr(0, 0, ''.join(self.frame_buffer)[:-1])
        self.stdscr.refresh()

    def update_framerate(self, frame_time):
        self.frames += 1
        self.elapsed += frame_time
        if self.elapsed >= 1:
            self.fps_estimate = self.frames / self.elapsed
            self.frames = 0
            self.elapsed = 0

    # def handle_input(self):
        # c = self.stdscr.getch()
        # if c == ord('w'):
        #     self.camera.position.z -= 1
        # elif c == ord('s'):
        #     self.camera.position.z += 1
        # elif c == ord('a'):
        #     self.camera.position.x -= 1
        # elif c == ord('d'):
        #     self.camera.position.x += 1
        # elif c == ord(' '):
        #     self.camera.position.y += 1

def main(stdscr):
    os.system('echo "" > log.txt')
    curses.start_color()
    pt = PyTrace(stdscr)
    pt.begin()

if __name__ == '__main__':
    curses.wrapper(main)
