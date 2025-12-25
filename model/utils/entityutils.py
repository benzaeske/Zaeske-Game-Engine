from typing import Tuple

from pygame import Vector2

def calculate_shortest_distance_and_virtual_position(point1: Vector2, point2: Vector2, world_width: float) -> Tuple[float, Vector2]:
    """
    Calculates and returns the shortest distance between two points.
    Calculates the direct distance between the points and then compares that to the distance between the points if the second point is wrapped around the x-axis of the world map.
    If the wrapped distance is less than the direct distance, it returns the second point at its 'virtual' wrapped location, otherwise it returns the second point unmodified.
    """
    direct_d: float = point1.distance_to(point2)
    wrap_pos: Vector2 = point2 + Vector2(world_width, 0) if point2.x < (
                world_width / 2) else point2 - Vector2(world_width, 0)
    wrap_d: float = point1.distance_to(wrap_pos)
    if direct_d < wrap_d:
        return direct_d, point2
    else:
        return wrap_d, wrap_pos