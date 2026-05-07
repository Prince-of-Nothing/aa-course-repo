import time
import tracemalloc
import pandas as pd
import sys
from collections import defaultdict, deque
from graph_generator import Graph, generate_tree, generate_star_graph, generate_linear_graph

sys.setrecursionlimit(50000)

TREE_SIZES = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
TRIALS_PER_CONFIGURATION = 10

def generate_binary_tree_custom(num_vertices):
    g = Graph(directed=False)
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

def generate_k_ary_tree(num_vertices, k):
    g = Graph(directed=False)
    for i in range(num_vertices):
        g.add_vertex(i)
    for i in range(num_vertices):
        for j in range(1, k + 1):
            child = k * i + j
            if child < num_vertices:
                g.add_edge(i, child)
    return g

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

def benchmark_algorithm(algo_func, graph, start_vertex, algo_name):
    tracemalloc.start()
    start_time = time.perf_counter()
    try:
        traversal = algo_func(graph, start_vertex)
        execution_time_ms = (time.perf_counter() - start_time) * 1000
        _, peak_memory = tracemalloc.get_traced_memory()
        peak_memory_kb = peak_memory / 1024.0
        success = (len(traversal) == graph.get_vertices_count())
    except Exception as e:
        print(f'Error in {algo_name}: {e}')
        execution_time_ms = 0
        peak_memory_kb = 0
        success = False
    finally:
        tracemalloc.stop()
        
    return {
        'algorithm': algo_name,
        'execution_time_ms': execution_time_ms,
        'peak_memory_kb': peak_memory_kb,
        'success': success
    }

def format_eta(seconds):
    total_seconds = max(0, int(round(seconds)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f'{hours:02d}:{minutes:02d}:{secs:02d}'
    return f'{minutes:02d}:{secs:02d}'

def run_tree_analysis():
    print("\n" + "=" * 70)
    print("TREE TOPOLOGY ANALYSIS")
    print("=" * 70)

    results = []
    algorithms = {
        'DFS_Iterative': dfs_iterative,
        'BFS': bfs
    }

    tree_generators = {
        'Random Tree': generate_tree,
        'Binary Tree': generate_binary_tree_custom,
        'Ternary Tree (3-ary)': lambda n: generate_k_ary_tree(n, 3),
        'Star Graph': generate_star_graph,
        'Path Graph': generate_linear_graph
    }

    total_sizes = len(TREE_SIZES)
    total_trees = len(tree_generators)
    analysis_start = time.perf_counter()

    for size_index, size in enumerate(TREE_SIZES, start=1):
        print(f"\nSize {size_index}/{total_sizes}: {size} vertices")
        size_start = time.perf_counter()
        
        for tree_name, generator in tree_generators.items():
            graph = generator(size)
            vertices = graph.get_vertices_count()
            edges = graph.get_edges_count()
            start_vertex = 0
            
            for algo_name, algo_func in algorithms.items():
                trial_results = []
                for trial in range(1, TRIALS_PER_CONFIGURATION + 1):
                    result = benchmark_algorithm(algo_func, graph, start_vertex, algo_name)
                    result['nodes'] = vertices
                    result['edges'] = edges
                    result['tree_type'] = tree_name
                    result['trial'] = trial
                    results.append(result)
                    trial_results.append(result)

                successful_trials = [r for r in trial_results if r['success']]
                if successful_trials:
                    median_time = pd.Series([r['execution_time_ms'] for r in successful_trials]).median()
                    median_memory = pd.Series([r['peak_memory_kb'] for r in successful_trials]).median()
                    print(f"    {tree_name:20} - {algo_name:15}: median {median_time:.3f} ms, {median_memory:.1f} KB over {len(successful_trials)} trials")
                else:
                    print(f"    {tree_name:20} - {algo_name:15}: all trials FAILED")

        size_elapsed = time.perf_counter() - size_start
        elapsed_total = time.perf_counter() - analysis_start
        avg_per_size = elapsed_total / size_index
        remaining_sizes = total_sizes - size_index
        eta_seconds = avg_per_size * remaining_sizes
        
        print(f"  Progress: {size_index}/{total_sizes} sizes | size elapsed {format_eta(size_elapsed)} | total elapsed {format_eta(elapsed_total)} | ETA {format_eta(eta_seconds)}")

    return results

def save_results(df, filename='performance_data.csv'):
    output_path = f'c:\\Users\\Unknown\\Documents\\Repos\\aa-course-repo\\Lab3\\{filename}'
    df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")

def main():
    print("=" * 70)
    print("LABORATORY WORK 3: DFS vs BFS Tree Empirical Analysis")
    print("=" * 70)

    all_results = run_tree_analysis()
    results_df = pd.DataFrame(all_results)
    save_results(results_df)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print(f"Total tests conducted: {len(all_results)}")
    print("Run python plot_results.py / tree_report_analysis.py to generate visualizations")
    print("=" * 70)

if __name__ == '__main__':
    main()
