#!/usr/bin/env python3
# Laboratorium 2 - OpenGL 2D.
# Uruchomienie: python Laboratorium 2 - Oliwier Urbański.py
#
#   1 - trojkat z trzema kolorami
#   2 - prostokaty z losowymi kolorami i deformacja
#   3 - dywan Sierpinskiego
#   4 - trojkat Sierpinskiego

import random
import sys

from glfw.GLFW import *
from OpenGL.GL import *

DEPTH = 8

SCENE = 2  # aktualnie rysowana scena

DISTORTION = 0.2

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass


def draw_color_triangle():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-100.0, -100.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(100.0, -100.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-100.0, 100.0)
    glEnd()


def draw_rectangle(x, y, a, b, d=0.0):
    if d > 0.0:
        a = a * ((1-d))
        b = b * ((1-d))

    glBegin(GL_TRIANGLES)
    # trojkat pierwszy
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a, y)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a, y + b)
    # trojkat drugi
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a, y + b)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y + b)
    glEnd()

def draw_sierpinski_carpet(x, y, size, depth):
    if depth <= 0:
        draw_rectangle(x, y, size, size)
        return

    step = size / 3.0
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            draw_sierpinski_carpet(x + i * step, y + j * step, step, depth - 1)

def draw_sierpinski_triangle(x1, y1, x2, y2, x3, y3, depth):
    if depth <= 0:
        glColor3f(random.random(), random.random(), random.random())
        glBegin(GL_TRIANGLES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glVertex2f(x3, y3)
        glEnd()
        return

    # srodki bokow
    mx12, my12 = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    mx23, my23 = (x2 + x3) / 2.0, (y2 + y3) / 2.0
    mx31, my31 = (x3 + x1) / 2.0, (y3 + y1) / 2.0

    draw_sierpinski_triangle(x1, y1, mx12, my12, mx31, my31, depth - 1)
    draw_sierpinski_triangle(mx12, my12, x2, y2, mx23, my23, depth - 1)
    draw_sierpinski_triangle(mx31, my31, mx23, my23, x3, y3, depth - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    if SCENE == 1:
        draw_color_triangle()
    elif SCENE == 2:
        draw_rectangle(0, 0, 100,100, DISTORTION)
    elif SCENE == 3:
        draw_sierpinski_carpet(-100, -100, 200, DEPTH)
    else:
        draw_sierpinski_triangle(-80, -80, 80, -80, 0, 80, DEPTH)

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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

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
