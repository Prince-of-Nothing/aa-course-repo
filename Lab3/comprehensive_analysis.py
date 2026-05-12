import time
import tracemalloc
import pandas as pd
import sys
from collections import defaultdict, deque

sys.setrecursionlimit(50000)

DENSITY_PERCENTAGES = list(range(0, 101, 5))
TRIALS_PER_CONFIGURATION = 20
MIN_VERTEX_COUNT = 2
MAX_VERTEX_COUNT = 1000
DENSITY_SIZE_COUNT = 100

def generate_density_sizes(min_vertices, max_vertices, count):
    if count <= 1:
        return [max_vertices]

    sizes = [
        min_vertices + (i * (max_vertices - min_vertices)) // (count - 1)
        for i in range(count)
    ]
    return sorted(set(sizes))

DENSITY_MATRIX_SIZES = generate_density_sizes(MIN_VERTEX_COUNT, MAX_VERTEX_COUNT, DENSITY_SIZE_COUNT)

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

    def add_vertex(self, v):
        self.vertices.add(v)

    def get_vertices_count(self):
        return len(self.vertices)

    def get_edges_count(self):
        count = sum(len(neighbors) for neighbors in self.graph.values())
        if not self.directed:
            count //= 2
        return count

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

def dfs_recursive(graph, start):
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

import random

def generate_random_graph(num_vertices, edge_probability=0.3, directed=False):
    g = Graph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_probability:
                g.add_edge(i, j)
    return g

def generate_sparse_graph(num_vertices, directed=False):
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
    return generate_random_graph(num_vertices, edge_probability=density, directed=directed)

def generate_complete_graph(num_vertices, directed=False):
    g = Graph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            g.add_edge(i, j)
    return g

def generate_tree(num_vertices):
    g = Graph(directed=False)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(1, num_vertices):
        parent = random.randint(0, i - 1)
        g.add_edge(parent, i)
    return g

def generate_graph_with_additional_links(num_vertices, additional_ratio):
    if not (0.0 <= additional_ratio <= 1.0):
        raise ValueError("additional_ratio must be between 0 and 1")

    g = Graph(directed=False)
    for i in range(num_vertices):
        g.add_vertex(i)

    existing_edges = set()

    for i in range(1, num_vertices):
        parent = random.randint(0, i - 1)
        u, v = (parent, i) if parent < i else (i, parent)
        existing_edges.add((u, v))
        g.add_edge(u, v)

    max_additional = (num_vertices - 1) * (num_vertices - 2) // 2
    target_additional = int(round(additional_ratio * max_additional))

    added = 0
    while added < target_additional:
        u = random.randrange(num_vertices)
        v = random.randrange(num_vertices - 1)
        if v >= u:
            v += 1
        if u > v:
            u, v = v, u

        edge = (u, v)
        if edge in existing_edges:
            continue

        existing_edges.add(edge)
        g.add_edge(u, v)
        added += 1

    return g

def generate_binary_tree(depth):
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
    g = Graph(directed=directed)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(num_vertices - 1):
        g.add_edge(i, i + 1)
    return g

def generate_grid_graph(size, directed=False):
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

def benchmark_algorithm(algorithm, graph, start_vertex, algorithm_name):
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
    print("\n" + "=" * 70)
    print("SCALABILITY ANALYSIS: Graph Size Impact")
    print("=" * 70)

    sizes = [100, 500, 1000, 2000, 5000, 10000]
    results = []

    algorithms = {
        'DFS_Iterative': dfs_iterative,
        'DFS_Recursive': dfs_recursive,
        'BFS': bfs
    }

    for size in sizes:
        print(f"\nTesting with {size} vertices...")

        graph = generate_random_graph(size, edge_probability=0.1)
        edges = graph.get_edges_count()
        start_vertex = 0

        print(f"  Graph: {size} vertices, {edges} edges")

        for algo_name, algo_func in algorithms.items():
            trial_results = []
            for trial in range(1, TRIALS_PER_CONFIGURATION + 1):
                result = benchmark_algorithm(algo_func, graph, start_vertex, algo_name)
                result['nodes'] = size
                result['edges'] = edges
                result['graph_type'] = 'Random (p=0.1)'
                result['trial'] = trial
                results.append(result)
                trial_results.append(result)

            successful_trials = [r for r in trial_results if r['success']]
            if successful_trials:
                median_time = pd.Series([r['execution_time_ms'] for r in successful_trials]).median()
                median_memory = pd.Series([r['peak_memory_kb'] for r in successful_trials]).median()
                print(f"  {algo_name:15}: median {median_time:.3f} ms, "
                      f"median {median_memory:.1f} KB over {len(successful_trials)} trials")
            else:
                print(f"  {algo_name:15}: all trials FAILED")

    return results

