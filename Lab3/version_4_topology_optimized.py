import os

from lab3_common import OPTIMIZED_ALGORITHMS, export_summary, run_analysis, save_csv, topology_cases


def main():
    print("VERSION 4: Optimized BFS/DFS by graph type")
    rows = run_analysis(topology_cases(), OPTIMIZED_ALGORITHMS)
    output_path = os.path.join(os.path.dirname(__file__), "version_4_topology_optimized.csv")
    save_csv(rows, output_path)
    export_summary(rows, output_path)


if __name__ == "__main__":
    main()
