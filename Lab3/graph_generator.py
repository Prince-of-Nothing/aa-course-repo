"""
Graph Generator for DFS/BFS Empirical Analysis
Laboratory Work 3

Generates various types of graphs for testing:
- Random graphs with configurable density
- Sparse graphs
- Dense graphs
- Complete graphs
- Tree structures
- Disconnected graphs
"""

import random
from collections import defaultdict


class Graph:
    """Graph class using adjacency list representation"""

    def __init__(self, directed=False):
        """
        Initialize graph

        Args:
            directed: If True, creates a directed graph; otherwise undirected
        """
        self.graph = defaultdict(list)
        self.directed = directed
        self.vertices = set()

    def add_edge(self, u, v):
        """Add an edge from vertex u to vertex v"""
        self.graph[u].append(v)
        self.vertices.add(u)
        self.vertices.add(v)

        if not self.directed:
            self.graph[v].append(u)

    def add_vertex(self, v):
        """Add a vertex without any edges"""
        self.vertices.add(v)

    def get_vertices_count(self):
        """Return the number of vertices"""
        return len(self.vertices)

    def get_edges_count(self):
        """Return the number of edges"""
        count = sum(len(neighbors) for neighbors in self.graph.values())
        if not self.directed:
            count //= 2
        return count

    def get_density(self):
        """Return the density of the graph (edges / max possible edges)"""
        n = self.get_vertices_count()
        if n <= 1:
            return 0.0
        max_edges = n * (n - 1) // 2 if not self.directed else n * (n - 1)
        return self.get_edges_count() / max_edges if max_edges > 0 else 0.0


def generate_random_graph(num_vertices, edge_probability=0.3, directed=False):
    """
    Generate a random graph using Erdos-Renyi model

    Args:
        num_vertices: Number of vertices
        edge_probability: Probability of edge creation between any two vertices
        directed: If True, creates a directed graph

    Returns:
        Graph object
    """
    g = Graph(directed=directed)

    # Add all vertices
    for i in range(num_vertices):
        g.add_vertex(i)

    # Add edges with given probability
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_probability:
                g.add_edge(i, j)

    return g


def generate_sparse_graph(num_vertices, directed=False):
    """
    Generate a sparse graph (approximately n edges for n vertices)

    Args:
        num_vertices: Number of vertices
        directed: If True, creates a directed graph

    Returns:
        Graph object
    """
    g = Graph(directed=directed)

    for i in range(num_vertices):
        g.add_vertex(i)

    # Create a spanning tree to ensure connectivity
    for i in range(1, num_vertices):
        parent = random.randint(0, i - 1)
        g.add_edge(parent, i)

    # Add a few extra edges
    extra_edges = num_vertices // 10
    for _ in range(extra_edges):
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)
        if u != v:
            g.add_edge(u, v)

    return g


def generate_dense_graph(num_vertices, density=0.7, directed=False):
    """
    Generate a dense graph with high edge probability

    Args:
        num_vertices: Number of vertices
        density: Target density (0.0 to 1.0)
        directed: If True, creates a directed graph

    Returns:
        Graph object
    """
    return generate_random_graph(num_vertices, edge_probability=density, directed=directed)


def generate_complete_graph(num_vertices, directed=False):
    """
    Generate a complete graph (every vertex connected to every other vertex)

    Args:
        num_vertices: Number of vertices
        directed: If True, creates a directed graph

    Returns:
        Graph object
    """
    g = Graph(directed=directed)

    for i in range(num_vertices):
        g.add_vertex(i)

    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            g.add_edge(i, j)

    return g


def generate_tree(num_vertices):
    """
    Generate a random tree with n vertices

    Args:
        num_vertices: Number of vertices

    Returns:
        Graph object (undirected)
    """
    g = Graph(directed=False)

    for i in range(num_vertices):
        g.add_vertex(i)

    # Each vertex (except root) connects to a random existing vertex
    for i in range(1, num_vertices):
        parent = random.randint(0, i - 1)
        g.add_edge(parent, i)

    return g


def generate_binary_tree(depth):
    """
    Generate a complete binary tree with given depth

    Args:
        depth: Depth of the tree (0 = just root)

    Returns:
        Graph object (undirected)
    """
    g = Graph(directed=False)
    num_vertices = (2 ** (depth + 1)) - 1

    for i in range(num_vertices):
        g.add_vertex(i)

    for i in range(num_vertices):
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        if left_child < num_vertices:
            g.add_edge(i, left_child)
        if right_child < num_vertices:
            g.add_edge(i, right_child)

    return g


