from __future__ import annotations

from .BFS import bfs
from .DFS import dfs
from .UCS import ucs
from .Greedy import greedy
from .a_star import astar

ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "Greedy": greedy,
    "A*": astar,
}


def compare_all(graph: dict, start: str, goal: str) -> list[dict]:
    results = []
    for name, fn in ALGORITHMS.items():
        r = fn(graph, start, goal)
        results.append({
            "algorithm": name,
            "path": r.path,
            "cost": r.cost,
            "steps": r.steps,
        })

    finite = [r["cost"] for r in results if r["path"]]
    optimal_cost = min(finite) if finite else float("inf")
    for r in results:
        r["optimal"] = bool(r["path"]) and r["cost"] == optimal_cost

    return results