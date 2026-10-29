from __future__ import annotations

from dataclasses import dataclass

@dataclass
class SearchResult:
    path: list[str]
    cost: float
    steps: int


def _reconstruct_path(parent: dict[str, str | None], start: str, goal: str) -> list[str]:
    path: list[str] = []
    cur: str | None = goal
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = parent[cur]
    path.reverse()
    return path


def _path_cost(graph: dict, path: list[str]) -> float:
    total = 0.0
    for a, b in zip(path, path[1:]):
        edge = next(e for e in graph["adjacency"][a] if e["to"] == b)
        total += edge["km"]
    return total


def _neighbors(graph: dict, city: str) -> list[dict]:
    return graph["adjacency"][city]