def run_graph_type_analysis():
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
        ('Grid (45x45)', lambda: generate_grid_graph(45)),
        ('Binary Tree (d=10)', lambda: generate_binary_tree(10)),
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
            trial_results = []
            for trial in range(1, TRIALS_PER_CONFIGURATION + 1):
                result = benchmark_algorithm(algo_func, graph, start_vertex, algo_name)
                result['nodes'] = vertices
                result['edges'] = edges
                result['graph_type'] = graph_name
                result['trial'] = trial
                results.append(result)
                trial_results.append(result)

            successful_trials = [r for r in trial_results if r['success']]
            if successful_trials:
                median_time = pd.Series([r['execution_time_ms'] for r in successful_trials]).median()
                median_memory = pd.Series([r['peak_memory_kb'] for r in successful_trials]).median()
                print(f"  {algo_name:15}: median {median_time:.3f} ms, "
                      f"median {median_memory:.1f} KB over {len(successful_trials)} trials")
            else:
                print(f"  {algo_name:15}: all trials FAILED")

    return results

def calculate_target_edges_for_density(num_vertices, density_percent):
    if not (0 <= density_percent <= 100):
        raise ValueError("density_percent must be in [0, 100]")

    if num_vertices <= 1:
        return 0

    min_edges = num_vertices - 1
    max_edges = num_vertices * (num_vertices - 1) // 2
    return min_edges + int(round((density_percent / 100.0) * (max_edges - min_edges)))

def format_eta(seconds):
    total_seconds = max(0, int(round(seconds)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def run_density_matrix_analysis():
    print("\n" + "=" * 70)
    print("DENSITY MATRIX ANALYSIS: 0% to 100% (5% Steps)")
    print("0% => n-1 edges, 100% => n(n-1)/2 edges")
    print("=" * 70)

    results = []

    algorithms = {
        'DFS_Iterative': dfs_iterative,
        'BFS': bfs
    }

    total_sizes = len(DENSITY_MATRIX_SIZES)
    analysis_start = time.perf_counter()

    for size_index, size in enumerate(DENSITY_MATRIX_SIZES, start=1):
        size_start = time.perf_counter()
        print(f"\nVertex size {size_index}/{total_sizes}: {size}")
        for percent in DENSITY_PERCENTAGES:
            ratio = percent / 100.0
            expected_edges = calculate_target_edges_for_density(size, percent)

            graph = generate_graph_with_additional_links(size, ratio)
            vertices = graph.get_vertices_count()
            edges = graph.get_edges_count()
            start_vertex = 0

            if edges != expected_edges:
                print(f"  Warning: expected {expected_edges} edges at {percent}%, generated {edges}")

            print(f"  Density {percent:3d}%: {vertices} vertices, {edges} edges")

            for algo_name, algo_func in algorithms.items():
                trial_results = []
                for trial in range(1, TRIALS_PER_CONFIGURATION + 1):
                    result = benchmark_algorithm(algo_func, graph, start_vertex, algo_name)
                    result['nodes'] = vertices
                    result['edges'] = edges
                    result['density_percent'] = percent
                    result['density_ratio'] = ratio
                    result['density_target_edges'] = expected_edges
                    result['graph_type'] = f'Density Matrix ({percent}%)'
                    result['trial'] = trial
                    results.append(result)
                    trial_results.append(result)

                successful_trials = [r for r in trial_results if r['success']]
                if successful_trials:
                    median_time = pd.Series([r['execution_time_ms'] for r in successful_trials]).median()
                    median_memory = pd.Series([r['peak_memory_kb'] for r in successful_trials]).median()
                    print(f"    {algo_name:15}: median {median_time:.3f} ms, "
                          f"median {median_memory:.1f} KB over {len(successful_trials)} trials")
                else:
                    print(f"    {algo_name:15}: all trials FAILED")

        size_elapsed = time.perf_counter() - size_start
        elapsed_total = time.perf_counter() - analysis_start
        avg_per_size = elapsed_total / size_index
        remaining_sizes = total_sizes - size_index
        eta_seconds = avg_per_size * remaining_sizes
        progress_percent = (size_index / total_sizes) * 100

        print(
            f"  Progress: {size_index}/{total_sizes} sizes "
            f"({progress_percent:.1f}%) | size elapsed {format_eta(size_elapsed)} "
            f"| total elapsed {format_eta(elapsed_total)} | ETA {format_eta(eta_seconds)}"
        )

    return results

def generate_summary_report(all_results):
    print("\n" + "=" * 70)
    print("COMPREHENSIVE ANALYSIS SUMMARY")
    print("=" * 70)

    df = pd.DataFrame(all_results)

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
    output_path = f'c:\\Users\\Unknown\\Documents\\Repos\\aa-course-repo\\Lab3\\{filename}'
    df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")

def main():
    print("=" * 70)
    print("LABORATORY WORK 3: DFS vs BFS Empirical Analysis")
    print("=" * 70)

    all_results = []

    all_results.extend(run_density_matrix_analysis())
    results_df = generate_summary_report(all_results)
    save_results(results_df)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print(f"Total tests conducted: {len(all_results)}")
    print("Run 'python plot_results.py' to generate visualizations")
    print("=" * 70)

if __name__ == "__main__":
    main()

