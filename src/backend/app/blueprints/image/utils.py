import math


def color_distance_simple(color):
    white = (255, 255, 255)

    # Проверяем, что введенный цветвалидный RGB
    if not all(0 <= c <= 255 for c in color):
        raise ValueError("Значения цвета должны быть в диапазоне от 0 до 255")

    # Вычисляем расстояние
    distance = math.sqrt(
        (color[0] - white[0]) ** 2
        + (color[1] - white[1]) ** 2
        + (color[2] - white[2]) ** 2
    )
    return distance
