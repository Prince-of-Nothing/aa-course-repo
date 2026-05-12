from collections import defaultdict

class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed
        self.vertices = set()

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.vertices.add(u)
        self.vertices.add(v)

        if not self.directed:
            self.graph[v].append(u)

    def get_vertices_count(self):
        return len(self.vertices)

    def get_edges_count(self):
        count = sum(len(neighbors) for neighbors in self.graph.values())
        if not self.directed:
            count //= 2
        return count

def dfs_recursive(graph, start, visited=None):
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
    visited = set()
    stack = [start]
    traversal_order = []

    while stack:
        vertex = stack.pop()

        if vertex not in visited:
            visited.add(vertex)
            traversal_order.append(vertex)

            for neighbor in reversed(graph.graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return traversal_order

def dfs_all_vertices(graph, start=None):
    visited = set()
    traversal_order = []

    def dfs_helper(vertex):
        visited.add(vertex)
        traversal_order.append(vertex)

        for neighbor in graph.graph[vertex]:
            if neighbor not in visited:
                dfs_helper(neighbor)

    vertices_list = list(graph.vertices)
    if start is None and vertices_list:
        start = vertices_list[0]

    if start is not None:
        dfs_helper(start)

    for vertex in vertices_list:
        if vertex not in visited:
            dfs_helper(vertex)

    return traversal_order

if __name__ == "__main__":
    print("DFS Algorithm Demo")
    print("=" * 40)

    g = Graph()
    edges = [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)]

    for u, v in edges:
        g.add_edge(u, v)

    print(f"Graph has {g.get_vertices_count()} vertices and {g.get_edges_count()} edges")
    print(f"\nDFS starting from vertex 2:")
    print(f"Recursive: {dfs_recursive(g, 2)}")
    print(f"Iterative: {dfs_iterative(g, 2)}")
    print(f"All vertices: {dfs_all_vertices(g, 2)}")

