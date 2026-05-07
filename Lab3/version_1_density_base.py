import os

from lab3_common import BASE_ALGORITHMS, density_cases, export_summary, run_analysis, save_csv


def main():
    print("VERSION 1: Base BFS/DFS by percent fill")
    rows = run_analysis(density_cases(sizes=[10, 50, 100, 200]), BASE_ALGORITHMS)
    output_path = os.path.join(os.path.dirname(__file__), "version_1_density_base.csv")
    save_csv(rows, output_path)
    export_summary(rows, output_path)


if __name__ == "__main__":
    main()
