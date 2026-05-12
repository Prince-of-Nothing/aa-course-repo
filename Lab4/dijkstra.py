import heapq

try:
    from graph_utils import INF
except ModuleNotFoundError:
    from .graph_utils import INF


def dijkstra_classic(graph, source=0):
    n = graph.num_vertices
    distances = [INF] * n
    visited = [False] * n
    distances[source] = 0

    for _ in range(n):
        current = -1
        current_distance = INF
        for vertex in range(n):
            if not visited[vertex] and distances[vertex] < current_distance:
                current_distance = distances[vertex]
                current = vertex

        if current == -1:
            break

        visited[current] = True
        for neighbor, weight in graph.adj[current]:
            candidate = distances[current] + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate

    return distances


def dijkstra_optimized(graph, source=0):
    n = graph.num_vertices
    distances = [INF] * n
    distances[source] = 0
    heap = [(0, source)]

    while heap:
        current_distance, vertex = heapq.heappop(heap)
        if current_distance != distances[vertex]:
            continue

        for neighbor, weight in graph.adj[vertex]:
            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))

    return distances
