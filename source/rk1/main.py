import time
import random
import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

"""
Алгоритм заполнения методом затравки:
1. Указывается затравочная точка;
2. Алгоритм проверяет, входит ли текущая точка в заданную область:
- Если точка входит в область и ещё не была заполнена, она добавляется в множество заполненных точек
  и итеративно обходит своих соседей;
- Если точка не принадлежит области или уже была обработана, обход не выполняется;
3. Заполнение: Повторяется процесс обхода и добавления точек, пока не заполнятся все точки внутри границ;
"""

def generate_polygon(num_vertices, grid_size):
    # Генерируем случайные уникальные вершины многоугольника
    points = set()
    
    while len(points) < num_vertices:
        x = random.randint(0, grid_size[0] - 1)
        y = random.randint(0, grid_size[1] - 1)
        points.add((x, y))
    
    # Преобразуем в список и сортируем по углу относительно центра
    points = list(points)
    
    return points


def fill_polygon_pyopengl(polygon, color=(1.0, 0.0, 0.0)):
    glClear(GL_COLOR_BUFFER_BIT) # Очистка буфера цвета
    
    glColor3f(*color) # Установка цвета заливки

    glBegin(GL_POLYGON) # Начало рисования многоугольника
    for x, y in polygon:
        glVertex2f(x / 500 - 1.0, y / 500 - 1.0)
    glEnd() # Конец рисования многоугольника

    # Заливка многоугольника
    glFlush() # Отображение изменений


def isPointInPolygon(point, polygon):
    x, y = point
    n = len(polygon)
    inter = 0

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        # Проверка пересечения луча с ребром
        if (y1 <= y < y2 or y2 <= y < y1) and \
            x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                inter += 1

    return inter % 2 == 1  # Нечетное количество пересечений означает, что точка внутри


def flood_fill(polygon, start_point, grid_size):
    filled_points = set()  # Множество для хранения заполненных точек
    queue = [start_point]

    # Проверяем, попадают ли вершины многоугольника в сетку
    for x, y in polygon:
        if 0 <= x < grid_size[1] and 0 <= y < grid_size[0]:
            filled_points.add((x, y))

    # Функция для заливки
    while queue:
        x, y = queue.pop()

        if (x, y) not in filled_points and 0 <= x < grid_size[1] and 0 <= y < grid_size[0] and isPointInPolygon((x, y), polygon):
            filled_points.add((x, y))

            # Добавляем соседние точки в очередь для дальнейшей проверки
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

    return filled_points


def fill_polygon(vertices, grid):
    start_vertex = vertices[0]
    filled_points = flood_fill(vertices, start_vertex, grid)

    # Формируем сетку для вывода
    grid_list = [[' ' for _ in range(grid[1])] for _ in range(grid[0])]

    for (x, y) in filled_points:
        if 0 <= x < grid[1] and 0 <= y < grid[0]:
            grid_list[int(y)][int(x)] = '#'


def compare_performance(num_polygons, num_vertices, grid):
    custom_times = []
    opengl_times = []

    for _ in range(num_polygons):
        vertices = generate_polygon(num_vertices, grid)

        # Измерение времени для собственного алгоритма
        start_time = time.time()
        fill_polygon(vertices, grid)
        custom_times.append(time.time() - start_time)

        # Измерение времени для OpenGL
        start_time = time.time()
        fill_polygon_pyopengl(vertices)
        opengl_times.append(time.time() - start_time)

    avg_custom_time = sum(custom_times) / num_polygons
    avg_opengl_time = sum(opengl_times) / num_polygons

    print(f"Avg time for custom algorithm: {avg_custom_time:.6f} seconds")
    print(f"Avg time for OpenGL method: {avg_opengl_time:.6f} seconds")


# Инициализация Pygame и OpenGL (Pygame работает через OpenGL)
pygame.init()
display = (1000, 1000)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

num_polygons = 1000  # Количество многоугольников для тестирования
num_vertices = 1000  # Количество вершин в многоугольнике

compare_performance(num_polygons, num_vertices, display)

pygame.quit()