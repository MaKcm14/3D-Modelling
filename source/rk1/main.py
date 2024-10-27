import time
import numpy as np
import random
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

def fill_polygon_opengl(vertices):
    # Заполнение многоугольника с использованием PyOpenGL
    glBegin(GL_POLYGON)
    for vertex in vertices:
        glVertex2f(vertex[0], vertex[1])
    glEnd()


def generate_polygon(num_vertices, grid_size):
    # Генерируем случайные уникальные вершины многоугольника
    points = set()
    
    while len(points) < num_vertices:
        x = random.randint(0, grid_size[0] - 1)
        y = random.randint(0, grid_size[1] - 1)
        points.add((x, y))
    
    # Преобразуем в список и сортируем по углу относительно центра
    points = list(points)
    
    # Находим центр для сортировки по углу
    center = (sum(x for x, y in points) / num_vertices, 
              sum(y for x, y in points) / num_vertices)
    
    # Сортируем точки по углу
    points.sort(key=lambda point: (point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2)
    
    return points


def flood_fill(polygon, start_point, grid_size=(800, 600)):
    filled_points = set()  # Множество для хранения заполненных точек
    queue = [start_point]

    # Проверяем, попадают ли вершины многоугольника в сетку
    for x, y in polygon:
        if 0 <= x < grid_size[1] and 0 <= y < grid_size[0]:
            filled_points.add((x, y))

    # Функция для заливки
    while queue:
        x, y = queue.pop()

        if (x, y) not in filled_points and 0 <= x < grid_size[1] and 0 <= y < grid_size[0]:
            filled_points.add((x, y))

            # Добавляем соседние точки в очередь
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

    return filled_points


def fill_polygon(vertices):
    # Начинаем заливку с первой вершины
    start_vertex = vertices[0]
    filled_points = flood_fill(vertices, start_vertex)

    # Формируем сетку для вывода
    grid_size = (800, 600)
    grid = [[' ' for _ in range(grid_size[1])] for _ in range(grid_size[0])]

    for (x, y) in filled_points:
        if 0 <= x < grid_size[1] and 0 <= y < grid_size[0]:
            grid[int(y)][int(x)] = '#'


def compare_performance(num_polygons, num_vertices, grid):
    custom_times = []
    opengl_times = []

    for _ in range(num_polygons):
        vertices = generate_polygon(num_vertices, grid)

        # Измерение времени для собственного алгоритма
        start_time = time.time()
        fill_polygon(vertices)
        custom_times.append(time.time() - start_time)

        # Измерение времени для OpenGL
        start_time = time.time()
        fill_polygon_opengl(vertices)
        opengl_times.append(time.time() - start_time)

    avg_custom_time = sum(custom_times) / num_polygons
    avg_opengl_time = sum(opengl_times) / num_polygons

    print(f"Avg time for custom algorithm: {avg_custom_time:.6f} seconds")
    print(f"Avg time for OpenGL method: {avg_opengl_time:.6f} seconds")


# Инициализация Pygame и OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
gluOrtho2D(-1, 1, -1, 1)

num_polygons = 1000  # Количество многоугольников для тестирования
num_vertices = 1000  # Количество вершин в многоугольнике

compare_performance(num_polygons, num_vertices, display)

pygame.quit()