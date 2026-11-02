import heapq
from .rules import SearchResult, _reconstruct_path, _neighbors
from heuristic import h


def astar(graph: dict, start: str, goal: str) -> SearchResult:
    cities = graph["cities"]
    counter = 0
    frontier = [(h(start, goal, cities), counter, 0.0, start)]  # (f, tie, g, node)
    parent: dict[str, str | None] = {start: None}
    best_g: dict[str, float] = {start: 0.0}
    closed: set[str] = set()
    steps = 0

    while frontier:
        f, _, g, current = heapq.heappop(frontier)

        if current in closed:
            continue
        closed.add(current)
        steps += 1

        if current == goal:
            path = _reconstruct_path(parent, start, goal)
            return SearchResult(path=path, cost=g, steps=steps)

        for edge in _neighbors(graph, current):
            neighbor = edge["to"]
            new_g = g + edge["km"]
            if neighbor not in best_g or new_g < best_g[neighbor]:
                best_g[neighbor] = new_g
                parent[neighbor] = current
                counter += 1
                new_f = new_g + h(neighbor, goal, cities)
                heapq.heappush(frontier, (new_f, counter, new_g, neighbor))

    return SearchResult(path=[], cost=float("inf"), steps=steps)