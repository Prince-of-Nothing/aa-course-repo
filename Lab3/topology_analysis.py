import time
import tracemalloc
import pandas as pd
import sys
from collections import defaultdict, deque
from graph_generator import (Graph, generate_random_graph, generate_dense_graph, generate_tree, 
                             generate_cycle_graph, generate_complete_graph, generate_grid_graph, generate_disconnected_graph)
from graph_generator_extra import (generate_bipartite_graph, generate_wheel_graph, 
                                   generate_weighted_graph, strip_weights, make_demo_graphs, render_traversal_gif)

sys.setrecursionlimit(50000)

GRAPH_SIZES = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
TRIALS_PER_CONFIGURATION = 5

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
        print(f"Error in {algo_name}: {e}")
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
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def run_topology_analysis():
    print("\n" + "=" * 70)
    print("GRAPH TOPOLOGY ANALYSIS")
    print("=" * 70)

    # Invoke extra tasks
    make_demo_graphs()
    render_traversal_gif()

    results = []
    algorithms = {
        'DFS_Iterative': dfs_iterative,
        'BFS': bfs
    }

    graph_generators = {
        'Simple Graph': lambda n: generate_random_graph(n, 0.05),
        'Dense Graph': lambda n: generate_dense_graph(n, 0.7),
        'Tree': generate_tree,
        'Cyclic Graph': generate_cycle_graph,
        'Bipartite Graph': generate_bipartite_graph,
        'Complete Graph': generate_complete_graph,
        'Wheel Graph': generate_wheel_graph,
        'Grid Planar': lambda n: generate_grid_graph(int(n**0.5), int(n**0.5)) if n > 0 else generate_grid_graph(0,0),
        'Weighted Graph': generate_weighted_graph,
        'Stripped Weights Graph': lambda n: strip_weights(generate_weighted_graph(n)),
        'Disconnected Graph': generate_disconnected_graph
    }

    total_sizes = len(GRAPH_SIZES)
    total_graphs = len(graph_generators)
    analysis_start = time.perf_counter()

    for size_index, size in enumerate(GRAPH_SIZES, start=1):
        print(f"\nSize {size_index}/{total_sizes}: {size} vertices")
        size_start = time.perf_counter()
        
        for graph_name, generator in graph_generators.items():
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
                    result['graph_type'] = graph_name
                    result['trial'] = trial
                    results.append(result)
                    trial_results.append(result)

                successful_trials = [r for r in trial_results if r['success']]
                if successful_trials:
                    median_time = pd.Series([r['execution_time_ms'] for r in successful_trials]).median()
                    median_memory = pd.Series([r['peak_memory_kb'] for r in successful_trials]).median()
                    print(f"    {graph_name:20} - {algo_name:15}: median {median_time:.3f} ms, {median_memory:.1f} KB")
                else:
                    print(f"    {graph_name:20} - {algo_name:15}: all trials FAILED")

        size_elapsed = time.perf_counter() - size_start
        elapsed_total = time.perf_counter() - analysis_start
        avg_per_size = elapsed_total / size_index
        remaining_sizes = total_sizes - size_index
        eta_seconds = avg_per_size * remaining_sizes
        
        print(f"  Progress: {size_index}/{total_sizes} | ETA {format_eta(eta_seconds)}")

    return results

def save_results(df, filename='topology_performance_data.csv'):
    output_path = f"c:/Users/Unknown/Documents/Repos/aa-course-repo/Lab3/{filename}"
    df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")

def main():
    all_results = run_topology_analysis()
    results_df = pd.DataFrame(all_results)
    save_results(results_df)

if __name__ == "__main__":
    main()
