import random
from dataclasses import dataclass


INF = float("inf")


@dataclass
class WeightedEdge:
    source: int
    target: int
    weight: int


class WeightedDirectedGraph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj = [[] for _ in range(num_vertices)]

    def add_edge(self, source, target, weight):
        self.adj[source].append((target, weight))

    def edge_count(self):
        return sum(len(neighbors) for neighbors in self.adj)

    def density(self):
        if self.num_vertices <= 1:
            return 0.0
        return self.edge_count() / (self.num_vertices * (self.num_vertices - 1))

    def to_matrix(self):
        matrix = [[INF] * self.num_vertices for _ in range(self.num_vertices)]
        for i in range(self.num_vertices):
            matrix[i][i] = 0
            for target, weight in self.adj[i]:
                if weight < matrix[i][target]:
                    matrix[i][target] = weight
        return matrix


def generate_weighted_directed_graph(num_vertices, edge_probability, weight_range=(1, 20), seed=None):
    rng = random.Random(seed)
    graph = WeightedDirectedGraph(num_vertices)

    for source in range(num_vertices):
        for target in range(num_vertices):
            if source == target:
                continue
            if rng.random() <= edge_probability:
                graph.add_edge(source, target, rng.randint(*weight_range))

    return graph


def graph_type_cases():
    return [
        ("sparse", 0.15),
        ("medium", 0.35),
        ("dense", 0.65),
    ]
