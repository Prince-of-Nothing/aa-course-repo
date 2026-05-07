import os
import time
import tracemalloc

import pandas as pd

try:
    from dijkstra import dijkstra_classic, dijkstra_optimized
    from floyd_warshall import floyd_warshall_classic, floyd_warshall_optimized
    from graph_utils import INF, generate_weighted_directed_graph, graph_type_cases
except ModuleNotFoundError:
    from .dijkstra import dijkstra_classic, dijkstra_optimized
    from .floyd_warshall import floyd_warshall_classic, floyd_warshall_optimized
    from .graph_utils import INF, generate_weighted_directed_graph, graph_type_cases


DIJKSTRA_SIZES = [100, 250, 500, 1000, 1500]
FLOYD_WARSHALL_SIZES = [25, 50, 75, 100, 125]
TRIALS = 5


def benchmark_algorithm(algorithm_name, algorithm, graph, family):
    tracemalloc.start()
    start = time.perf_counter()
    result = algorithm(graph)
    elapsed_ms = (time.perf_counter() - start) * 1000
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if family == "single_source":
        reachable = sum(1 for value in result if value != INF)
    else:
        reachable = sum(1 for row in result for value in row if value != INF)

    return {
        "algorithm": algorithm_name,
        "algorithm_family": family,
        "execution_time_ms": elapsed_ms,
        "peak_memory_kb": peak / 1024,
        "reachable_distances": reachable,
    }


def run_analysis():
    rows = []
    cases = graph_type_cases()
    algorithm_groups = [
        ("single_source", DIJKSTRA_SIZES, {
            "Dijkstra_Classic": dijkstra_classic,
            "Dijkstra_Optimized": dijkstra_optimized,
        }),
        ("all_pairs", FLOYD_WARSHALL_SIZES, {
            "FloydWarshall_Classic": floyd_warshall_classic,
            "FloydWarshall_Optimized": floyd_warshall_optimized,
        }),
    ]

    for family, sizes, algorithms in algorithm_groups:
        print(f"\n{family.upper()} ANALYSIS")
        for graph_type, probability in cases:
            print(f"  Graph type: {graph_type} (p={probability})")
            for size in sizes:
                graph = generate_weighted_directed_graph(size, probability, seed=size)
                for algorithm_name, algorithm in algorithms.items():
                    trials = []
                    for trial in range(1, TRIALS + 1):
                        row = benchmark_algorithm(algorithm_name, algorithm, graph, family)
                        row.update({
                            "trial": trial,
                            "nodes": size,
                            "edges": graph.edge_count(),
                            "density_ratio": graph.density(),
                            "graph_type": graph_type,
                        })
                        rows.append(row)
                        trials.append(row)

                    median_time = pd.Series([trial["execution_time_ms"] for trial in trials]).median()
                    print(f"    {algorithm_name:24} n={size:4} median={median_time:9.3f} ms")

    return rows


def export_summaries(df, base_dir):
    summary_dir = os.path.join(base_dir, "summary")
    os.makedirs(summary_dir, exist_ok=True)

    grouped = (
        df.groupby(["algorithm_family", "graph_type", "nodes", "algorithm"])
        .agg(
            median_time_ms=("execution_time_ms", "median"),
            median_memory_kb=("peak_memory_kb", "median"),
            median_reachable=("reachable_distances", "median"),
            edges=("edges", "median"),
            density_ratio=("density_ratio", "median"),
        )
        .reset_index()
    )
    grouped.to_csv(os.path.join(summary_dir, "median_summary.csv"), index=False)

    with open(os.path.join(summary_dir, "median_summary.txt"), "w", encoding="utf-8") as handle:
        handle.write(grouped.to_string(index=False))

    insights = []
    for family in sorted(df["algorithm_family"].unique()):
        family_rows = grouped[grouped["algorithm_family"] == family]
        if family_rows.empty:
            continue

        avg_by_algorithm = (
            family_rows.groupby("algorithm")["median_time_ms"].mean().sort_values()
        )
        best_algorithm = avg_by_algorithm.index[0]
        worst_algorithm = avg_by_algorithm.index[-1]
        speedup = avg_by_algorithm.iloc[-1] / avg_by_algorithm.iloc[0] if avg_by_algorithm.iloc[0] else 0

        insights.append(f"{family}:")
        insights.append(f"  fastest average median-time algorithm: {best_algorithm}")
        insights.append(f"  slowest average median-time algorithm: {worst_algorithm}")
        insights.append(f"  spread between slowest and fastest: {speedup:.2f}x")

    with open(os.path.join(summary_dir, "insights.txt"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(insights))


def main():
    print("=" * 72)
    print("LABORATORY WORK 4: DIJKSTRA AND FLOYD-WARSHALL ANALYSIS")
    print("=" * 72)

    rows = run_analysis()
    df = pd.DataFrame(rows)
    base_dir = os.path.dirname(__file__)
    output_path = os.path.join(base_dir, "performance_data.csv")
    df.to_csv(output_path, index=False)
    export_summaries(df, base_dir)
    print(f"\nSaved results to {output_path}")


if __name__ == "__main__":
    main()
