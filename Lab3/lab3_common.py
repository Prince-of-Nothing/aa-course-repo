import csv
import os
import time
import tracemalloc
from collections import deque
from statistics import median

import pandas as pd

try:
    from graph_generator import Graph
    from graph_generator_extra import (
        bipartite_graph,
        classify_graph,
        complete_graph,
        cyclic_graph,
        dense_graph,
        disconnected_graph,
        grid_planar,
        make_demo_graphs,
        render_traversal_gif,
        simple_graph,
        strip_weights,
        tree,
        weighted_graph,
        wheel_graph,
    )
except ModuleNotFoundError:
    from .graph_generator import Graph
    from .graph_generator_extra import (
        bipartite_graph,
        classify_graph,
        complete_graph,
        cyclic_graph,
        dense_graph,
        disconnected_graph,
        grid_planar,
        make_demo_graphs,
        render_traversal_gif,
        simple_graph,
        strip_weights,
        tree,
        weighted_graph,
        wheel_graph,
    )


DEFAULT_SIZES = [10, 50, 100, 200, 500, 1000]
DEFAULT_DENSITIES = list(range(0, 101, 25))
DEFAULT_TRIALS = 5


def dfs_base(graph, start):
    visited = []
    order = []

    def visit_component(start_vertex):
        stack = [start_vertex]
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue

            visited.append(vertex)
            order.append(vertex)

            for neighbor in reversed(graph.graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)

    visit_component(start)
    for vertex in graph.vertices:
        if vertex not in visited:
            visit_component(vertex)

    return order


def bfs_base(graph, start):
    visited = []
    order = []

    def visit_component(start_vertex):
        visited.append(start_vertex)
        queue = [start_vertex]
        while queue:
            vertex = queue.pop(0)
            order.append(vertex)

            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)

    visit_component(start)
    for vertex in graph.vertices:
        if vertex not in visited:
            visit_component(vertex)

    return order


def dfs_optimized(graph, start):
    visited = set()
    order = []

    def visit_component(start_vertex):
        stack = [start_vertex]
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue

            visited.add(vertex)
            order.append(vertex)

            for neighbor in reversed(graph.graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)

    visit_component(start)
    for vertex in graph.vertices:
        if vertex not in visited:
            visit_component(vertex)

    return order


def bfs_optimized(graph, start):
    visited = set()
    order = []

    def visit_component(start_vertex):
        visited.add(start_vertex)
        queue = deque([start_vertex])
        while queue:
            vertex = queue.popleft()
            order.append(vertex)

            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    visit_component(start)
    for vertex in graph.vertices:
        if vertex not in visited:
            visit_component(vertex)

    return order


def generate_density_graph(num_vertices, density_percent):
    if not 0 <= density_percent <= 100:
        raise ValueError("density_percent must be from 0 to 100")

    graph = Graph(directed=False)
    for vertex in range(num_vertices):
        graph.add_vertex(vertex)

    max_edges = num_vertices * (num_vertices - 1) // 2
    target_edges = round((density_percent / 100) * max_edges)
    existing = set()

    for u in range(num_vertices):
        if len(existing) >= target_edges:
            break
        for v in range(u + 1, num_vertices):
            if len(existing) >= target_edges:
                break
            edge = (u, v)
            if edge not in existing:
                existing.add(edge)
                graph.add_edge(u, v)

    return graph


def density_cases(sizes=DEFAULT_SIZES, densities=DEFAULT_DENSITIES):
    for size in sizes:
        for density_percent in densities:
            graph = generate_density_graph(size, density_percent)
            label = f"Fill {density_percent}%"
            yield {
                "graph_type": "density_fill",
                "classification": classify_graph(graph, label),
                "density_percent": density_percent,
                "graph": graph,
            }


def topology_cases(sizes=DEFAULT_SIZES):
    topology_builders = {
        "simple_graph": simple_graph,
        "dense_graph": dense_graph,
        "tree": tree,
        "cyclic_graph": cyclic_graph,
        "bipartite_graph": bipartite_graph,
        "complete_graph": complete_graph,
        "wheel_graph": wheel_graph,
        "grid_planar": grid_planar,
        "weighted_graph": weighted_graph,
        "strip_weights": lambda n: strip_weights(weighted_graph(n)),
        "disconnected_graph": disconnected_graph,
    }

    make_demo_graphs()
    render_traversal_gif()

    for size in sizes:
        for graph_type, builder in topology_builders.items():
            graph = builder(size)
            yield {
                "graph_type": graph_type,
                "classification": classify_graph(graph, graph_type),
                "density_percent": round(graph.get_density() * 100, 2),
                "graph": graph,
            }


