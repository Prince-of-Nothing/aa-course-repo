import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def plot_median_line(ax, data, x_col, y_col, algorithm, color, marker, label):
    algo_data = data[data['algorithm'] == algorithm].copy()
    if algo_data.empty:
        return

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
    else:
        density_data = data[data['graph_type'].str.startswith('Random (p=')]
        x_link_col = 'edges'
        x_link_label = 'Number of Edges (E)'
        link_plot_title = 'Performance Comparison: DFS vs. BFS (Time vs. Number of Edges)'
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
    plt.figure(figsize=(10, 6))

    ax = plt.gca()
    plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                     'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                     'DFS_Recursive', colors['DFS_Recursive'], '^', 'DFS_Recursive')

    plt.title('DFS Performance: Execution Time vs. Number of Nodes', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Nodes (V)', fontsize=12)
    plt.ylabel('Execution Time (milliseconds)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    dfs_plot_path = os.path.join(output_path, 'dfs_performance_vs_nodes.png')
    plt.savefig(dfs_plot_path, dpi=150)
    print(f"Saved DFS performance plot to {dfs_plot_path}")
    plt.close()

    plt.figure(figsize=(10, 6))

    ax = plt.gca()
    plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                     'BFS', colors['BFS'], 's', 'BFS')

    plt.title('BFS Performance: Execution Time vs. Number of Nodes', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Nodes (V)', fontsize=12)
    plt.ylabel('Execution Time (milliseconds)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    bfs_plot_path = os.path.join(output_path, 'bfs_performance_vs_nodes.png')
    plt.savefig(bfs_plot_path, dpi=150)
    print(f"Saved BFS performance plot to {bfs_plot_path}")
    plt.close()

    plt.figure(figsize=(10, 6))

    ax = plt.gca()
    plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                     'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    plot_median_line(ax, size_data, 'nodes', 'execution_time_ms',
                     'BFS', colors['BFS'], 's', 'BFS')

    plt.title('Performance Comparison: DFS vs. BFS (Time vs. Nodes)', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Nodes (V)', fontsize=12)
    plt.ylabel('Execution Time (milliseconds)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    comparison_plot_path = os.path.join(output_path, 'dfs_vs_bfs_performance_nodes.png')
    plt.savefig(comparison_plot_path, dpi=150)
    print(f"Saved comparison plot (vs Nodes) to {comparison_plot_path}")
    plt.close()

    plt.figure(figsize=(10, 6))

    ax = plt.gca()
    plot_median_line(ax, density_data, x_link_col, 'execution_time_ms',
                     'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    plot_median_line(ax, density_data, x_link_col, 'execution_time_ms',
                     'BFS', colors['BFS'], 's', 'BFS')

    plt.title(link_plot_title, fontsize=14, fontweight='bold')
    plt.xlabel(x_link_label, fontsize=12)
    plt.ylabel('Execution Time (milliseconds)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    comparison_edges_plot_path = os.path.join(output_path, 'dfs_vs_bfs_performance_edges.png')
    plt.savefig(comparison_edges_plot_path, dpi=150)
    print(f"Saved comparison plot (vs Edges) to {comparison_edges_plot_path}")
    plt.close()

    plt.figure(figsize=(10, 6))

    ax = plt.gca()
    plot_median_line(ax, size_data, 'nodes', 'peak_memory_kb',
                     'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    plot_median_line(ax, size_data, 'nodes', 'peak_memory_kb',
                     'BFS', colors['BFS'], 's', 'BFS')
    plot_median_line(ax, size_data, 'nodes', 'peak_memory_kb',
                     'DFS_Recursive', colors['DFS_Recursive'], '^', 'DFS_Recursive')

    plt.title('Memory Usage Comparison: DFS vs. BFS', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Nodes (V)', fontsize=12)
    plt.ylabel('Peak Memory Usage (KB)', fontsize=12)
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
    plot_median_line(ax1, size_data, 'nodes', 'execution_time_ms',
                     'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    plot_median_line(ax1, size_data, 'nodes', 'execution_time_ms',
                     'BFS', colors['BFS'], 's', 'BFS')
    ax1.set_xlabel('Number of Nodes (V)')
    ax1.set_ylabel('Time (ms)')
    ax1.set_title('Execution Time vs Nodes')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(2, 2, 2)
    plot_median_line(ax2, density_data, x_link_col, 'execution_time_ms',
                     'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    plot_median_line(ax2, density_data, x_link_col, 'execution_time_ms',
                     'BFS', colors['BFS'], 's', 'BFS')
    ax2.set_xlabel(x_link_label)
    ax2.set_ylabel('Time (ms)')
    ax2.set_title('Execution Time vs Density %' if x_link_col == 'density_percent' else 'Execution Time vs Edges')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    ax3 = fig.add_subplot(2, 2, 3)
    plot_median_line(ax3, size_data, 'nodes', 'peak_memory_kb',
                     'DFS_Iterative', colors['DFS_Iterative'], 'o', 'DFS_Iterative')
    plot_median_line(ax3, size_data, 'nodes', 'peak_memory_kb',
                     'BFS', colors['BFS'], 's', 'BFS')
    ax3.set_xlabel('Number of Nodes (V)')
    ax3.set_ylabel('Memory (KB)')
    ax3.set_title('Memory Usage vs Nodes')
    ax3.legend()
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

    print(f"\nAll plots successfully saved to the '{output_path}' directory.")

if __name__ == '__main__':
    base_path = 'c:\\Users\\Unknown\\Documents\\Repos\\aa-course-repo\\Lab3'
    csv_path = os.path.join(base_path, 'performance_data.csv')

    if not os.path.exists(csv_path):
        print("Error: 'performance_data.csv' not found.")
        print("Run 'python comprehensive_analysis.py' first to generate empirical data.")
        raise SystemExit(1)

    plot_performance()

