import heapq
from .rules import SearchResult, _reconstruct_path, _path_cost, _neighbors
from heuristic import h


def greedy(graph: dict, start: str, goal: str) -> SearchResult:
    cities = graph["cities"]
    counter = 0
    frontier = [(h(start, goal, cities), counter, start)]
    parent: dict[str, str | None] = {start: None}
    visited: set[str] = set()
    steps = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)

        if current in visited:
            continue
        visited.add(current)
        steps += 1

        if current == goal:
            path = _reconstruct_path(parent, start, goal)
            return SearchResult(path=path, cost=_path_cost(graph, path), steps=steps)

        for edge in _neighbors(graph, current):
            neighbor = edge["to"]
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current
                counter += 1
                heapq.heappush(frontier, (h(neighbor, goal, cities), counter, neighbor))

    return SearchResult(path=[], cost=float("inf"), steps=steps)