import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def plot_median_line(ax, data, x_col, y_col, algorithm, color, marker, label):
    algo_data = data[data['algorithm'] == algorithm].copy()
    if algo_data.empty:
        return False

    median_data = algo_data.groupby(x_col)[y_col].median().reset_index().sort_values(x_col)
    ax.plot(
        median_data[x_col],
        median_data[y_col],
        color=color,
        marker=marker,
        linestyle='-',
        linewidth=2.5,
        markersize=8,
        label=f'{label} (median)'
    )
    return True

def safe_name(text):
    return text.replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '').replace('%', 'pct')

def export_table(table_df, csv_path, md_path, float_format='%.3f'):
    table_df.to_csv(csv_path)
    with open(md_path, 'w', encoding='utf-8') as f:
        try:
            f.write(table_df.to_markdown(floatfmt=float_format.replace('%', '')))
        except ImportError:
            # Fallback when optional dependency 'tabulate' is not installed.
            f.write(table_df.to_string())

def build_range_frame(data, algorithm, density_percent, metric_col):
    subset = data[
        (data['algorithm'] == algorithm) &
        (data['density_percent'] == density_percent)
    ]
    if subset.empty:
        return pd.DataFrame()

    grouped = subset.groupby('nodes')[metric_col].agg(['min', 'median', 'max']).reset_index()
    return grouped.sort_values('nodes')

