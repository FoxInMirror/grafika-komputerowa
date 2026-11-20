#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

LEVEL = 2
FACES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
CORNERS = ((1.5, 1.5, 1.5), (-1.5, -1.5, 1.5),
           (-1.5, 1.5, -1.5), (1.5, -1.5, -1.5))
triangles = []


def middle(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)


def build(tet, level):
    if level == 0:
        for i, j, k in FACES:
            triangles.append((tet[i], tet[j], tet[k]))
        return

    for corner in tet:
        build([middle(corner, p) for p in tet], level - 1)


def color(p):
    return (0.5 + 0.3 * p[0], 0.5 + 0.3 * p[1], 0.5 + 0.3 * p[2])


def vertex(p):
    glColor3f(*color(p))
    glVertex3f(*p)


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def startup():
    build(CORNERS, LEVEL)
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / math.pi)

    glBegin(GL_TRIANGLES)
    for a, b, c in triangles:
        vertex(a)
        vertex(b)
        vertex(c)
    glEnd()

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
        glOrtho(-3.5, 3.5, -3.5 / aspect_ratio, 3.5 / aspect_ratio, -10.0, 10.0)
    else:
        glOrtho(-3.5 * aspect_ratio, 3.5 * aspect_ratio, -3.5, 3.5, -10.0, 10.0)

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
