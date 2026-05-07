import os
import time
import tracemalloc

import pandas as pd

try:
    from graph_utils import generate_connected_weighted_graph, graph_type_cases
    from kruskal import kruskal_classic, kruskal_optimized
    from prim import prim_classic, prim_optimized
except ModuleNotFoundError:
    from .graph_utils import generate_connected_weighted_graph, graph_type_cases
    from .kruskal import kruskal_classic, kruskal_optimized
    from .prim import prim_classic, prim_optimized


GRAPH_SIZES = [100, 200, 350, 500, 700]
TRIALS = 3


def benchmark_algorithm(algorithm_name, algorithm, graph):
    tracemalloc.start()
    start = time.perf_counter()
    mst_weight = algorithm(graph)
    elapsed_ms = (time.perf_counter() - start) * 1000
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": algorithm_name,
        "execution_time_ms": elapsed_ms,
        "peak_memory_kb": peak / 1024,
        "mst_weight": mst_weight,
    }


def run_analysis():
    rows = []
    algorithms = {
        "Prim_Classic": prim_classic,
        "Prim_Optimized": prim_optimized,
        "Kruskal_Classic": kruskal_classic,
        "Kruskal_Optimized": kruskal_optimized,
    }

    for graph_type, probability in graph_type_cases():
        print(f"\nGraph type: {graph_type} (p={probability})")
        for size in GRAPH_SIZES:
            graph = generate_connected_weighted_graph(size, probability, seed=size)
            for algorithm_name, algorithm in algorithms.items():
                trials = []
                for trial in range(1, TRIALS + 1):
                    row = benchmark_algorithm(algorithm_name, algorithm, graph)
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
                print(f"  {algorithm_name:20} n={size:4} median={median_time:9.3f} ms")

    return rows


def export_summaries(df, base_dir):
    summary_dir = os.path.join(base_dir, "summary")
    os.makedirs(summary_dir, exist_ok=True)

    grouped = (
        df.groupby(["graph_type", "nodes", "algorithm"])
        .agg(
            median_time_ms=("execution_time_ms", "median"),
            median_memory_kb=("peak_memory_kb", "median"),
            median_mst_weight=("mst_weight", "median"),
            edges=("edges", "median"),
            density_ratio=("density_ratio", "median"),
        )
        .reset_index()
    )
    grouped.to_csv(os.path.join(summary_dir, "median_summary.csv"), index=False)

    with open(os.path.join(summary_dir, "median_summary.txt"), "w", encoding="utf-8") as handle:
        handle.write(grouped.to_string(index=False))

    avg_by_algorithm = grouped.groupby("algorithm")["median_time_ms"].mean().sort_values()
    insights = [
        f"fastest average median-time algorithm: {avg_by_algorithm.index[0]}",
        f"slowest average median-time algorithm: {avg_by_algorithm.index[-1]}",
        f"spread between slowest and fastest: {(avg_by_algorithm.iloc[-1] / avg_by_algorithm.iloc[0]):.2f}x",
    ]
    with open(os.path.join(summary_dir, "insights.txt"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(insights))


def main():
    print("=" * 72)
    print("LABORATORY WORK 5: PRIM AND KRUSKAL ANALYSIS")
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
