#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 40
vertices = []
colors = []


def egg(u, v):
    r = -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u
    x = r * math.cos(math.pi * v)
    y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
    z = r * math.sin(math.pi * v)
    return (x, y, z)


def build():
    for i in range(N):
        u = i / (N - 1)
        row_v = []
        row_c = []
        for j in range(N):
            v = j / (N - 1)
            row_v.append(egg(u, v))
            row_c.append((random.random(), random.random(), random.random()))
        vertices.append(row_v)
        colors.append(row_c)


def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def vertex(p, c):
    glColor3f(*c)
    glVertex3f(*p)


def egg_triangles():
    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            vertex(vertices[i][j], colors[i][j])
            vertex(vertices[i + 1][j], colors[i + 1][j])
            vertex(vertices[i + 1][j + 1], colors[i + 1][j + 1])
            vertex(vertices[i][j], colors[i][j])
            vertex(vertices[i + 1][j + 1], colors[i + 1][j + 1])
            vertex(vertices[i][j + 1], colors[i][j + 1])
    glEnd()


def startup():
    build()
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / math.pi)
    axes()
    egg_triangles()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, -20.0, 20.0)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, -20.0, 20.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