def generate_linear_graph(num_vertices, directed=False):
    """
    Generate a linear (path) graph

    Args:
        num_vertices: Number of vertices
        directed: If True, creates a directed graph

    Returns:
        Graph object
    """
    g = Graph(directed=directed)

    for i in range(num_vertices):
        g.add_vertex(i)

    for i in range(num_vertices - 1):
        g.add_edge(i, i + 1)

    return g


def generate_cycle_graph(num_vertices, directed=False):
    """
    Generate a cycle graph

    Args:
        num_vertices: Number of vertices
        directed: If True, creates a directed graph

    Returns:
        Graph object
    """
    g = generate_linear_graph(num_vertices, directed)

    if num_vertices > 2:
        g.add_edge(num_vertices - 1, 0)

    return g


def generate_grid_graph(rows, cols, directed=False):
    """
    Generate a 2D grid graph

    Args:
        rows: Number of rows
        cols: Number of columns
        directed: If True, creates a directed graph

    Returns:
        Graph object
    """
    g = Graph(directed=directed)

    # Add vertices
    for i in range(rows * cols):
        g.add_vertex(i)

    # Add edges
    for r in range(rows):
        for c in range(cols):
            vertex = r * cols + c

            # Right neighbor
            if c < cols - 1:
                g.add_edge(vertex, vertex + 1)

            # Bottom neighbor
            if r < rows - 1:
                g.add_edge(vertex, vertex + cols)

    return g


def generate_disconnected_graph(num_vertices, num_components=3, directed=False):
    """
    Generate a disconnected graph with multiple components

    Args:
        num_vertices: Total number of vertices
        num_components: Number of disconnected components
        directed: If True, creates a directed graph

    Returns:
        Graph object
    """
    g = Graph(directed=directed)

    vertices_per_component = num_vertices // num_components
    remainder = num_vertices % num_components

    current_vertex = 0

    for component in range(num_components):
        component_size = vertices_per_component + (1 if component < remainder else 0)

        if component_size <= 0:
            continue

        # Add vertices for this component
        component_vertices = list(range(current_vertex, current_vertex + component_size))
        for v in component_vertices:
            g.add_vertex(v)

        # Create a random subgraph within the component
        for i, v in enumerate(component_vertices):
            if i > 0:
                # Connect to a random earlier vertex in the same component
                u = component_vertices[random.randint(0, i - 1)]
                g.add_edge(u, v)

        current_vertex += component_size

    return g


def generate_star_graph(num_vertices, directed=False):
    """
    Generate a star graph (one central vertex connected to all others)

    Args:
        num_vertices: Number of vertices
        directed: If True, creates a directed graph

    Returns:
        Graph object
    """
    g = Graph(directed=directed)

    for i in range(num_vertices):
        g.add_vertex(i)

    # Vertex 0 is the center
    for i in range(1, num_vertices):
        g.add_edge(0, i)

    return g


if __name__ == "__main__":
    # Demo usage
    print("Graph Generator Demo")
    print("=" * 50)

    generators = [
        ("Random Graph (n=100, p=0.3)", lambda: generate_random_graph(100, 0.3)),
        ("Sparse Graph (n=100)", lambda: generate_sparse_graph(100)),
        ("Dense Graph (n=100, d=0.7)", lambda: generate_dense_graph(100, 0.7)),
        ("Complete Graph (n=50)", lambda: generate_complete_graph(50)),
        ("Tree (n=100)", lambda: generate_tree(100)),
        ("Binary Tree (depth=6)", lambda: generate_binary_tree(6)),
        ("Linear Graph (n=100)", lambda: generate_linear_graph(100)),
        ("Cycle Graph (n=100)", lambda: generate_cycle_graph(100)),
        ("Grid Graph (10x10)", lambda: generate_grid_graph(10, 10)),
        ("Disconnected Graph (n=100, c=3)", lambda: generate_disconnected_graph(100, 3)),
        ("Star Graph (n=100)", lambda: generate_star_graph(100)),
    ]

    for name, generator in generators:
        g = generator()
        print(f"{name}")
        print(f"  Vertices: {g.get_vertices_count()}, Edges: {g.get_edges_count()}, Density: {g.get_density():.4f}")
