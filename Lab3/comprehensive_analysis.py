"""
Comprehensive Analysis of DFS and BFS Algorithms
Laboratory Work 3: Empirical Analysis of Graph Traversal Algorithms

This script performs empirical analysis of DFS and BFS algorithms by:
1. Testing on various graph sizes
2. Testing on different graph types (sparse, dense, tree, etc.)
3. Measuring execution time and memory usage
4. Comparing algorithmic performance
"""

import time
import tracemalloc
import pandas as pd
import sys
from collections import defaultdict, deque

# Increase recursion limit for deep graphs
sys.setrecursionlimit(50000)


# ===============================
# GRAPH CLASS (unified for analysis)
# ===============================

class Graph:
    """Graph class using adjacency list representation"""

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

    def add_vertex(self, v):
        self.vertices.add(v)

    def get_vertices_count(self):
        return len(self.vertices)

    def get_edges_count(self):
        count = sum(len(neighbors) for neighbors in self.graph.values())
        if not self.directed:
            count //= 2
        return count


# ===============================
# DFS AND BFS IMPLEMENTATIONS
# ===============================

def dfs_iterative(graph, start):
    """DFS using iterative approach with explicit stack"""
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


def dfs_recursive(graph, start):
    """DFS using recursive approach"""
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


def bfs(graph, start):
    """BFS using queue"""
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


# ===============================
# GRAPH GENERATORS
# ===============================

import random


def generate_random_graph(num_vertices, edge_probability=0.3, directed=False):
    """Generate random graph using Erdos-Renyi model"""
    g = Graph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_probability:
                g.add_edge(i, j)
    return g


def generate_sparse_graph(num_vertices, directed=False):
    """Generate sparse graph (approximately n edges)"""
    g = Graph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(1, num_vertices):
        parent = random.randint(0, i - 1)
        g.add_edge(parent, i)
    extra_edges = num_vertices // 10
    for _ in range(extra_edges):
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)
        if u != v:
            g.add_edge(u, v)
    return g


def generate_dense_graph(num_vertices, density=0.7, directed=False):
    """Generate dense graph with high edge probability"""
    return generate_random_graph(num_vertices, edge_probability=density, directed=directed)


def generate_complete_graph(num_vertices, directed=False):
    """Generate complete graph"""
    g = Graph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            g.add_edge(i, j)
    return g


def generate_tree(num_vertices):
    """Generate random tree"""
    g = Graph(directed=False)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(1, num_vertices):
        parent = random.randint(0, i - 1)
        g.add_edge(parent, i)
    return g


def generate_binary_tree(depth):
    """Generate complete binary tree"""
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
    """Generate linear path graph"""
    g = Graph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(num_vertices - 1):
        g.add_edge(i, i + 1)
    return g


def generate_grid_graph(size, directed=False):
    """Generate grid graph"""
    g = Graph(directed=directed)
    rows = cols = size
    for i in range(rows * cols):
        g.add_vertex(i)
    for r in range(rows):
        for c in range(cols):
            vertex = r * cols + c
            if c < cols - 1:
                g.add_edge(vertex, vertex + 1)
            if r < rows - 1:
                g.add_edge(vertex, vertex + cols)
    return g


# ===============================
# BENCHMARK FUNCTIONS
# ===============================

def benchmark_algorithm(algorithm, graph, start_vertex, algorithm_name):
    """Benchmark a single algorithm and return metrics"""
    tracemalloc.start()

    start_time = time.perf_counter()
    try:
        result = algorithm(graph, start_vertex)
        success = True
    except RecursionError:
        result = []
        success = False
    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time_ms = (end_time - start_time) * 1000
    peak_memory_kb = peak / 1024

    return {
        'algorithm': algorithm_name,
        'execution_time_ms': execution_time_ms,
        'peak_memory_kb': peak_memory_kb,
        'vertices_visited': len(result),
        'success': success
    }


def run_size_analysis():
    """Run analysis with different graph sizes"""
    print("\n" + "=" * 70)
    print("SCALABILITY ANALYSIS: Graph Size Impact")
    print("=" * 70)

    # Sizes to test (vertices)
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    results = []

    algorithms = {
        'DFS_Iterative': dfs_iterative,
        'DFS_Recursive': dfs_recursive,
        'BFS': bfs
    }

    for size in sizes:
        print(f"\nTesting with {size} vertices...")

        # Generate graph with moderate density
        graph = generate_random_graph(size, edge_probability=0.1)
        edges = graph.get_edges_count()
        start_vertex = 0

        print(f"  Graph: {size} vertices, {edges} edges")

        for algo_name, algo_func in algorithms.items():
            result = benchmark_algorithm(algo_func, graph, start_vertex, algo_name)
            result['nodes'] = size
            result['edges'] = edges
            result['graph_type'] = 'Random (p=0.1)'
            results.append(result)

            status = "OK" if result['success'] else "FAILED"
            print(f"  {algo_name:15}: {result['execution_time_ms']:.3f} ms, "
                  f"{result['peak_memory_kb']:.1f} KB [{status}]")

    return results


