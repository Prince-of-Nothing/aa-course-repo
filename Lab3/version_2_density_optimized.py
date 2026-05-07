import os

from lab3_common import OPTIMIZED_ALGORITHMS, density_cases, export_summary, run_analysis, save_csv


def main():
    print("VERSION 2: Optimized BFS/DFS by percent fill")
    rows = run_analysis(density_cases(), OPTIMIZED_ALGORITHMS)
    output_path = os.path.join(os.path.dirname(__file__), "version_2_density_optimized.csv")
    save_csv(rows, output_path)
    export_summary(rows, output_path)


if __name__ == "__main__":
    main()
