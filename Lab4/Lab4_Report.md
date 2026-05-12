# Laboratory Work 4 Report

## Subject
Dynamic programming. Empirical analysis of `Dijkstra` and `Floyd-Warshall`.

## 1. Goal

The goal of this laboratory work is to study shortest path algorithms and compare their empirical behavior on weighted graphs with different densities and sizes.

## 2. Implemented Algorithms

- Dijkstra Classic
- Dijkstra Optimized
- Floyd-Warshall Classic
- Floyd-Warshall Optimized

## 3. Input Data Properties

- weighted directed graphs
- sparse graphs
- medium-density graphs
- dense graphs
- increasing number of nodes
- random positive integer weights in the range `1..20`

## 4. Metrics

- execution time in milliseconds
- peak memory in kilobytes
- number of reachable distances
- number of nodes
- number of edges
- graph density

## 5. Empirical Analysis

The benchmark was executed on several graph sizes. Dijkstra was tested on larger inputs because its asymptotic cost is lower than Floyd-Warshall. Floyd-Warshall was tested on smaller inputs because of its cubic complexity.

The optimized Dijkstra implementation uses a priority queue and is significantly faster than the classic version on larger sparse and dense graphs.

The optimized Floyd-Warshall implementation reduces unnecessary work by skipping unreachable intermediate states, but in Python this optimization does not always outperform the classic version because interpreter overhead can dominate.

## 6. Graphical Presentation

The generated plots are:

- `plots/dijkstra_performance.png`
- `plots/floyd_warshall_performance.png`
- `plots/dijkstra_by_graph_type.png`
- `plots/floyd_warshall_by_graph_type.png`

## 7. Conclusion

The experiments confirm that graph density and the number of nodes strongly influence both algorithms.

- Dijkstra is more suitable for large sparse and medium graphs when single-source shortest paths are needed.
- Floyd-Warshall is useful for all-pairs shortest paths but becomes expensive as the number of nodes increases.
- Optimized implementations usually improve scalability, especially for Dijkstra.

Overall, the empirical analysis matches the theoretical expectation that Floyd-Warshall scales much worse than Dijkstra on larger inputs.
