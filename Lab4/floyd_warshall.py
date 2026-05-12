try:
    from graph_utils import INF
except ModuleNotFoundError:
    from .graph_utils import INF


def floyd_warshall_classic(graph):
    distance = graph.to_matrix()
    n = graph.num_vertices

    for k in range(n):
        for i in range(n):
            for j in range(n):
                candidate = distance[i][k] + distance[k][j]
                if candidate < distance[i][j]:
                    distance[i][j] = candidate

    return distance


def floyd_warshall_optimized(graph):
    distance = graph.to_matrix()
    n = graph.num_vertices

    for k in range(n):
        for i in range(n):
            if distance[i][k] == INF:
                continue
            dik = distance[i][k]
            for j in range(n):
                if distance[k][j] == INF:
                    continue
                candidate = dik + distance[k][j]
                if candidate < distance[i][j]:
                    distance[i][j] = candidate

    return distance
