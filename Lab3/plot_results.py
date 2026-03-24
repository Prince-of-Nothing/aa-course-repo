"""
Plot Results for DFS/BFS Empirical Analysis
Laboratory Work 3

Generates visualizations from the performance data CSV file.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def plot_performance(csv_file='performance_data.csv', output_dir='plots'):
    """
    Reads performance data from CSV and generates plots.
    Saves plots to the specified output directory.
    """
    # Construct full path
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

    # Filter successful runs only
    data = data[data['success'] == True]

    # Use comparable subsets for fair visual analysis.
    # - Size scalability: random graphs with fixed probability p=0.1
    # - Density analysis: random graphs at fixed node count with varying density
    # - Graph type comparison: structural generators only
    size_data = data[data['graph_type'] == 'Random (p=0.1)']
    density_data = data[data['graph_type'].str.startswith('Random (p=')]
    if 'edge_density' in density_data.columns:
        density_data = density_data[density_data['edge_density'].notna()]
    main_type_labels = [
        'Sparse',
        'Dense (p=0.5)',
        'Tree',
        'Linear/Path',
        'Grid (45x45)',
        'Binary Tree (d=10)'
    ]
    type_data = data[data['graph_type'].isin(main_type_labels)]

    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    colors = {'DFS_Iterative': '#3498db', 'DFS_Recursive': '#9b59b6', 'BFS': '#2ecc71'}

    # ========================================
    # Plot 1: DFS Performance (Time vs. Nodes)
    # ========================================
    plt.figure(figsize=(10, 6))

    for algo in ['DFS_Iterative', 'DFS_Recursive']:
        algo_data = size_data[size_data['algorithm'] == algo]
        if not algo_data.empty:
            # Group by nodes and calculate mean
            grouped = algo_data.groupby('nodes')['execution_time_ms'].mean().reset_index()
            grouped = grouped.sort_values('nodes')
            plt.plot(grouped['nodes'], grouped['execution_time_ms'],
                    marker='o', linestyle='-', color=colors.get(algo, 'gray'),
                    label=algo, linewidth=2, markersize=8)

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

    # ========================================
    # Plot 2: BFS Performance (Time vs. Nodes)
    # ========================================
    plt.figure(figsize=(10, 6))

    bfs_data = size_data[size_data['algorithm'] == 'BFS']
    if not bfs_data.empty:
        grouped = bfs_data.groupby('nodes')['execution_time_ms'].mean().reset_index()
        grouped = grouped.sort_values('nodes')
        plt.plot(grouped['nodes'], grouped['execution_time_ms'],
                marker='s', linestyle='-', color=colors['BFS'],
                label='BFS', linewidth=2, markersize=8)

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

    # ========================================
    # Plot 3: Comparison DFS vs BFS (Time vs. Nodes)
    # ========================================
    plt.figure(figsize=(10, 6))

    for algo in ['DFS_Iterative', 'BFS']:
        algo_data = size_data[size_data['algorithm'] == algo]
        if not algo_data.empty:
            grouped = algo_data.groupby('nodes')['execution_time_ms'].mean().reset_index()
            grouped = grouped.sort_values('nodes')
            plt.plot(grouped['nodes'], grouped['execution_time_ms'],
                    marker='o' if algo == 'DFS_Iterative' else 's',
                    linestyle='-', color=colors.get(algo, 'gray'),
                    label=algo, linewidth=2, markersize=8)

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

    # ========================================
    # Plot 4: Comparison DFS vs BFS (Time vs. Edges)
    # ========================================
    plt.figure(figsize=(10, 6))

    for algo in ['DFS_Iterative', 'BFS']:
        algo_data = density_data[density_data['algorithm'] == algo]
        if not algo_data.empty:
            grouped = algo_data.groupby('edges')['execution_time_ms'].mean().reset_index()
            grouped = grouped.sort_values('edges')
            plt.plot(grouped['edges'], grouped['execution_time_ms'],
                    marker='o' if algo == 'DFS_Iterative' else 's',
                    linestyle='--', color=colors.get(algo, 'gray'),
                    label=algo, linewidth=2, markersize=8)

    plt.title('Performance Comparison: DFS vs. BFS (Time vs. Number of Edges)', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Edges (E)', fontsize=12)
    plt.ylabel('Execution Time (milliseconds)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    comparison_edges_plot_path = os.path.join(output_path, 'dfs_vs_bfs_performance_edges.png')
    plt.savefig(comparison_edges_plot_path, dpi=150)
    print(f"Saved comparison plot (vs Edges) to {comparison_edges_plot_path}")
    plt.close()

    # ========================================
    # Plot 5: Memory Usage Comparison
    # ========================================
    plt.figure(figsize=(10, 6))

    for algo in ['DFS_Iterative', 'BFS', 'DFS_Recursive']:
        algo_data = size_data[size_data['algorithm'] == algo]
        if not algo_data.empty:
            grouped = algo_data.groupby('nodes')['peak_memory_kb'].mean().reset_index()
            grouped = grouped.sort_values('nodes')
            marker = {'DFS_Iterative': 'o', 'DFS_Recursive': '^', 'BFS': 's'}.get(algo, 'o')
            plt.plot(grouped['nodes'], grouped['peak_memory_kb'],
                    marker=marker, linestyle='-', color=colors.get(algo, 'gray'),
                    label=algo, linewidth=2, markersize=8)

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

    # ========================================
    # Plot 6: Performance by Graph Type (Bar Chart)
    # ========================================
    plt.figure(figsize=(12, 6))

    if not type_data.empty:
        pivot_data = type_data.pivot_table(
            values='execution_time_ms',
            index='graph_type',
            columns='algorithm',
            aggfunc='mean'
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

    # ========================================
    # Plot 7: Comprehensive Analysis Figure
    # ========================================
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Comprehensive DFS vs BFS Analysis', fontsize=16, fontweight='bold')

    # Subplot 1: Time vs Nodes
    ax1 = fig.add_subplot(2, 2, 1)
    for algo in ['DFS_Iterative', 'BFS']:
        algo_data = size_data[size_data['algorithm'] == algo]
        if not algo_data.empty:
            grouped = algo_data.groupby('nodes')['execution_time_ms'].mean().reset_index()
            grouped = grouped.sort_values('nodes')
            ax1.plot(grouped['nodes'], grouped['execution_time_ms'],
                    marker='o' if algo == 'DFS_Iterative' else 's',
                    color=colors.get(algo, 'gray'), label=algo, linewidth=2)
    ax1.set_xlabel('Number of Nodes (V)')
    ax1.set_ylabel('Time (ms)')
    ax1.set_title('Execution Time vs Nodes')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Subplot 2: Time vs Edges
    ax2 = fig.add_subplot(2, 2, 2)
    for algo in ['DFS_Iterative', 'BFS']:
        algo_data = density_data[density_data['algorithm'] == algo]
        if not algo_data.empty:
            grouped = algo_data.groupby('edges')['execution_time_ms'].mean().reset_index()
            grouped = grouped.sort_values('edges')
            ax2.plot(grouped['edges'], grouped['execution_time_ms'],
                    marker='o' if algo == 'DFS_Iterative' else 's',
                    color=colors.get(algo, 'gray'), label=algo, linewidth=2)
    ax2.set_xlabel('Number of Edges (E)')
    ax2.set_ylabel('Time (ms)')
    ax2.set_title('Execution Time vs Edges')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Subplot 3: Memory Usage
    ax3 = fig.add_subplot(2, 2, 3)
    for algo in ['DFS_Iterative', 'BFS']:
        algo_data = size_data[size_data['algorithm'] == algo]
        if not algo_data.empty:
            grouped = algo_data.groupby('nodes')['peak_memory_kb'].mean().reset_index()
            grouped = grouped.sort_values('nodes')
            ax3.plot(grouped['nodes'], grouped['peak_memory_kb'],
                    marker='o' if algo == 'DFS_Iterative' else 's',
                    color=colors.get(algo, 'gray'), label=algo, linewidth=2)
    ax3.set_xlabel('Number of Nodes (V)')
    ax3.set_ylabel('Memory (KB)')
    ax3.set_title('Memory Usage vs Nodes')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Subplot 4: Performance by Graph Type
    ax4 = fig.add_subplot(2, 2, 4)
    if not type_data.empty:
        pivot_data = type_data.pivot_table(
            values='execution_time_ms',
            index='graph_type',
            columns='algorithm',
            aggfunc='mean'
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
