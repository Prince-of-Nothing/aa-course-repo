from collections import defaultdict, deque

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

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    traversal_order = []

    while queue:
        vertex = queue.popleft()
        traversal_order.append(vertex)

        for neighbor in graph.graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return traversal_order

def bfs_with_levels(graph, start):
    visited = set()
    queue = deque([(start, 0)])
    visited.add(start)
    traversal_order = []
    levels = {start: 0}

    while queue:
        vertex, level = queue.popleft()
        traversal_order.append(vertex)

        for neighbor in graph.graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                levels[neighbor] = level + 1
                queue.append((neighbor, level + 1))

    return traversal_order, levels

def bfs_all_vertices(graph, start=None):
    visited = set()
    traversal_order = []

    def bfs_component(start_vertex):
        queue = deque([start_vertex])
        visited.add(start_vertex)

        while queue:
            vertex = queue.popleft()
            traversal_order.append(vertex)

            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    vertices_list = list(graph.vertices)
    if start is None and vertices_list:
        start = vertices_list[0]

    if start is not None:
        bfs_component(start)

    for vertex in vertices_list:
        if vertex not in visited:
            bfs_component(vertex)

    return traversal_order

def bfs_shortest_path(graph, start, end):
    if start == end:
        return [start]

    visited = set()
    queue = deque([(start, [start])])
    visited.add(start)

    while queue:
        vertex, path = queue.popleft()

        for neighbor in graph.graph[vertex]:
            if neighbor not in visited:
                new_path = path + [neighbor]

                if neighbor == end:
                    return new_path

                visited.add(neighbor)
                queue.append((neighbor, new_path))

    return None

if __name__ == "__main__":
    print("BFS Algorithm Demo")
    print("=" * 40)

    g = Graph()
    edges = [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)]

    for u, v in edges:
        g.add_edge(u, v)

    print(f"Graph has {g.get_vertices_count()} vertices and {g.get_edges_count()} edges")
    print(f"\nBFS starting from vertex 2:")
    print(f"Standard BFS: {bfs(g, 2)}")

    traversal, levels = bfs_with_levels(g, 2)
    print(f"BFS with levels: {traversal}")
    print(f"Vertex levels: {levels}")

    print(f"All vertices: {bfs_all_vertices(g, 2)}")

    print(f"\nShortest path from 0 to 3: {bfs_shortest_path(g, 0, 3)}")

