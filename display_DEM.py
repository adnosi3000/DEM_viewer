import pygame
import numpy as np
from math import sin, cos
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 1500, 900
SCALE_XY = 1
SCALE_Z = 100
NMT_PATH = r"sample_DEM.xyz"
SPARSE_RATIO = 0.0008

def _project(proj_matrix, point3d):
    return np.dot(proj_matrix, point3d.T)[0:2]

def _global2pygame(x, y, w=WIDTH, h=HEIGHT, s=SCALE_XY):
    t = np.array([w/2, h/2])
    return np.array([x, -(y)])*s + t

def _rotate_scene(scene3D, x_angle=0, y_angle=0, z_angle=0):
    Rx = np.array([[1, 0, 0],
                      [0, cos(x_angle), -sin(x_angle)],
                      [0, sin(x_angle), cos(x_angle)]])
    Ry = np.array([[cos(y_angle), 0, sin(y_angle)],
                      [0, 1, 0],
                      [-sin(y_angle), 0, cos(y_angle)]])
    Rz = np.array([[cos(z_angle), -sin(z_angle), 0],
                      [sin(z_angle), cos(z_angle), 0],
                      [0, 0, 1]])

    R = np.dot(np.dot(Rz, Ry), Rx)

    return list(map(lambda x: (np.dot(R, x.T)).T, scene3D))

def _scale_scene3D(scene3D, s):
    assert s != 0, "Unable to scale by 0"
    return list(map(lambda v: np.array([v[0]*s, v[1]*s, v[2]*s]), scene3D))

def _normalize(value, value_max, value_min, a, b):
    return a + ((value - value_min)*(b-a))/(value_max - value_min)

def _read_scene(fp):
    points = []
    xs, ys, zs = [], [], []
    with open(fp) as f:
        for id, point in enumerate(f.readlines()):
            if random.random() >= SPARSE_RATIO:
                continue
            x, y, z = point.strip("\n").split()
            points.append(np.array([int(x.split('.')[0]), int(y.split('.')[0]), float(z)]))
            xs.append(int(x.split('.')[0]))
            ys.append(int(y.split('.')[0]))
            zs.append(int(z.split('.')[0]))

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    zmin, zmax = min(zs), max(zs)
    del xs, ys

    points = list(map(lambda v: np.array([_normalize(v[0], xmax, xmin, -WIDTH/2, WIDTH/2),
                                          _normalize(v[1], ymax, ymin, -HEIGHT/2, HEIGHT/2),
                                          _normalize(v[2], zmax, zmin, 0, SCALE_Z)]), points))

    print(f"Wczytano {len(points)} punktów")
    return points, zmin, zmax, zs

def _colorize(z, zmin, zmax):
    z = _normalize(z, zmax, zmin, 0, 5)
    if 0 <= z < 1:
        return (4, 143, 50)
    elif 1 <= z < 2:
        return (25, 143, 4)
    elif 2 <= z < 3:
        return (181, 166, 2)
    elif 3 <= z < 4:
        return (209, 92, 2)
    else:
        return (158, 22, 2)

scene3D, zmin, zmax, zs = _read_scene(NMT_PATH)

proj_matrix = np.array([[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 0]])


pygame.display.set_caption("NMT projection 3D")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_UP:
                scene3D = _rotate_scene(scene3D, x_angle=0.05)
            elif event.key == pygame.K_DOWN:
                scene3D = _rotate_scene(scene3D, x_angle=-0.05)
            elif event.key == pygame.K_LEFT:
                scene3D = _rotate_scene(scene3D, y_angle=-0.05)
            elif event.key == pygame.K_RIGHT:
                scene3D = _rotate_scene(scene3D, y_angle=0.05)
            elif event.key == pygame.K_COMMA:
                scene3D = _rotate_scene(scene3D, z_angle=-0.05)
            elif event.key == pygame.K_PERIOD:
                scene3D = _rotate_scene(scene3D, z_angle=0.05)
            elif event.key == pygame.K_EQUALS:
                scene3D = _scale_scene3D(scene3D, 1.05)
            elif event.key == pygame.K_MINUS:
                scene3D = _scale_scene3D(scene3D, 0.95)

    screen.fill(BLACK)

    scene2D_global = list(map(lambda x: _project(proj_matrix, x), scene3D))
    scene2D_pygame = list(map(lambda x: _global2pygame(*x), scene2D_global))

    for point, z in zip(scene2D_pygame, zs):
        pygame.draw.circle(screen, _colorize(z, zmin, zmax), point, 2)

    pygame.display.update()
