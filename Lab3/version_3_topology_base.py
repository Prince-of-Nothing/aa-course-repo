import os

from lab3_common import BASE_ALGORITHMS, export_summary, run_analysis, save_csv, topology_cases


def main():
    print("VERSION 3: Base BFS/DFS by graph type")
    rows = run_analysis(topology_cases(sizes=[10, 50, 100, 200]), BASE_ALGORITHMS)
    output_path = os.path.join(os.path.dirname(__file__), "version_3_topology_base.csv")
    save_csv(rows, output_path)
    export_summary(rows, output_path)


if __name__ == "__main__":
    main()
