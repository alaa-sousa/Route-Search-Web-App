from __future__ import annotations

import heapq

from heuristic import h
from rules import SearchResult, reconstruct_path, path_cost, neighbors


def greedy(graph: dict, start: str, goal: str) -> SearchResult:
    cities = graph["cities"]
    frontier: list[tuple[float, str, str]] = [(h(start, goal, cities), start, start)]
    in_frontier = {start}
    explored: set[str] = set()
    parent: dict[str, str | None] = {start: None}
    steps = 0

    while frontier:
        _, _, node = heapq.heappop(frontier)
        in_frontier.discard(node)
        if node in explored:
            continue
        explored.add(node)
        steps += 1

        if node == goal:
            path = reconstruct_path(parent, start, goal)
            return SearchResult(path, path_cost(graph, path), steps)

        for edge in neighbors(graph, node):
            to = edge["to"]
            if to not in explored and to not in in_frontier:
                parent[to] = node
                heapq.heappush(frontier, (h(to, goal, cities), to, to))
                in_frontier.add(to)

    return SearchResult([], float("inf"), steps)