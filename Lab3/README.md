# Laboratory Work 3: Empirical Analysis of DFS and BFS

## Subject
Empirical analysis of algorithms: Depth First Search (DFS), Breadth First Search (BFS)

## Scope Covered

This lab covers the base assignment tasks and also includes extra comparison variants:

1. implementation of DFS and BFS in Python
2. definition of input properties through graph size, graph density, and graph topology
3. comparison metrics:
   execution time, peak memory usage, visited vertices, success status
4. empirical analysis across increasing graph sizes
5. graphical presentation of the obtained data
6. support material for the final report

## Implemented Algorithms

- `DFS_Base`
- `DFS_Optimized`
- `BFS_Base`
- `BFS_Optimized`

## Files

- `dfs.py` - DFS demo implementation
- `bfs.py` - BFS demo implementation
- `graph_generator.py` - legacy graph generation helpers
- `graph_generator_extra.py` - topology-specific generators used by the four-version workflow
- `lab3_common.py` - shared traversal and benchmarking helpers
- `version_1_density_base.py` - density classification, base traversal
- `version_2_density_optimized.py` - density classification, optimized traversal
- `version_3_topology_base.py` - graph-type classification, base traversal
- `version_4_topology_optimized.py` - graph-type classification, optimized traversal
- `run_four_versions.py` - runs all four required versions
- `comprehensive_analysis.py` - legacy broad benchmark
- `density_report_analysis.py` - density summary analysis
- `plot_results.py` - main visualization generator

## Input Data Properties

The laboratory uses two complementary ways of classifying graphs.

### 1. Density / Fill Classification

- graph sizes used by the base density runs: `10, 50, 100, 200`
- density values from `0%` to `100%`
- `version_1_density_base.py` and `version_2_density_optimized.py` use literal fill percentage:
  - `0%` means no edges
  - `100%` means a complete graph

### 2. Graph Type Classification

The topology versions classify the input by named graph type. The generators include:

- `simple_graph`
- `dense_graph`
- `tree`
- `cyclic_graph`
- `bipartite_graph`
- `complete_graph`
- `wheel_graph`
- `grid_planar`
- `weighted_graph`
- `strip_weights`
- `disconnected_graph`

The optimized topology runs include sizes up to `1000` nodes in order to show scaling more clearly.

### Legacy Benchmark Note

`comprehensive_analysis.py` uses an older density interpretation where the lowest density setting corresponds to a connected-tree baseline rather than a truly empty graph. The four dedicated version scripts use the newer literal fill model and are the recommended deliverables for the assignment.

## Metrics

- execution time in milliseconds
- peak memory usage in kilobytes
- visited vertices
- success status
- node count
- edge count
- density percentage

## Run

### Run the Four Required Versions

```bash
cd Lab3
python version_1_density_base.py
python version_2_density_optimized.py
python version_3_topology_base.py
python version_4_topology_optimized.py
```

Or run everything in one step:

```bash
cd Lab3
python run_four_versions.py
```

### Run the Legacy Comprehensive Benchmark

```bash
cd Lab3
python comprehensive_analysis.py
```

### Generate Plots

```bash
cd Lab3
python plot_results.py
```

## Generated Outputs

- `version_1_density_base.csv`
- `version_2_density_optimized.csv`
- `version_3_topology_base.csv`
- `version_4_topology_optimized.csv`
- `performance_data.csv` from the legacy benchmark
- `plots/dfs_performance_vs_nodes.png`
- `plots/bfs_performance_vs_nodes.png`
- `plots/dfs_vs_bfs_performance_nodes.png`
- `plots/dfs_vs_bfs_performance_edges.png`
- `plots/memory_usage_comparison.png`
- `plots/performance_by_graph_type.png`
- `plots/comprehensive_analysis.png`
- `summary/*.csv`
- `summary/*.txt`

## Practical Notes

- BFS is especially useful for shortest paths in unweighted graphs.
- DFS is often useful for reachability, connected components, cycle checks, and structural exploration.
- The optimized variants scale better because they use more suitable containers (`set`, `deque`) for traversal bookkeeping.
- Dense and complete graphs increase the runtime significantly because both algorithms still have to inspect many more edges.

## Theory Links

1. [GeeksforGeeks - BFS](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)
2. [GeeksforGeeks - DFS](https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/)
3. [YouTube - Graph Traversal Algorithms](https://www.youtube.com/watch?v=zaBhtODEL0w)
