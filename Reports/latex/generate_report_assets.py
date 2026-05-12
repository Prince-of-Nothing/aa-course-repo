from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "generated"
OUT.mkdir(parents=True, exist_ok=True)


def fmt_number(value, decimals=2):
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.{decimals}f}"
    return str(value)


def latex_escape(value):
    text = str(value)
    replacements = {
        "\\": "\\textbackslash{}",
        "_": "\\_",
        "%": "\\%",
        "&": "\\&",
        "#": "\\#",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def write_latex_table(df: pd.DataFrame, out_name: str):
    align = "l" * len(df.columns)
    lines = [f"\\begin{{tabular}}{{{align}}}", "\\toprule"]
    lines.append(" & ".join(latex_escape(col) for col in df.columns) + " \\\\")
    lines.append("\\midrule")

    for row in df.itertuples(index=False):
        lines.append(" & ".join(latex_escape(value) for value in row) + " \\\\")

    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    (OUT / out_name).write_text("\n".join(lines), encoding="utf-8")


def lab3_tables():
    density = pd.read_csv(ROOT / "Lab3" / "summary" / "version_1_density_base_summary.csv")
    density = density[density["density_percent"] == 50.0][
        ["algorithm", "nodes", "median_time_ms", "median_memory_kb"]
    ].copy()
    density["median_time_ms"] = density["median_time_ms"].map(lambda x: fmt_number(x, 3))
    density["median_memory_kb"] = density["median_memory_kb"].map(lambda x: fmt_number(x, 2))
    density.columns = ["Algorithm", "Nodes", "Median time (ms)", "Median memory (KB)"]
    write_latex_table(density, "lab3_density_table.tex")

    topology = pd.read_csv(ROOT / "Lab3" / "summary" / "version_4_topology_optimized_summary.csv")
    topology = topology[
        (topology["nodes"] == 1000)
        & (topology["graph_type"].isin(["tree", "grid_planar", "bipartite_graph", "complete_graph"]))
    ][["graph_type", "algorithm", "median_time_ms", "median_memory_kb", "edges"]].copy()
    topology["median_time_ms"] = topology["median_time_ms"].map(lambda x: fmt_number(x, 3))
    topology["median_memory_kb"] = topology["median_memory_kb"].map(lambda x: fmt_number(x, 2))
    topology.columns = ["Graph type", "Algorithm", "Median time (ms)", "Median memory (KB)", "Edges"]
    write_latex_table(topology, "lab3_topology_table.tex")


def lab4_tables():
    summary = pd.read_csv(ROOT / "Lab4" / "summary" / "median_summary.csv")

    dijkstra = summary[
        (summary["algorithm_family"] == "single_source")
        & (summary["nodes"] == 1500)
        & (summary["graph_type"].isin(["sparse", "dense"]))
    ][["graph_type", "algorithm", "median_time_ms", "median_memory_kb", "edges"]].copy()
    dijkstra["median_time_ms"] = dijkstra["median_time_ms"].map(lambda x: fmt_number(x, 3))
    dijkstra["median_memory_kb"] = dijkstra["median_memory_kb"].map(lambda x: fmt_number(x, 2))
    dijkstra.columns = ["Graph type", "Algorithm", "Median time (ms)", "Median memory (KB)", "Edges"]
    write_latex_table(dijkstra, "lab4_dijkstra_table.tex")

    floyd = summary[
        (summary["algorithm_family"] == "all_pairs")
        & (summary["nodes"] == 125)
        & (summary["graph_type"].isin(["sparse", "dense"]))
    ][["graph_type", "algorithm", "median_time_ms", "median_memory_kb", "edges"]].copy()
    floyd["median_time_ms"] = floyd["median_time_ms"].map(lambda x: fmt_number(x, 3))
    floyd["median_memory_kb"] = floyd["median_memory_kb"].map(lambda x: fmt_number(x, 2))
    floyd.columns = ["Graph type", "Algorithm", "Median time (ms)", "Median memory (KB)", "Edges"]
    write_latex_table(floyd, "lab4_floyd_table.tex")


def lab5_tables():
    summary = pd.read_csv(ROOT / "Lab5" / "summary" / "median_summary.csv")

    dense = summary[
        (summary["graph_type"] == "dense")
        & (summary["nodes"] == 700)
    ][["algorithm", "median_time_ms", "median_memory_kb", "median_mst_weight", "edges"]].copy()
    dense["median_time_ms"] = dense["median_time_ms"].map(lambda x: fmt_number(x, 3))
    dense["median_memory_kb"] = dense["median_memory_kb"].map(lambda x: fmt_number(x, 2))
    dense["median_mst_weight"] = dense["median_mst_weight"].map(lambda x: fmt_number(x, 0))
    dense.columns = ["Algorithm", "Median time (ms)", "Median memory (KB)", "MST weight", "Edges"]
    write_latex_table(dense, "lab5_dense_table.tex")

    sparse = summary[
        (summary["graph_type"] == "sparse")
        & (summary["nodes"] == 700)
    ][["algorithm", "median_time_ms", "median_memory_kb", "median_mst_weight", "edges"]].copy()
    sparse["median_time_ms"] = sparse["median_time_ms"].map(lambda x: fmt_number(x, 3))
    sparse["median_memory_kb"] = sparse["median_memory_kb"].map(lambda x: fmt_number(x, 2))
    sparse["median_mst_weight"] = sparse["median_mst_weight"].map(lambda x: fmt_number(x, 0))
    sparse.columns = ["Algorithm", "Median time (ms)", "Median memory (KB)", "MST weight", "Edges"]
    write_latex_table(sparse, "lab5_sparse_table.tex")


if __name__ == "__main__":
    lab3_tables()
    lab4_tables()
    lab5_tables()
