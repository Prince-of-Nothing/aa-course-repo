import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def load_density_data(csv_path):
    df = pd.read_csv(csv_path)

    if "success" in df.columns:
        df = df[df["success"] == True]

    if "density_percent" in df.columns and df["density_percent"].notna().any():
        density_col = "density_percent"
    elif "additional_links_percent" in df.columns and df["additional_links_percent"].notna().any():
        density_col = "additional_links_percent"
    else:
        raise ValueError(
            "No density information found. Expected 'density_percent' or 'additional_links_percent'."
        )

    density = df[df[density_col].notna()].copy()
    density["density_percent"] = density[density_col].astype(float).round().astype(int)

    density = density[density["algorithm"].isin(["DFS_Iterative", "BFS"])].copy()
    if density.empty:
        raise ValueError("No BFS/DFS density rows found in CSV.")

    density["nodes"] = pd.to_numeric(density["nodes"], errors="coerce")
    density["execution_time_ms"] = pd.to_numeric(density["execution_time_ms"], errors="coerce")
    density["peak_memory_kb"] = pd.to_numeric(density["peak_memory_kb"], errors="coerce")
    density = density.dropna(subset=["nodes", "execution_time_ms", "peak_memory_kb", "density_percent"])

    return density


def ensure_output_dirs(base_dir):
    out_dir = os.path.join(base_dir, "density_summary_outputs")
    per_density_dir = os.path.join(out_dir, "plots_per_density")
    median_dir = os.path.join(out_dir, "plots_median_behavior")
    tables_dir = os.path.join(out_dir, "tables")

    os.makedirs(per_density_dir, exist_ok=True)
    os.makedirs(median_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)

    return out_dir, per_density_dir, median_dir, tables_dir


def write_table(df, csv_path, txt_path):
    df.to_csv(csv_path, index=False)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(df.to_string(index=False))


def plot_bfs_dfs_for_each_density(density_df, out_dir):
    colors = {"DFS_Iterative": "#1f77b4", "BFS": "#2ca02c"}
    markers = {"DFS_Iterative": "o", "BFS": "s"}

    density_levels = sorted(density_df["density_percent"].unique().tolist())

    for d in density_levels:
        subset = density_df[density_df["density_percent"] == d]

        for metric, ylabel, suffix in [
            ("execution_time_ms", "Execution Time (ms)", "time"),
            ("peak_memory_kb", "Peak Memory (KB)", "memory"),
        ]:
            plt.figure(figsize=(10, 6))

            for algo in ["DFS_Iterative", "BFS"]:
                algo_data = subset[subset["algorithm"] == algo]
                if algo_data.empty:
                    continue

                grouped = (
                    algo_data.groupby("nodes")[metric]
                    .median()
                    .reset_index()
                    .sort_values("nodes")
                )

                plt.plot(
                    grouped["nodes"],
                    grouped[metric],
                    marker=markers[algo],
                    linewidth=2.2,
                    color=colors[algo],
                    label=f"{algo} median",
                )

            plt.title(f"BFS vs DFS at Density {d}% ({suffix})")
            plt.xlabel("Nodes (V)")
            plt.ylabel(ylabel)
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.legend()
            plt.tight_layout()
            out_name = f"density_{d:03d}_bfs_vs_dfs_{suffix}.png"
            plt.savefig(os.path.join(out_dir, out_name), dpi=150)
            plt.close()


def plot_median_behavior_vs_density(density_df, out_dir):
    colors = {"DFS_Iterative": "#1f77b4", "BFS": "#2ca02c"}
    markers = {"DFS_Iterative": "o", "BFS": "s"}

    for metric, ylabel, out_name in [
        ("execution_time_ms", "Median Execution Time (ms)", "median_behavior_time_vs_density.png"),
        ("peak_memory_kb", "Median Peak Memory (KB)", "median_behavior_memory_vs_density.png"),
    ]:
        grouped = (
            density_df.groupby(["density_percent", "algorithm"])[metric]
            .median()
            .reset_index()
        )

        plt.figure(figsize=(10, 6))

        for algo in ["DFS_Iterative", "BFS"]:
            algo_data = grouped[grouped["algorithm"] == algo].sort_values("density_percent")
            if algo_data.empty:
                continue

            plt.plot(
                algo_data["density_percent"],
                algo_data[metric],
                marker=markers[algo],
                linewidth=2.4,
                color=colors[algo],
                label=f"{algo} median",
            )

        plt.title(f"{ylabel} vs Density")
        plt.xlabel("Density (%)")
        plt.ylabel(ylabel)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, out_name), dpi=150)
        plt.close()


