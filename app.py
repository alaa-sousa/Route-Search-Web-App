from __future__ import annotations

import io
import json

import streamlit as st

from algorithms.compare_All import ALGORITHMS, compare_all
from draw import draw_map
from graph_utils import (
    build_graph,
    load_default_map,
    load_map_from_json_bytes,
    validate_map,
)

st.set_page_config(page_title="Route Search — West Bank", page_icon="🗺️", layout="wide")


@st.cache_data(show_spinner=False)
def get_default_map():
    return load_default_map("data/westbank_map.json")


def _ensure_state():
    if "graph" not in st.session_state:
        st.session_state.graph = get_default_map()
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "compare_results" not in st.session_state:
        st.session_state.compare_results = None


def _reset_results():
    st.session_state.last_result = None
    st.session_state.compare_results = None


_ensure_state()


st.title("🗺️ Route Search Web App")
st.caption("Fundamentals of Artificial Intelligence — Assignment 1")


with st.sidebar:
    st.header("Map")
    st.write(f"**Current:** {st.session_state.graph['name']}")

    uploaded = st.file_uploader("Upload new map (JSON)", type=["json"])
    if uploaded is not None:
        try:
            new_graph = load_map_from_json_bytes(uploaded.getvalue())
            if st.button("Use this map", type="primary", use_container_width=True):
                st.session_state.graph = new_graph
                _reset_results()
                st.success("Map loaded successfully.")
                st.rerun()
        except Exception as e:
            st.error(f"Invalid map:\n\n{e}")

    st.divider()
    st.subheader("Rules")
    st.markdown(
        "- Heuristic **h(n)** = straight-line distance to goal (floored).\n"
        "- Ties broken **alphabetically**.\n"
        "- Goal test applied **when a node is removed** from the frontier.\n"
        "- **Graph search**: a city is never expanded twice.\n"
        "- **Steps** = nodes removed from the frontier and expanded."
    )


graph = st.session_state.graph
city_names = sorted(graph["cities"].keys())

col1, col2, col3 = st.columns(3)
with col1:
    start = st.selectbox("Start city", city_names, index=0)
with col2:
    goal = st.selectbox("Goal city", city_names, index=len(city_names) - 1)
with col3:
    algorithm = st.selectbox("Algorithm", list(ALGORITHMS.keys()))

col_btn1, col_btn2, _ = st.columns([1, 1, 2])
with col_btn1:
    do_search = st.button("🔍 Search", type="primary", use_container_width=True)
with col_btn2:
    do_compare = st.button("⚖️ Compare All", use_container_width=True)


if do_search:
    result = ALGORITHMS[algorithm](graph, start, goal)
    st.session_state.last_result = {
        "algorithm": algorithm,
        "start": start,
        "goal": goal,
        "path": result.path,
        "cost": result.cost,
        "steps": result.steps,
    }
    st.session_state.compare_results = None

if do_compare:
    st.session_state.compare_results = compare_all(graph, start, goal)
    st.session_state.last_result = None


st.subheader("Result")

last = st.session_state.last_result
if last:
    if not last["path"]:
        st.error(f"No path found by **{last['algorithm']}** from **{last['start']}** to **{last['goal']}**.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Algorithm", last["algorithm"])
        m2.metric("Total cost", f"{last['cost']:.0f} km")
        m3.metric("Steps", last["steps"])
        st.markdown("**Path:**")
        st.code(" → ".join(last["path"]), language=None)
else:
    st.info("Choose start, goal, and algorithm, then click **Search** (or **Compare All**).")


compare_results = st.session_state.compare_results
if compare_results:
    st.subheader("Comparison")
    import pandas as pd
    rows = []
    for r in compare_results:
        rows.append({
            "Algorithm": r["algorithm"],
            "Path": " → ".join(r["path"]) if r["path"] else "—",
            "Cost (km)": "∞" if r["cost"] == float("inf") else f"{r['cost']:.0f}",
            "Steps": r["steps"],
            "Optimal": "✅" if r["optimal"] else "",
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


st.subheader("Map")
path_for_drawing = []
if st.session_state.last_result and st.session_state.last_result["path"]:
    path_for_drawing = st.session_state.last_result["path"]

fig = draw_map(graph, path_for_drawing)
st.pyplot(fig, use_container_width=True)