# Laboratory Work 7: Greedy Algorithms

## Subject
Empirical analysis of algorithms: `Prim` and `Kruskal`

## Scope Covered

This lab covers the base assignment tasks and also includes optimized variants:

1. study and implementation of greedy algorithms
2. implementation of `Prim` and `Kruskal`
3. empirical analysis of both algorithms
4. graph-size growth analysis with charts
5. support material for the final report

## Implemented Algorithms

- `Prim_Classic`
- `Prim_Optimized`
- `Kruskal_Classic`
- `Kruskal_Optimized`

## Files

- `graph_utils.py` - connected weighted undirected graph generation
- `prim.py` - Prim implementations
- `kruskal.py` - Kruskal implementations
- `comprehensive_analysis.py` - empirical benchmark runner
- `plot_results.py` - visualization generator
- `Lab5_Report.md` - short academic-style report draft

## Input Data Properties

- graph model: connected weighted undirected graph
- graph types: `sparse`, `medium`, `dense`
- graph sizes: `100, 200, 350, 500, 700`
- edge weights: random integers from `1` to `20`

## Metrics

- execution time in milliseconds
- peak memory in kilobytes
- MST total weight
- number of nodes
- number of edges
- graph density

## Run

```bash
cd Lab5
python comprehensive_analysis.py
python plot_results.py
```

## Generated Outputs

- `performance_data.csv`
- `plots/mst_performance.png`
- `plots/mst_by_graph_type.png`
- `plots/mst_memory.png`
- `plots/mst_memory_by_graph_type.png`
- `summary/median_summary.csv`
- `summary/median_summary.txt`
- `summary/insights.txt`

## Theory Links

1. [Greedy Algorithms - GeeksforGeeks](https://www.geeksforgeeks.org/greedy-algorithms/)
2. [Greedy Algorithms - TutorialsPoint](https://www.tutorialspoint.com/data_structures_algorithms/greedy_algorithms.htm)
3. [Prim's and Kruskal's Algorithm](https://www.scaler.com/topics/prims-and-kruskal-algorithm/)
