import random
from dataclasses import dataclass


@dataclass(order=True)
class WeightedEdge:
    weight: int
    source: int
    target: int


class WeightedUndirectedGraph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj = [[] for _ in range(num_vertices)]
        self.edges = []

    def add_edge(self, source, target, weight):
        self.adj[source].append((target, weight))
        self.adj[target].append((source, weight))
        self.edges.append(WeightedEdge(weight, source, target))

    def edge_count(self):
        return len(self.edges)

    def density(self):
        if self.num_vertices <= 1:
            return 0.0
        return self.edge_count() / (self.num_vertices * (self.num_vertices - 1) / 2)

    def to_matrix(self):
        matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]
        for edge in self.edges:
            matrix[edge.source][edge.target] = edge.weight
            matrix[edge.target][edge.source] = edge.weight
        return matrix


def generate_connected_weighted_graph(num_vertices, edge_probability, weight_range=(1, 20), seed=None):
    rng = random.Random(seed)
    graph = WeightedUndirectedGraph(num_vertices)

    for vertex in range(1, num_vertices):
        parent = rng.randrange(vertex)
        graph.add_edge(parent, vertex, rng.randint(*weight_range))

    for source in range(num_vertices):
        for target in range(source + 1, num_vertices):
            if any(neighbor == target for neighbor, _ in graph.adj[source]):
                continue
            if rng.random() <= edge_probability:
                graph.add_edge(source, target, rng.randint(*weight_range))

    return graph


def graph_type_cases():
    return [
        ("sparse", 0.10),
        ("medium", 0.25),
        ("dense", 0.50),
    ]
