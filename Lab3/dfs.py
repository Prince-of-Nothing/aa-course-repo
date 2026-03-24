"""
Depth First Search (DFS) Algorithm Implementation
Laboratory Work 3: Empirical Analysis of Graph Traversal Algorithms

DFS explores as far as possible along each branch before backtracking.
Time Complexity: O(V + E) where V is vertices and E is edges
Space Complexity: O(V) for the visited set and recursion stack
"""

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

    def get_vertices_count(self):
        """Return the number of vertices"""
        return len(self.vertices)

    def get_edges_count(self):
        """Return the number of edges"""
        count = sum(len(neighbors) for neighbors in self.graph.values())
        if not self.directed:
            count //= 2
        return count


def dfs_recursive(graph, start, visited=None):
    """
    Depth First Search - Recursive Implementation

    Args:
        graph: Graph object with adjacency list
        start: Starting vertex
        visited: Set of visited vertices (used internally)

    Returns:
        List of vertices in DFS traversal order
    """
    if visited is None:
        visited = set()

    traversal_order = []

    def dfs_helper(vertex):
        visited.add(vertex)
        traversal_order.append(vertex)

        for neighbor in graph.graph[vertex]:
            if neighbor not in visited:
                dfs_helper(neighbor)

    dfs_helper(start)
    return traversal_order


def dfs_iterative(graph, start):
    """
    Depth First Search - Iterative Implementation using Stack

    Args:
        graph: Graph object with adjacency list
        start: Starting vertex

    Returns:
        List of vertices in DFS traversal order
    """
    visited = set()
    stack = [start]
    traversal_order = []

    while stack:
        vertex = stack.pop()

        if vertex not in visited:
            visited.add(vertex)
            traversal_order.append(vertex)

            # Add neighbors to stack in reverse order to maintain left-to-right traversal
            for neighbor in reversed(graph.graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return traversal_order


def dfs_all_vertices(graph, start=None):
    """
    DFS that visits all vertices in the graph (handles disconnected components)

    Args:
        graph: Graph object with adjacency list
        start: Optional starting vertex

    Returns:
        List of vertices in DFS traversal order
    """
    visited = set()
    traversal_order = []

    def dfs_helper(vertex):
        visited.add(vertex)
        traversal_order.append(vertex)

        for neighbor in graph.graph[vertex]:
            if neighbor not in visited:
                dfs_helper(neighbor)

    # Start from specified vertex or first vertex
    vertices_list = list(graph.vertices)
    if start is None and vertices_list:
        start = vertices_list[0]

    if start is not None:
        dfs_helper(start)

    # Visit remaining unvisited vertices (disconnected components)
    for vertex in vertices_list:
        if vertex not in visited:
            dfs_helper(vertex)

    return traversal_order


if __name__ == "__main__":
    # Demo usage
    print("DFS Algorithm Demo")
    print("=" * 40)

    # Create a sample graph
    g = Graph()
    edges = [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)]

    for u, v in edges:
        g.add_edge(u, v)

    print(f"Graph has {g.get_vertices_count()} vertices and {g.get_edges_count()} edges")
    print(f"\nDFS starting from vertex 2:")
    print(f"Recursive: {dfs_recursive(g, 2)}")
    print(f"Iterative: {dfs_iterative(g, 2)}")
    print(f"All vertices: {dfs_all_vertices(g, 2)}")