def benchmark(algorithm_name, algorithm, graph):
    start_vertex = next(iter(graph.vertices), None)
    if start_vertex is None:
        return {
            "algorithm": algorithm_name,
            "execution_time_ms": 0.0,
            "peak_memory_kb": 0.0,
            "vertices_visited": 0,
            "success": True,
        }

    tracemalloc.start()
    started = time.perf_counter()
    try:
        traversal = algorithm(graph, start_vertex)
        success = len(traversal) == graph.get_vertices_count()
    except Exception:
        traversal = []
        success = False
    elapsed_ms = (time.perf_counter() - started) * 1000
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": algorithm_name,
        "execution_time_ms": elapsed_ms,
        "peak_memory_kb": peak_memory / 1024,
        "vertices_visited": len(traversal),
        "success": success,
    }


def run_analysis(case_iterator, algorithms, trials=DEFAULT_TRIALS):
    rows = []

    for case in case_iterator:
        graph = case["graph"]
        for algorithm_name, algorithm in algorithms.items():
            trial_rows = []
            for trial in range(1, trials + 1):
                row = benchmark(algorithm_name, algorithm, graph)
                row.update(
                    {
                        "trial": trial,
                        "nodes": graph.get_vertices_count(),
                        "edges": graph.get_edges_count(),
                        "graph_type": case["graph_type"],
                        "classification": case["classification"],
                        "density_percent": case["density_percent"],
                    }
                )
                rows.append(row)
                trial_rows.append(row)

            good = [row for row in trial_rows if row["success"]]
            if good:
                print(
                    f"{case['graph_type']:18} {algorithm_name:14} "
                    f"V={graph.get_vertices_count():4} E={graph.get_edges_count():6} "
                    f"median={median(row['execution_time_ms'] for row in good):8.4f} ms"
                )

    return rows


def save_csv(rows, output_path):
    if not rows:
        return

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} rows to {output_path}")


def export_summary(rows, output_stem):
    if not rows:
        return

    df = pd.DataFrame(rows)
    summary = (
        df.groupby(["graph_type", "algorithm", "nodes"])
        .agg(
            median_time_ms=("execution_time_ms", "median"),
            median_memory_kb=("peak_memory_kb", "median"),
            median_vertices_visited=("vertices_visited", "median"),
            edges=("edges", "median"),
            density_percent=("density_percent", "median"),
            success_rate=("success", "mean"),
        )
        .reset_index()
    )

    summary_dir = os.path.join(os.path.dirname(output_stem), "summary")
    os.makedirs(summary_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(output_stem))[0]

    csv_path = os.path.join(summary_dir, f"{base_name}_summary.csv")
    txt_path = os.path.join(summary_dir, f"{base_name}_summary.txt")
    insights_path = os.path.join(summary_dir, f"{base_name}_insights.txt")

    summary.to_csv(csv_path, index=False)
    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(summary.to_string(index=False))

    avg_by_algorithm = summary.groupby("algorithm")["median_time_ms"].mean().sort_values()
    lines = [
        f"fastest average median-time algorithm: {avg_by_algorithm.index[0]}",
        f"slowest average median-time algorithm: {avg_by_algorithm.index[-1]}",
        f"spread between slowest and fastest: {(avg_by_algorithm.iloc[-1] / avg_by_algorithm.iloc[0]):.2f}x" if avg_by_algorithm.iloc[0] else "spread between slowest and fastest: n/a",
    ]
    with open(insights_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"Saved summary files for {base_name} in {summary_dir}")


BASE_ALGORITHMS = {
    "DFS_Base": dfs_base,
    "BFS_Base": bfs_base,
}

OPTIMIZED_ALGORITHMS = {
    "DFS_Optimized": dfs_optimized,
    "BFS_Optimized": bfs_optimized,
}
