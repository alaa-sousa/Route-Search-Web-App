import heapq
from .rules import SearchResult, _reconstruct_path, _neighbors


def ucs(graph: dict, start: str, goal: str) -> SearchResult:
    counter = 0                      # tie-breaker so heap never compares strings
    frontier = [(0.0, counter, start)]
    parent: dict[str, str | None] = {start: None}
    best_g: dict[str, float] = {start: 0.0}
    closed: set[str] = set()
    steps = 0

    while frontier:
        g, _, current = heapq.heappop(frontier)

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
                heapq.heappush(frontier, (new_g, counter, neighbor))

    return SearchResult(path=[], cost=float("inf"), steps=steps)