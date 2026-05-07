try:
    from graph_utils import WeightedEdge
except ModuleNotFoundError:
    from .graph_utils import WeightedEdge


def kruskal_classic(graph):
    components = [{vertex} for vertex in range(graph.num_vertices)]
    total_weight = 0

    for edge in sorted(graph.edges):
        left_index = next(i for i, comp in enumerate(components) if edge.source in comp)
        right_index = next(i for i, comp in enumerate(components) if edge.target in comp)

        if left_index == right_index:
            continue

        total_weight += edge.weight
        merged = components[left_index] | components[right_index]
        components[left_index] = merged
        components.pop(right_index)

        if len(components) == 1:
            break

    return total_weight


def kruskal_optimized(graph):
    parent = list(range(graph.num_vertices))
    rank = [0] * graph.num_vertices
    total_weight = 0

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(left, right):
        root_left = find(left)
        root_right = find(right)
        if root_left == root_right:
            return False
        if rank[root_left] < rank[root_right]:
            parent[root_left] = root_right
        elif rank[root_left] > rank[root_right]:
            parent[root_right] = root_left
        else:
            parent[root_right] = root_left
            rank[root_left] += 1
        return True

    for edge in sorted(graph.edges):
        if union(edge.source, edge.target):
            total_weight += edge.weight

    return total_weight
