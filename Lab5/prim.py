import heapq


def prim_classic(graph, start=0):
    n = graph.num_vertices
    matrix = graph.to_matrix()
    selected = [False] * n
    min_edge = [float("inf")] * n
    min_edge[start] = 0
    total_weight = 0

    for _ in range(n):
        vertex = -1
        best = float("inf")
        for i in range(n):
            if not selected[i] and min_edge[i] < best:
                best = min_edge[i]
                vertex = i

        if vertex == -1:
            break

        selected[vertex] = True
        total_weight += best

        for neighbor in range(n):
            weight = matrix[vertex][neighbor]
            if weight and not selected[neighbor] and weight < min_edge[neighbor]:
                min_edge[neighbor] = weight

    return total_weight


def prim_optimized(graph, start=0):
    visited = set()
    heap = [(0, start)]
    total_weight = 0

    while heap and len(visited) < graph.num_vertices:
        weight, vertex = heapq.heappop(heap)
        if vertex in visited:
            continue

        visited.add(vertex)
        total_weight += weight

        for neighbor, edge_weight in graph.adj[vertex]:
            if neighbor not in visited:
                heapq.heappush(heap, (edge_weight, neighbor))

    return total_weight
