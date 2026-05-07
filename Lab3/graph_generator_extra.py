import math
import random
from dataclasses import dataclass

try:
    from graph_generator import (
        Graph,
        generate_complete_graph,
        generate_cycle_graph,
        generate_dense_graph,
        generate_disconnected_graph,
        generate_grid_graph,
        generate_random_graph,
        generate_tree,
    )
except ModuleNotFoundError:
    from .graph_generator import (
        Graph,
        generate_complete_graph,
        generate_cycle_graph,
        generate_dense_graph,
        generate_disconnected_graph,
        generate_grid_graph,
        generate_random_graph,
        generate_tree,
    )


@dataclass(frozen=True)
class GraphCase:
    key: str
    label: str
    classification: str
    graph: Graph


def simple_graph(num_vertices, edge_probability=0.15, directed=False):
    return generate_random_graph(num_vertices, edge_probability, directed)


def dense_graph(num_vertices, edge_probability=0.70, directed=False):
    return generate_dense_graph(num_vertices, edge_probability, directed)


def tree(num_vertices):
    return generate_tree(num_vertices)


def cyclic_graph(num_vertices, directed=False):
    return generate_cycle_graph(num_vertices, directed)


def bipartite_graph(num_vertices, edge_probability=0.30, directed=False):
    g = Graph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)

    split = num_vertices // 2
    for left in range(split):
        for right in range(split, num_vertices):
            if random.random() < edge_probability:
                g.add_edge(left, right)

    return g


def complete_graph(num_vertices, directed=False):
    return generate_complete_graph(num_vertices, directed)


def wheel_graph(num_vertices, directed=False):
    g = Graph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)

    if num_vertices <= 1:
        return g

    for vertex in range(1, num_vertices):
        g.add_edge(0, vertex)

    for vertex in range(1, num_vertices):
        next_vertex = 1 if vertex == num_vertices - 1 else vertex + 1
        if vertex != next_vertex:
            g.add_edge(vertex, next_vertex)

    return g


def grid_planar(num_vertices, directed=False):
    if num_vertices <= 0:
        return generate_grid_graph(0, 0, directed)

    rows = max(1, int(math.sqrt(num_vertices)))
    cols = max(1, math.ceil(num_vertices / rows))
    grid = generate_grid_graph(rows, cols, directed)

    while grid.get_vertices_count() > num_vertices:
        victim = max(grid.vertices)
        grid.vertices.remove(victim)
        grid.graph.pop(victim, None)
        for neighbors in grid.graph.values():
            while victim in neighbors:
                neighbors.remove(victim)

    return grid


class WeightedGraph(Graph):
    def __init__(self, directed=False):
        super().__init__(directed)
        self.weights = {}

    def add_edge(self, u, v, weight=1):
        super().add_edge(u, v)
        self.weights[(u, v)] = weight
        if not self.directed:
            self.weights[(v, u)] = weight


def weighted_graph(num_vertices, edge_probability=0.30, directed=False):
    g = WeightedGraph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)

    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_probability:
                g.add_edge(i, j, random.randint(1, 100))

    return g


def strip_weights(weighted):
    g = Graph(directed=weighted.directed)
    for vertex in weighted.vertices:
        g.add_vertex(vertex)

    seen_edges = set()
    for u, neighbors in weighted.graph.items():
        for v in neighbors:
            edge = (u, v) if weighted.directed else tuple(sorted((u, v)))
            if edge in seen_edges:
                continue
            seen_edges.add(edge)
            g.add_edge(u, v)

    return g


def disconnected_graph(num_vertices, num_components=3, directed=False):
    return generate_disconnected_graph(num_vertices, num_components, directed)


def classify_graph(graph, declared_type):
    vertices = graph.get_vertices_count()
    edges = graph.get_edges_count()
    density = graph.get_density()
    weighted = hasattr(graph, "weights")

    if vertices == 0:
        connectivity = "empty"
    elif _visited_count(graph, next(iter(graph.vertices))) == vertices:
        connectivity = "connected"
    else:
        connectivity = "disconnected"

    density_band = "sparse" if density < 0.30 else "medium" if density < 0.70 else "dense"
    weight_band = "weighted" if weighted else "unweighted"
    direction_band = "directed" if graph.directed else "undirected"

    return (
        f"{declared_type}; {connectivity}; {density_band}; "
        f"{weight_band}; {direction_band}; V={vertices}; E={edges}; fill={density * 100:.2f}%"
    )


def make_demo_graphs(num_vertices=12):
    weighted = weighted_graph(num_vertices)
    cases = [
        ("simple_graph", "Simple Graph", simple_graph(num_vertices)),
        ("dense_graph", "Dense Graph", dense_graph(num_vertices)),
        ("tree", "Tree", tree(num_vertices)),
        ("cyclic_graph", "Cyclic Graph", cyclic_graph(num_vertices)),
        ("bipartite_graph", "Bipartite Graph", bipartite_graph(num_vertices)),
        ("complete_graph", "Complete Graph", complete_graph(num_vertices)),
        ("wheel_graph", "Wheel Graph", wheel_graph(num_vertices)),
        ("grid_planar", "Grid Planar", grid_planar(num_vertices)),
        ("weighted_graph", "Weighted Graph", weighted),
        ("strip_weights", "Stripped Weighted Graph", strip_weights(weighted)),
        ("disconnected_graph", "Disconnected Graph", disconnected_graph(num_vertices)),
    ]

    return [
        GraphCase(key=key, label=label, classification=classify_graph(graph, label), graph=graph)
        for key, label, graph in cases
    ]


def render_traversal_gif(graph=None, traversal=None, output_path=None):
    message = "Traversal GIF rendering is optional for the benchmark."
    if output_path:
        message += f" Requested output: {output_path}"
    return message


def _visited_count(graph, start):
    visited = {start}
    stack = [start]

    while stack:
        vertex = stack.pop()
        for neighbor in graph.graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return len(visited)


generate_bipartite_graph = bipartite_graph
generate_wheel_graph = wheel_graph
generate_weighted_graph = weighted_graph