def generate_density_dedicated_report(density_data, output_path, colors):
    if density_data.empty:
        print('Skipped dedicated density report: no density rows found.')
        return

    report_dir = os.path.join(output_path, 'density_report')
    per_algorithm_dir = os.path.join(report_dir, 'per_algorithm')
    pairwise_dir = os.path.join(report_dir, 'pairwise')
    tables_dir = os.path.join(report_dir, 'tables')

    os.makedirs(per_algorithm_dir, exist_ok=True)
    os.makedirs(pairwise_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)

    algorithms = [algo for algo in ['DFS_Iterative', 'BFS'] if algo in density_data['algorithm'].unique()]
    density_levels = list(range(0, 101, 5))

    if not algorithms or not density_levels:
        print('Skipped dedicated density report: missing required algorithm/density data.')
        return

    # 22 plots per type: 21 densities (0..100 step 5) + 1 summary/median plot.
    for algorithm in algorithms:
        algo_dir = os.path.join(per_algorithm_dir, safe_name(algorithm))
        os.makedirs(algo_dir, exist_ok=True)

        for density in density_levels:
            time_frame = build_range_frame(density_data, algorithm, density, 'execution_time_ms')

            plt.figure(figsize=(10, 6))
            ax = plt.gca()

            if time_frame.empty:
                ax.text(0.5, 0.5, f'No data for density {density}%', ha='center', va='center', transform=ax.transAxes)
            else:
                ax.fill_between(
                    time_frame['nodes'].to_numpy(),
                    time_frame['min'].to_numpy(),
                    time_frame['max'].to_numpy(),
                    color=colors.get(algorithm, 'gray'),
                    alpha=0.20,
                    label='Range (min-max)'
                )
                ax.plot(
                    time_frame['nodes'].to_numpy(),
                    time_frame['median'].to_numpy(),
                    marker='o',
                    linewidth=2.2,
                    color=colors.get(algorithm, 'gray'),
                    label='Median'
                )
                ax.legend()

            ax.set_title(f'{algorithm} - Density {density}% (Execution Time)')
            ax.set_xlabel('Nodes (V)')
            ax.set_ylabel('Execution Time (ms)')
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            out_file = os.path.join(algo_dir, f'{safe_name(algorithm)}_density_{density:03d}_time.png')
            plt.savefig(out_file, dpi=150)
            plt.close()

        # 22nd dedicated plot: median-over-density summary for this algorithm.
        summary = density_data[density_data['algorithm'] == algorithm].copy()
        summary = summary.groupby('density_percent')['execution_time_ms'].median().reset_index().sort_values('density_percent')
        if not summary.empty:
            plt.figure(figsize=(10, 6))
            ax = plt.gca()
            ax.plot(
                summary['density_percent'].to_numpy(),
                summary['execution_time_ms'].to_numpy(),
                marker='s',
                linewidth=2.5,
                color=colors.get(algorithm, 'gray')
            )
            ax.set_title(f'{algorithm} - Median Time Across Density Levels')
            ax.set_xlabel('Density (%)')
            ax.set_ylabel('Median Execution Time (ms)')
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            out_file = os.path.join(algo_dir, f'{safe_name(algorithm)}_density_median_summary.png')
            plt.savefig(out_file, dpi=150)
            plt.close()

        print(f'Generated {len(density_levels) + 1} dedicated plots for {algorithm}.')

    # Pairwise density overlays (DFS vs BFS) to compare behavior density-by-density.
    if all(x in algorithms for x in ['DFS_Iterative', 'BFS']):
        for density in density_levels:
            dfs_frame = build_range_frame(density_data, 'DFS_Iterative', density, 'execution_time_ms')
            bfs_frame = build_range_frame(density_data, 'BFS', density, 'execution_time_ms')

            plt.figure(figsize=(10, 6))
            ax = plt.gca()

            if not dfs_frame.empty:
                ax.fill_between(
                    dfs_frame['nodes'].to_numpy(),
                    dfs_frame['min'].to_numpy(),
                    dfs_frame['max'].to_numpy(),
                    color=colors['DFS_Iterative'],
                    alpha=0.16
                )
                ax.plot(
                    dfs_frame['nodes'].to_numpy(),
                    dfs_frame['median'].to_numpy(),
                    color=colors['DFS_Iterative'],
                    linewidth=2.2,
                    marker='o',
                    label='DFS_Iterative median'
                )

            if not bfs_frame.empty:
                ax.fill_between(
                    bfs_frame['nodes'].to_numpy(),
                    bfs_frame['min'].to_numpy(),
                    bfs_frame['max'].to_numpy(),
                    color=colors['BFS'],
                    alpha=0.16
                )
                ax.plot(
                    bfs_frame['nodes'].to_numpy(),
                    bfs_frame['median'].to_numpy(),
                    color=colors['BFS'],
                    linewidth=2.2,
                    marker='s',
                    label='BFS median'
                )

            if dfs_frame.empty and bfs_frame.empty:
                ax.text(0.5, 0.5, f'No data for density {density}%', ha='center', va='center', transform=ax.transAxes)

            ax.set_title(f'DFS vs BFS Overlay - Density {density}%')
            ax.set_xlabel('Nodes (V)')
            ax.set_ylabel('Execution Time (ms)')
            ax.grid(True, linestyle='--', alpha=0.6)
            if not (dfs_frame.empty and bfs_frame.empty):
                ax.legend()
            plt.tight_layout()
            out_file = os.path.join(pairwise_dir, f'dfs_vs_bfs_density_{density:03d}_overlay.png')
            plt.savefig(out_file, dpi=150)
            plt.close()

    # Tables for speed and memory (median values).
    for algorithm in algorithms:
        algo_data = density_data[density_data['algorithm'] == algorithm].copy()
        if algo_data.empty:
            continue

        speed_table = algo_data.pivot_table(
            values='execution_time_ms',
            index='nodes',
            columns='density_percent',
            aggfunc='median'
        ).sort_index().sort_index(axis=1)

        memory_table = algo_data.pivot_table(
            values='peak_memory_kb',
            index='nodes',
            columns='density_percent',
            aggfunc='median'
        ).sort_index().sort_index(axis=1)

        speed_csv = os.path.join(tables_dir, f'{safe_name(algorithm)}_speed_median_table.csv')
        speed_md = os.path.join(tables_dir, f'{safe_name(algorithm)}_speed_median_table.md')
        memory_csv = os.path.join(tables_dir, f'{safe_name(algorithm)}_memory_median_table.csv')
        memory_md = os.path.join(tables_dir, f'{safe_name(algorithm)}_memory_median_table.md')

        export_table(speed_table, speed_csv, speed_md)
        export_table(memory_table, memory_csv, memory_md)

    if all(x in algorithms for x in ['DFS_Iterative', 'BFS']):
        cmp_base = density_data[density_data['algorithm'].isin(['DFS_Iterative', 'BFS'])].copy()
        cmp_tbl = cmp_base.pivot_table(
            values='execution_time_ms',
            index=['nodes', 'density_percent'],
            columns='algorithm',
            aggfunc='median'
        ).reset_index()
        if 'DFS_Iterative' in cmp_tbl.columns and 'BFS' in cmp_tbl.columns:
            cmp_tbl['speed_ratio_dfs_over_bfs'] = cmp_tbl['DFS_Iterative'] / cmp_tbl['BFS']
        cmp_tbl = cmp_tbl.sort_values(['nodes', 'density_percent'])

        cmp_csv = os.path.join(tables_dir, 'dfs_vs_bfs_speed_comparison.csv')
        cmp_md = os.path.join(tables_dir, 'dfs_vs_bfs_speed_comparison.md')
        cmp_tbl.to_csv(cmp_csv, index=False)
        with open(cmp_md, 'w', encoding='utf-8') as f:
            try:
                f.write(cmp_tbl.to_markdown(index=False))
            except ImportError:
                f.write(cmp_tbl.to_string(index=False))

    print(f'Dedicated density report saved in: {report_dir}')

