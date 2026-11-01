from .rules import SearchResult, _reconstruct_path, _path_cost, _neighbors


def dfs(graph: dict, start: str, goal: str) -> SearchResult:
    stack = [(start, None)]
    parent: dict[str, str | None] = {}
    steps = 0

    while stack:
        current, prev = stack.pop()

        if current in parent:
            continue
        parent[current] = prev
        steps += 1

        if current == goal:
            path = _reconstruct_path(parent, start, goal)
            return SearchResult(path=path, cost=_path_cost(graph, path), steps=steps)

        for edge in reversed(_neighbors(graph, current)):
            neighbor = edge["to"]
            if neighbor not in parent:
                stack.append((neighbor, current))

    return SearchResult(path=[], cost=float("inf"), steps=steps)