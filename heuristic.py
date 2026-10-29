import math


def h(city_name: str, goal_name: str, cities: dict) -> int:
    a = cities[city_name]
    b = cities[goal_name]
    dx = a["x"] - b["x"]
    dy = a["y"] - b["y"]
    return math.floor(math.sqrt(dx * dx + dy * dy))