def plot_performance(csv_file='performance_data.csv', output_dir='plots'):
    base_path = 'c:\\Users\\Unknown\\Documents\\Repos\\aa-course-repo\\Lab3'
    csv_path = os.path.join(base_path, csv_file)
    output_path = os.path.join(base_path, output_dir)

    try:
        data = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: The file {csv_path} was not found.")
        print("Please run comprehensive_analysis.py first to generate data.")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

    data = data[data['success'] == True]

    size_data = data[data['graph_type'] == 'Random (p=0.1)']

    if 'density_percent' in data.columns and data['density_percent'].notna().any():
        density_data = data[data['density_percent'].notna()].copy()
        x_link_col = 'density_percent'
        x_link_label = 'Density (%) where 0% = n-1 edges, 100% = n(n-1)/2'
        link_plot_title = 'Performance Comparison: DFS vs. BFS (Time vs. Density %)'
    elif 'additional_links_percent' in data.columns and data['additional_links_percent'].notna().any():
        density_data = data[data['additional_links_percent'].notna()].copy()
        density_data['density_percent'] = density_data['additional_links_percent']
        if 'additional_links_ratio' in density_data.columns:
            density_data['density_ratio'] = density_data['additional_links_ratio']
        x_link_col = 'density_percent'
        x_link_label = 'Density (%) where 0% = n-1 edges, 100% = n(n-1)/2'
        link_plot_title = 'Performance Comparison: DFS vs. BFS (Time vs. Density %)'
    else:
        density_data = data[data['graph_type'].str.startswith('Random (p=')]
        x_link_col = 'edges'
        x_link_label = 'Number of Edges (E)'
        link_plot_title = 'Performance Comparison: DFS vs. BFS (Time vs. Number of Edges)'

    if 'nodes' in density_data.columns and not density_data.empty:
        density_node_count = density_data['nodes'].nunique()
        if density_node_count < 100:
            print(
                f"Warning: density data contains {density_node_count} unique node sizes. "
                "For the new setup, regenerate CSV via comprehensive_analysis.py to get 100 sizes (2..1000)."
            )
    main_type_labels = [
        'Sparse',
        'Dense (p=0.5)',
        'Tree',
        'Linear/Path',
        'Grid (45x45)',
        'Binary Tree (d=10)'
    ]
    type_data = data[data['graph_type'].isin(main_type_labels)]

    plt.style.use('seaborn-v0_8-whitegrid')
    colors = {'DFS_Iterative': '#3498db', 'DFS_Recursive': '#9b59b6', 'BFS': '#2ecc71'}
    if size_data.empty:
        print("Skipped node-based plots: no 'Random (p=0.1)' rows found in CSV.")
    else:
        plt.figure(figsize=(10, 6))

        ax = plt.gca()
        has_dfs_iter = plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                                        'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
        has_dfs_rec = plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                                       'DFS_Recursive', colors['DFS_Recursive'], '^', 'DFS_Recursive')

        plt.title('DFS Performance: Execution Time vs. Number of Nodes', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Nodes (V)', fontsize=12)
        plt.ylabel('Execution Time (milliseconds)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        if has_dfs_iter or has_dfs_rec:
            plt.legend(fontsize=10)
        plt.tight_layout()
        dfs_plot_path = os.path.join(output_path, 'dfs_performance_vs_nodes.png')
        plt.savefig(dfs_plot_path, dpi=150)
        print(f"Saved DFS performance plot to {dfs_plot_path}")
        plt.close()

        plt.figure(figsize=(10, 6))

        ax = plt.gca()
        has_bfs = plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                                   'BFS', colors['BFS'], 's', 'BFS')

        plt.title('BFS Performance: Execution Time vs. Number of Nodes', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Nodes (V)', fontsize=12)
        plt.ylabel('Execution Time (milliseconds)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        if has_bfs:
            plt.legend(fontsize=10)
        plt.tight_layout()
        bfs_plot_path = os.path.join(output_path, 'bfs_performance_vs_nodes.png')
        plt.savefig(bfs_plot_path, dpi=150)
        print(f"Saved BFS performance plot to {bfs_plot_path}")
        plt.close()

        plt.figure(figsize=(10, 6))

        ax = plt.gca()
        has_dfs_iter = plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                                        'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
        has_bfs = plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                                   'BFS', colors['BFS'], 's', 'BFS')

        plt.title('Performance Comparison: DFS vs. BFS (Time vs. Nodes)', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Nodes (V)', fontsize=12)
        plt.ylabel('Execution Time (milliseconds)', fontsize=12)
        if has_dfs_iter or has_bfs:
            plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        comparison_plot_path = os.path.join(output_path, 'dfs_vs_bfs_performance_nodes.png')
        plt.savefig(comparison_plot_path, dpi=150)
        print(f"Saved comparison plot (vs Nodes) to {comparison_plot_path}")
        plt.close()

    plt.figure(figsize=(10, 6))

    ax = plt.gca()
    has_dfs_iter = plot_median_line(ax, density_data, x_link_col, 'execution_time_ms',
                                    'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    has_bfs = plot_median_line(ax, density_data, x_link_col, 'execution_time_ms',
                               'BFS', colors['BFS'], 's', 'BFS')

    plt.title(link_plot_title, fontsize=14, fontweight='bold')
    plt.xlabel(x_link_label, fontsize=12)
    plt.ylabel('Execution Time (milliseconds)', fontsize=12)
    if has_dfs_iter or has_bfs:
        plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    comparison_edges_plot_path = os.path.join(output_path, 'dfs_vs_bfs_performance_edges.png')
    plt.savefig(comparison_edges_plot_path, dpi=150)
    print(f"Saved comparison plot (vs Edges) to {comparison_edges_plot_path}")
    plt.close()

    if not size_data.empty:
        plt.figure(figsize=(10, 6))

        ax = plt.gca()
        has_dfs_iter = plot_median_line(ax, size_data, 'nodes', 'peak_memory_kb',
                                        'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
        has_bfs = plot_median_line(ax, size_data, 'nodes', 'peak_memory_kb',
                                   'BFS', colors['BFS'], 's', 'BFS')
        has_dfs_rec = plot_median_line(ax, size_data, 'nodes', 'peak_memory_kb',
                                       'DFS_Recursive', colors['DFS_Recursive'], '^', 'DFS_Recursive')

        plt.title('Memory Usage Comparison: DFS vs. BFS', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Nodes (V)', fontsize=12)
        plt.ylabel('Peak Memory Usage (KB)', fontsize=12)
        if has_dfs_iter or has_bfs or has_dfs_rec:
            plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        memory_plot_path = os.path.join(output_path, 'memory_usage_comparison.png')
        plt.savefig(memory_plot_path, dpi=150)
        print(f"Saved memory usage plot to {memory_plot_path}")
        plt.close()

    plt.figure(figsize=(12, 6))

    if not type_data.empty:
        pivot_data = type_data.pivot_table(
            values='execution_time_ms',
            index='graph_type',
            columns='algorithm',
            aggfunc='median'
        )

        if not pivot_data.empty:
            ax = pivot_data.plot(kind='bar', width=0.8, figsize=(12, 6),
                               color=[colors.get(c, 'gray') for c in pivot_data.columns])
            plt.title('Algorithm Performance by Graph Type', fontsize=14, fontweight='bold')
            plt.xlabel('Graph Type', fontsize=12)
            plt.ylabel('Execution Time (ms)', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.legend(title='Algorithm', fontsize=10)
            plt.grid(True, axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            graph_type_plot_path = os.path.join(output_path, 'performance_by_graph_type.png')
            plt.savefig(graph_type_plot_path, dpi=150)
            print(f"Saved graph type performance plot to {graph_type_plot_path}")
            plt.close()

    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Comprehensive DFS vs BFS Analysis', fontsize=16, fontweight='bold')

    ax1 = fig.add_subplot(2, 2, 1)
    has_dfs_iter = plot_median_line(ax1, size_data, 'nodes', 'execution_time_ms',
                                    'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    has_bfs = plot_median_line(ax1, size_data, 'nodes', 'execution_time_ms',
                               'BFS', colors['BFS'], 's', 'BFS')
    ax1.set_xlabel('Number of Nodes (V)')
    ax1.set_ylabel('Time (ms)')
    ax1.set_title('Execution Time vs Nodes')
    if has_dfs_iter or has_bfs:
        ax1.legend()
    else:
        ax1.text(0.5, 0.5, 'No node-scaling data', ha='center', va='center', transform=ax1.transAxes)
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(2, 2, 2)
    has_dfs_iter = plot_median_line(ax2, density_data, x_link_col, 'execution_time_ms',
                                    'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    has_bfs = plot_median_line(ax2, density_data, x_link_col, 'execution_time_ms',
                               'BFS', colors['BFS'], 's', 'BFS')
    ax2.set_xlabel(x_link_label)
    ax2.set_ylabel('Time (ms)')
    ax2.set_title('Execution Time vs Density %' if x_link_col == 'density_percent' else 'Execution Time vs Edges')
    if has_dfs_iter or has_bfs:
        ax2.legend()
    ax2.grid(True, alpha=0.3)

    ax3 = fig.add_subplot(2, 2, 3)
    has_dfs_iter = plot_median_line(ax3, size_data, 'nodes', 'peak_memory_kb',
                                    'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    has_bfs = plot_median_line(ax3, size_data, 'nodes', 'peak_memory_kb',
                               'BFS', colors['BFS'], 's', 'BFS')
    ax3.set_xlabel('Number of Nodes (V)')
    ax3.set_ylabel('Memory (KB)')
    ax3.set_title('Memory Usage vs Nodes')
    if has_dfs_iter or has_bfs:
        ax3.legend()
    else:
        ax3.text(0.5, 0.5, 'No node-scaling data', ha='center', va='center', transform=ax3.transAxes)
    ax3.grid(True, alpha=0.3)

    ax4 = fig.add_subplot(2, 2, 4)
    if not type_data.empty:
        pivot_data = type_data.pivot_table(
            values='execution_time_ms',
            index='graph_type',
            columns='algorithm',
            aggfunc='median'
        )
        if not pivot_data.empty and 'DFS_Iterative' in pivot_data.columns and 'BFS' in pivot_data.columns:
            x = np.arange(len(pivot_data.index))
            width = 0.35
            ax4.bar(x - width/2, pivot_data['DFS_Iterative'], width,
                   label='DFS_Iterative', color=colors['DFS_Iterative'])
            ax4.bar(x + width/2, pivot_data['BFS'], width,
                   label='BFS', color=colors['BFS'])
            ax4.set_xticks(x)
            ax4.set_xticklabels(pivot_data.index, rotation=45, ha='right')
            ax4.set_ylabel('Time (ms)')
            ax4.set_title('Performance by Graph Type')
            ax4.legend()
            ax4.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    comprehensive_plot_path = os.path.join(output_path, 'comprehensive_analysis.png')
    plt.savefig(comprehensive_plot_path, dpi=150, bbox_inches='tight')
    print(f"Saved comprehensive analysis plot to {comprehensive_plot_path}")
    plt.close()

    if 'density_percent' in density_data.columns and density_data['density_percent'].notna().any():
        generate_density_dedicated_report(density_data, output_path, colors)

    print(f"\nAll plots successfully saved to the '{output_path}' directory.")

if __name__ == '__main__':
    base_path = 'c:\\Users\\Unknown\\Documents\\Repos\\aa-course-repo\\Lab3'
    csv_path = os.path.join(base_path, 'performance_data.csv')

    if not os.path.exists(csv_path):
        print("Error: 'performance_data.csv' not found.")
        print("Run 'python comprehensive_analysis.py' first to generate empirical data.")
        raise SystemExit(1)

    plot_performance()