def build_summary_tables(density_df, tables_dir):
    speed_summary = (
        density_df.groupby(["density_percent", "algorithm"])
        .agg(
            samples=("execution_time_ms", "count"),
            unique_nodes=("nodes", "nunique"),
            min_time_ms=("execution_time_ms", "min"),
            median_time_ms=("execution_time_ms", "median"),
            max_time_ms=("execution_time_ms", "max"),
        )
        .reset_index()
        .sort_values(["density_percent", "algorithm"])
    )

    memory_summary = (
        density_df.groupby(["density_percent", "algorithm"])
        .agg(
            samples=("peak_memory_kb", "count"),
            unique_nodes=("nodes", "nunique"),
            min_memory_kb=("peak_memory_kb", "min"),
            median_memory_kb=("peak_memory_kb", "median"),
            max_memory_kb=("peak_memory_kb", "max"),
        )
        .reset_index()
        .sort_values(["density_percent", "algorithm"])
    )

    write_table(
        speed_summary,
        os.path.join(tables_dir, "speed_summary_by_density.csv"),
        os.path.join(tables_dir, "speed_summary_by_density.txt"),
    )
    write_table(
        memory_summary,
        os.path.join(tables_dir, "memory_summary_by_density.csv"),
        os.path.join(tables_dir, "memory_summary_by_density.txt"),
    )

    speed_median = speed_summary.pivot_table(
        index="density_percent", columns="algorithm", values="median_time_ms"
    ).reset_index()

    memory_median = memory_summary.pivot_table(
        index="density_percent", columns="algorithm", values="median_memory_kb"
    ).reset_index()

    if "DFS_Iterative" in speed_median.columns and "BFS" in speed_median.columns:
        speed_median["faster_algorithm"] = speed_median.apply(
            lambda r: "DFS_Iterative" if r["DFS_Iterative"] < r["BFS"] else "BFS",
            axis=1,
        )
        speed_median["speed_ratio"] = speed_median.apply(
            lambda r: (r["BFS"] / r["DFS_Iterative"])
            if r["DFS_Iterative"] < r["BFS"]
            else (r["DFS_Iterative"] / r["BFS"]),
            axis=1,
        )

    if "DFS_Iterative" in memory_median.columns and "BFS" in memory_median.columns:
        memory_median["lower_memory_algorithm"] = memory_median.apply(
            lambda r: "DFS_Iterative" if r["DFS_Iterative"] < r["BFS"] else "BFS",
            axis=1,
        )
        memory_median["memory_ratio"] = memory_median.apply(
            lambda r: (r["BFS"] / r["DFS_Iterative"])
            if r["DFS_Iterative"] < r["BFS"]
            else (r["DFS_Iterative"] / r["BFS"]),
            axis=1,
        )

    write_table(
        speed_median,
        os.path.join(tables_dir, "speed_median_comparison.csv"),
        os.path.join(tables_dir, "speed_median_comparison.txt"),
    )
    write_table(
        memory_median,
        os.path.join(tables_dir, "memory_median_comparison.csv"),
        os.path.join(tables_dir, "memory_median_comparison.txt"),
    )

    return speed_median, memory_median


def write_insights(speed_median, memory_median, out_dir):
    insights_path = os.path.join(out_dir, "insights.txt")

    lines = []
    lines.append("DENSITY SUMMARY INSIGHTS")
    lines.append("=" * 60)

    if "faster_algorithm" in speed_median.columns:
        counts = speed_median["faster_algorithm"].value_counts()
        lines.append("\nFaster algorithm by density level:")
        for algo, cnt in counts.items():
            lines.append(f"- {algo}: {cnt} density levels")

        if "speed_ratio" in speed_median.columns:
            lines.append(f"\nTypical speed ratio (median): {speed_median['speed_ratio'].median():.3f}x")
            lines.append(f"Best speed ratio observed: {speed_median['speed_ratio'].max():.3f}x")

    if "lower_memory_algorithm" in memory_median.columns:
        counts = memory_median["lower_memory_algorithm"].value_counts()
        lines.append("\nLower-memory algorithm by density level:")
        for algo, cnt in counts.items():
            lines.append(f"- {algo}: {cnt} density levels")

        if "memory_ratio" in memory_median.columns:
            lines.append(f"\nTypical memory ratio (median): {memory_median['memory_ratio'].median():.3f}x")
            lines.append(f"Best memory ratio observed: {memory_median['memory_ratio'].max():.3f}x")

    with open(insights_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "performance_data.csv")

    if len(sys.argv) > 1:
        csv_path = sys.argv[1]

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    density_df = load_density_data(csv_path)
    out_dir, per_density_dir, median_dir, tables_dir = ensure_output_dirs(base_dir)

    plot_bfs_dfs_for_each_density(density_df, per_density_dir)
    plot_median_behavior_vs_density(density_df, median_dir)
    speed_median, memory_median = build_summary_tables(density_df, tables_dir)
    write_insights(speed_median, memory_median, out_dir)

    print("Density report complete.")
    print(f"Output directory: {out_dir}")
    print(f"Per-density plots: {per_density_dir}")
    print(f"Median behavior plots: {median_dir}")
    print(f"Tables: {tables_dir}")


if __name__ == "__main__":
    main()
