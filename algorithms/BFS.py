from collections import deque
from .rules import SearchResult, _reconstruct_path, _path_cost, _neighbors


def bfs(graph: dict, start: str, goal: str) -> SearchResult:
    queue = deque([start])
    parent: dict[str, str | None] = {start: None}
    steps = 0

    while queue:
        current = queue.popleft()
        steps += 1

        if current == goal:
            path = _reconstruct_path(parent, start, goal)
            return SearchResult(path=path, cost=_path_cost(graph, path), steps=steps)

        for edge in _neighbors(graph, current):
            neighbor = edge["to"]
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    return SearchResult(path=[], cost=float("inf"), steps=steps)