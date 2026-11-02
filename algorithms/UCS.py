from __future__ import annotations

import heapq

from rules import SearchResult, reconstruct_path, path_cost, neighbors


def ucs(graph: dict, start: str, goal: str) -> SearchResult:
    frontier: list[tuple[float, str, str]] = [(0.0, start, start)]
    best_g: dict[str, float] = {start: 0.0}
    explored: set[str] = set()
    parent: dict[str, str | None] = {start: None}
    steps = 0

    while frontier:
        g, _, node = heapq.heappop(frontier)
        if node in explored:
            continue
        explored.add(node)
        steps += 1

        if node == goal:
            path = reconstruct_path(parent, start, goal)
            return SearchResult(path, path_cost(graph, path), steps)

        for edge in neighbors(graph, node):
            to, km = edge["to"], edge["km"]
            if to in explored:
                continue
            new_g = g + km
            if to not in best_g or new_g < best_g[to]:
                best_g[to] = new_g
                parent[to] = node
                heapq.heappush(frontier, (new_g, to, to))

    return SearchResult([], float("inf"), steps)