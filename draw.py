import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def draw_map(graph: dict, path: list[str] | None = None):
    path = path or []
    cities = graph["cities"]
    adjacency = graph["adjacency"]

    fig, ax = plt.subplots(figsize=(7, 8))
    ax.set_aspect("equal")
    ax.axis("off")

    path_edges = set()
    for a, b in zip(path, path[1:]):
        path_edges.add(tuple(sorted((a, b))))

    drawn = set()
    for frm, edges in adjacency.items():
        for e in edges:
            to, km = e["to"], e["km"]
            key = tuple(sorted((frm, to)))
            if key in drawn:
                continue
            drawn.add(key)

            x1, y1 = cities[frm]["x"], cities[frm]["y"]
            x2, y2 = cities[to]["x"], cities[to]["y"]
            is_path = key in path_edges

            ax.plot(
                [x1, x2], [y1, y2],
                color=("#e11d48" if is_path else "#94a3b8"),
                linewidth=(3.5 if is_path else 1.2),
                zorder=(3 if is_path else 1),
            )
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my, str(km), fontsize=7, color="#475569",
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
                    zorder=4)

    highlighted = set(path)
    for name, c in cities.items():
        is_hl = name in highlighted
        ax.scatter(
            c["x"], c["y"],
            s=(180 if is_hl else 90),
            c=("#f59e0b" if is_hl else "#0f766e"),
            edgecolors="white", linewidths=1.5, zorder=5,
        )
        ax.text(c["x"], c["y"] + 3.5, name, fontsize=8, fontweight="bold",
                ha="center", va="bottom", color="#1f2937", zorder=6)

    ax.set_title(graph.get("name", "Map"), fontsize=11, color="#0f766e")
    fig.tight_layout()
    return fig