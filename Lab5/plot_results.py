import os

import matplotlib.pyplot as plt
import pandas as pd


def plot_algorithms(data, output_path, metric="execution_time_ms", ylabel="Median Execution Time (ms)", title="Lab 5: MST Algorithm Performance"):
    plt.figure(figsize=(10, 6))
    for algorithm_name in sorted(data["algorithm"].unique()):
        subset = data[data["algorithm"] == algorithm_name]
        grouped = subset.groupby("nodes")[metric].median().reset_index()
        plt.plot(grouped["nodes"], grouped[metric], marker="o", linewidth=2.2, label=algorithm_name)

    plt.title(title)
    plt.xlabel("Nodes")
    plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_by_graph_type(data, output_path, metric="execution_time_ms", ylabel="Median Execution Time (ms)", title="Lab 5: MST Performance by Graph Type"):
    pivot = data.pivot_table(
        values=metric,
        index="graph_type",
        columns="algorithm",
        aggfunc="median",
    )
    if pivot.empty:
        return

    pivot.plot(kind="bar", figsize=(11, 6))
    plt.title(title)
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
    plot_algorithms(data, os.path.join(plot_dir, "mst_performance.png"))
    plot_by_graph_type(data, os.path.join(plot_dir, "mst_by_graph_type.png"))
    plot_algorithms(
        data,
        os.path.join(plot_dir, "mst_memory.png"),
        metric="peak_memory_kb",
        ylabel="Median Peak Memory (KB)",
        title="Lab 5: MST Algorithm Memory Usage",
    )
    plot_by_graph_type(
        data,
        os.path.join(plot_dir, "mst_memory_by_graph_type.png"),
        metric="peak_memory_kb",
        ylabel="Median Peak Memory (KB)",
        title="Lab 5: MST Memory by Graph Type",
    )
    print(f"Saved plots to {plot_dir}")


if __name__ == "__main__":
    main()
