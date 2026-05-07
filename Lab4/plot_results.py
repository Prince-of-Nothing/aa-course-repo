import os

import matplotlib.pyplot as plt
import pandas as pd


def plot_group(data, algorithm_names, title, output_path, metric="execution_time_ms", ylabel="Median Execution Time (ms)"):
    plt.figure(figsize=(10, 6))
    plotted = False
    for algorithm_name in algorithm_names:
        subset = data[data["algorithm"] == algorithm_name]
        if subset.empty:
            continue
        grouped = subset.groupby("nodes")[metric].median().reset_index()
        plt.plot(grouped["nodes"], grouped[metric], marker="o", linewidth=2.2, label=algorithm_name)
        plotted = True

    plt.title(title)
    plt.xlabel("Nodes")
    plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.5)
    if plotted:
        plt.legend()

    if plotted:
        positive_values = data[data[metric] > 0][metric]
        if not positive_values.empty and positive_values.max() / positive_values.min() > 20:
            plt.yscale("log")
            plt.ylabel(f"{ylabel} (log scale)")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_sparse_dense_lines(
    data,
    algorithm_names,
    title,
    output_path,
    metric="execution_time_ms",
    ylabel="Median Execution Time (ms)",
):
    filtered = data[data["graph_type"].isin(["sparse", "dense"])].copy()
    if filtered.empty:
        return

    plt.figure(figsize=(10, 6))
    colors = {
        algorithm_names[0]: "#1f77b4",
        algorithm_names[1]: "#ff7f0e" if len(algorithm_names) > 1 else "#ff7f0e",
    }
    line_styles = {"sparse": "-", "dense": "--"}
    plotted = False

    for algorithm_name in algorithm_names:
        for graph_type in ["sparse", "dense"]:
            subset = filtered[
                (filtered["algorithm"] == algorithm_name) &
                (filtered["graph_type"] == graph_type)
            ]
            if subset.empty:
                continue

            grouped = subset.groupby("nodes")[metric].median().reset_index()
            plt.plot(
                grouped["nodes"],
                grouped[metric],
                marker="o",
                linewidth=2.2,
                linestyle=line_styles[graph_type],
                color=colors.get(algorithm_name),
                label=f"{algorithm_name} ({graph_type})",
            )
            plotted = True

    plt.title(title)
    plt.xlabel("Nodes")
    plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.5)
    if plotted:
        plt.legend()

        positive_values = filtered[filtered[metric] > 0][metric]
        if not positive_values.empty and positive_values.max() / positive_values.min() > 20:
            plt.yscale("log")
            plt.ylabel(f"{ylabel} (log scale)")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_by_density(data, family, output_path, metric="execution_time_ms", ylabel="Median Execution Time (ms)"):
    family_data = data[data["algorithm_family"] == family]
    pivot = family_data.pivot_table(
        values=metric,
        index="graph_type",
        columns="algorithm",
        aggfunc="median",
    )
    if pivot.empty:
        return

    pivot.plot(kind="bar", figsize=(11, 6))
    plt.title(f"{family.replace('_', ' ').title()} Performance by Graph Type")
    plt.xlabel("Graph Type")
    plt.ylabel(ylabel)
    plt.xticks(rotation=0)
    plt.grid(True, axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def main():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "performance_data.csv")
    plot_dir = os.path.join(base_dir, "plots")
    os.makedirs(plot_dir, exist_ok=True)

    data = pd.read_csv(csv_path)

    plot_group(
        data,
        ["Dijkstra_Classic", "Dijkstra_Optimized"],
        "Lab 4: Dijkstra Performance (All Graph Types)",
        os.path.join(plot_dir, "dijkstra_performance.png"),
    )
    plot_sparse_dense_lines(
        data,
        ["Dijkstra_Classic", "Dijkstra_Optimized"],
        "Lab 4: Dijkstra Performance on Sparse vs Dense Graphs",
        os.path.join(plot_dir, "dijkstra_sparse_dense_performance.png"),
    )
    plot_group(
        data,
        ["FloydWarshall_Classic", "FloydWarshall_Optimized"],
        "Lab 4: Floyd-Warshall Performance (All Graph Types)",
        os.path.join(plot_dir, "floyd_warshall_performance.png"),
    )
    plot_sparse_dense_lines(
        data,
        ["FloydWarshall_Classic", "FloydWarshall_Optimized"],
        "Lab 4: Floyd-Warshall Performance on Sparse vs Dense Graphs",
        os.path.join(plot_dir, "floyd_warshall_sparse_dense_performance.png"),
    )
    plot_group(
        data,
        ["Dijkstra_Classic", "Dijkstra_Optimized"],
        "Lab 4: Dijkstra Memory Usage (All Graph Types)",
        os.path.join(plot_dir, "dijkstra_memory.png"),
        metric="peak_memory_kb",
        ylabel="Median Peak Memory (KB)",
    )
    plot_sparse_dense_lines(
        data,
        ["Dijkstra_Classic", "Dijkstra_Optimized"],
        "Lab 4: Dijkstra Memory on Sparse vs Dense Graphs",
        os.path.join(plot_dir, "dijkstra_sparse_dense_memory.png"),
        metric="peak_memory_kb",
        ylabel="Median Peak Memory (KB)",
    )
    plot_group(
        data,
        ["FloydWarshall_Classic", "FloydWarshall_Optimized"],
        "Lab 4: Floyd-Warshall Memory Usage (All Graph Types)",
        os.path.join(plot_dir, "floyd_warshall_memory.png"),
        metric="peak_memory_kb",
        ylabel="Median Peak Memory (KB)",
    )
    plot_sparse_dense_lines(
        data,
        ["FloydWarshall_Classic", "FloydWarshall_Optimized"],
        "Lab 4: Floyd-Warshall Memory on Sparse vs Dense Graphs",
        os.path.join(plot_dir, "floyd_warshall_sparse_dense_memory.png"),
        metric="peak_memory_kb",
        ylabel="Median Peak Memory (KB)",
    )
    plot_by_density(data, "single_source", os.path.join(plot_dir, "dijkstra_by_graph_type.png"))
    plot_by_density(data, "all_pairs", os.path.join(plot_dir, "floyd_warshall_by_graph_type.png"))
    plot_by_density(
        data,
        "single_source",
        os.path.join(plot_dir, "dijkstra_memory_by_graph_type.png"),
        metric="peak_memory_kb",
        ylabel="Median Peak Memory (KB)",
    )
    plot_by_density(
        data,
        "all_pairs",
        os.path.join(plot_dir, "floyd_warshall_memory_by_graph_type.png"),
        metric="peak_memory_kb",
        ylabel="Median Peak Memory (KB)",
    )

    print(f"Saved plots to {plot_dir}")


if __name__ == "__main__":
    main()
