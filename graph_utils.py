import json
from pathlib import Path


def validate_map(data: dict) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["Map must be a JSON object."]

    cities = data.get("cities")
    roads = data.get("roads")

    if not isinstance(cities, list) or not cities:
        errors.append("'cities' must be a non-empty array.")
        return errors
    if not isinstance(roads, list):
        errors.append("'roads' must be an array.")
        return errors

    city_names: set[str] = set()
    for i, c in enumerate(cities):
        if not isinstance(c, dict):
            errors.append(f"City #{i} must be an object.")
            continue
        name = c.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"City #{i} must have a non-empty 'name'.")
            continue
        if not isinstance(c.get("x"), (int, float)) or not isinstance(c.get("y"), (int, float)):
            errors.append(f"City '{name}' must have numeric 'x' and 'y'.")
        if name in city_names:
            errors.append(f"Duplicate city name: '{name}'.")
        city_names.add(name)

    for i, r in enumerate(roads):
        if not isinstance(r, dict):
            errors.append(f"Road #{i} must be an object.")
            continue
        frm = r.get("from")
        to = r.get("to")
        km = r.get("km")
        if frm not in city_names:
            errors.append(f"Road #{i} references unknown city: '{frm}'.")
        if to not in city_names:
            errors.append(f"Road #{i} references unknown city: '{to}'.")
        if not isinstance(km, (int, float)) or km <= 0:
            errors.append(f"Road {frm}->{to} must have positive numeric 'km'.")

    return errors


def build_graph(data: dict) -> dict:
    cities = {c["name"]: {"x": c["x"], "y": c["y"]} for c in data["cities"]}
    adjacency: dict[str, list[dict]] = {name: [] for name in cities}

    for r in data["roads"]:
        frm, to, km = r["from"], r["to"], r["km"]
        adjacency[frm].append({"to": to, "km": km})
        adjacency[to].append({"to": frm, "km": km})

    for name in adjacency:
        adjacency[name].sort(key=lambda e: e["to"])

    return {
        "name": data.get("name", "Map"),
        "unit": data.get("unit", "km"),
        "cities": cities,
        "adjacency": adjacency,
    }


def load_map_from_json_bytes(raw: bytes) -> dict:
    data = json.loads(raw.decode("utf-8"))
    errors = validate_map(data)
    if errors:
        raise ValueError("\n".join(errors))
    return build_graph(data)


def load_default_map(path: str | Path = "data/westbank_map.json") -> dict:
    raw = Path(path).read_bytes()
    return load_map_from_json_bytes(raw)