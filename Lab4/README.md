# Laboratory Work 5: Dynamic Programming

## Subject
Empirical analysis of algorithms: `Dijkstra` and `Floyd-Warshall`

## Scope Covered

This lab covers the base assignment tasks and also includes optimized variants:

1. implementation of `Dijkstra` and `Floyd-Warshall`
2. input data definition through sparse, medium, and dense weighted directed graphs
3. comparison metrics:
   execution time, peak memory, reachable distances, number of nodes, number of edges, density
4. empirical analysis across increasing graph sizes
5. graphical presentation of benchmark results
6. support material for the final report

## Implemented Algorithms

- `Dijkstra_Classic`
- `Dijkstra_Optimized`
- `FloydWarshall_Classic`
- `FloydWarshall_Optimized`

## Files

- `graph_utils.py` - weighted directed graph generation
- `dijkstra.py` - Dijkstra implementations
- `floyd_warshall.py` - Floyd-Warshall implementations
- `comprehensive_analysis.py` - empirical benchmark runner
- `plot_results.py` - visualization generator
- `Lab4_Report.md` - short academic-style report draft

## Input Data Properties

- graph model: weighted directed graph
- graph types: `sparse`, `medium`, `dense`
- Dijkstra sizes: `100, 250, 500, 1000, 1500`
- Floyd-Warshall sizes: `25, 50, 75, 100, 125`
- edge weights: random integers from `1` to `20`

## Run

```bash
cd Lab4
python comprehensive_analysis.py
python plot_results.py
```

## Generated Outputs

- `performance_data.csv`
- `plots/dijkstra_performance.png`
- `plots/floyd_warshall_performance.png`
- `plots/dijkstra_memory.png`
- `plots/floyd_warshall_memory.png`
- `plots/dijkstra_by_graph_type.png`
- `plots/floyd_warshall_by_graph_type.png`
- `plots/dijkstra_memory_by_graph_type.png`
- `plots/floyd_warshall_memory_by_graph_type.png`
- `summary/median_summary.csv`
- `summary/median_summary.txt`
- `summary/insights.txt`

## Theory Links

1. [Dynamic Programming - GeeksforGeeks](https://www.geeksforgeeks.org/dynamic-programming/)
2. [Dynamic Programming - TutorialsPoint](https://www.tutorialspoint.com/data_structures_algorithms/dynamic_programming.htm)
3. [Dijkstra vs Floyd-Warshall](https://www.codingninjas.com/codestudio/library/dijkstras-algorithm-vs-floydwarshalls-algorithm)