def run_graph_type_analysis():
    """Run analysis with different graph types"""
    print("\n" + "=" * 70)
    print("GRAPH TYPE ANALYSIS: Different Graph Structures")
    print("=" * 70)

    results = []
    fixed_size = 2000

    graph_generators = [
        ('Sparse', lambda: generate_sparse_graph(fixed_size)),
        ('Dense (p=0.5)', lambda: generate_dense_graph(fixed_size, 0.5)),
        ('Tree', lambda: generate_tree(fixed_size)),
        ('Linear/Path', lambda: generate_linear_graph(fixed_size)),
        ('Grid (45x45)', lambda: generate_grid_graph(45)),  # ~2025 vertices
        ('Binary Tree (d=10)', lambda: generate_binary_tree(10)),  # 2047 vertices
    ]

    algorithms = {
        'DFS_Iterative': dfs_iterative,
        'DFS_Recursive': dfs_recursive,
        'BFS': bfs
    }

    for graph_name, generator in graph_generators:
        print(f"\nTesting {graph_name} graph...")

        graph = generator()
        vertices = graph.get_vertices_count()
        edges = graph.get_edges_count()
        start_vertex = 0

        print(f"  Structure: {vertices} vertices, {edges} edges")

        for algo_name, algo_func in algorithms.items():
            result = benchmark_algorithm(algo_func, graph, start_vertex, algo_name)
            result['nodes'] = vertices
            result['edges'] = edges
            result['graph_type'] = graph_name
            results.append(result)

            status = "OK" if result['success'] else "FAILED"
            print(f"  {algo_name:15}: {result['execution_time_ms']:.3f} ms, "
                  f"{result['peak_memory_kb']:.1f} KB [{status}]")

    return results


def run_edge_density_analysis():
    """Run analysis with varying edge densities"""
    print("\n" + "=" * 70)
    print("EDGE DENSITY ANALYSIS: Sparse to Dense Graphs")
    print("=" * 70)

    results = []
    fixed_size = 1500
    densities = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5]

    algorithms = {
        'DFS_Iterative': dfs_iterative,
        'BFS': bfs
    }

    for density in densities:
        print(f"\nTesting with edge probability {density}...")

        graph = generate_random_graph(fixed_size, edge_probability=density)
        vertices = graph.get_vertices_count()
        edges = graph.get_edges_count()
        start_vertex = 0

        print(f"  Graph: {vertices} vertices, {edges} edges")

        for algo_name, algo_func in algorithms.items():
            result = benchmark_algorithm(algo_func, graph, start_vertex, algo_name)
            result['nodes'] = vertices
            result['edges'] = edges
            result['edge_density'] = density
            result['graph_type'] = f'Random (p={density})'
            results.append(result)

            print(f"  {algo_name:15}: {result['execution_time_ms']:.3f} ms, "
                  f"{result['peak_memory_kb']:.1f} KB")

    return results


def generate_summary_report(all_results):
    """Generate comprehensive summary report"""
    print("\n" + "=" * 70)
    print("COMPREHENSIVE ANALYSIS SUMMARY")
    print("=" * 70)

    df = pd.DataFrame(all_results)

    # Filter successful runs
    successful = df[df['success'] == True]

    print("\n1. ALGORITHM PERFORMANCE OVERVIEW")
    print("-" * 50)

    for algo in successful['algorithm'].unique():
        algo_data = successful[successful['algorithm'] == algo]
        print(f"\n{algo}:")
        print(f"  Average time: {algo_data['execution_time_ms'].mean():.3f} ms")
        print(f"  Median time: {algo_data['execution_time_ms'].median():.3f} ms")
        print(f"  Min time: {algo_data['execution_time_ms'].min():.3f} ms")
        print(f"  Max time: {algo_data['execution_time_ms'].max():.3f} ms")
        print(f"  Avg memory: {algo_data['peak_memory_kb'].mean():.1f} KB")

    print("\n2. BEST ALGORITHM BY GRAPH TYPE")
    print("-" * 50)

    for graph_type in successful['graph_type'].unique():
        type_data = successful[successful['graph_type'] == graph_type]
        if not type_data.empty:
            best_algo = type_data.loc[type_data['execution_time_ms'].idxmin()]
            print(f"\n{graph_type}:")
            print(f"  Best: {best_algo['algorithm']} ({best_algo['execution_time_ms']:.3f} ms)")

    print("\n3. SCALABILITY INSIGHTS")
    print("-" * 50)

    # Compare DFS vs BFS scaling
    dfs_data = successful[successful['algorithm'] == 'DFS_Iterative']
    bfs_data = successful[successful['algorithm'] == 'BFS']

    if not dfs_data.empty and not bfs_data.empty:
        dfs_avg = dfs_data['execution_time_ms'].mean()
        bfs_avg = bfs_data['execution_time_ms'].mean()

        if dfs_avg < bfs_avg:
            faster = 'DFS_Iterative'
            ratio = bfs_avg / dfs_avg
        else:
            faster = 'BFS'
            ratio = dfs_avg / bfs_avg

        print(f"  On average, {faster} is {ratio:.2f}x faster")

    return df


def save_results(df, filename='performance_data.csv'):
    """Save results to CSV file"""
    output_path = f'c:\\Users\\Unknown\\Documents\\Repos\\aa-course-repo\\Lab3\\{filename}'
    df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")


def main():
    """Main function to run comprehensive analysis"""
    print("=" * 70)
    print("LABORATORY WORK 3: DFS vs BFS Empirical Analysis")
    print("=" * 70)

    all_results = []

    # Run different analyses
    all_results.extend(run_size_analysis())
    all_results.extend(run_graph_type_analysis())
    all_results.extend(run_edge_density_analysis())

    # Generate report
    results_df = generate_summary_report(all_results)

    # Save results
    save_results(results_df)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print(f"Total tests conducted: {len(all_results)}")
    print("Run 'python plot_results.py' to generate visualizations")
    print("=" * 70)


if __name__ == "__main__":
    main()
