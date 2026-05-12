# Laboratory Work 5 Report

## Subject
Greedy algorithms. Empirical analysis of `Prim` and `Kruskal`.

## 1. Goal

The goal of this laboratory work is to study greedy algorithm design and compare Prim and Kruskal on weighted graphs of different sizes and densities.

## 2. Implemented Algorithms

- Prim Classic
- Prim Optimized
- Kruskal Classic
- Kruskal Optimized

## 3. Input Data Properties

- connected weighted undirected graphs
- sparse graphs
- medium-density graphs
- dense graphs
- increasing number of nodes
- random positive edge weights in the range `1..20`

## 4. Metrics

- execution time in milliseconds
- peak memory in kilobytes
- total weight of the minimum spanning tree
- number of nodes
- number of edges
- graph density

## 5. Empirical Analysis

The benchmark compares classic and optimized implementations on graphs with different edge probabilities.

The optimized Prim implementation uses a priority queue and usually scales better than the classic version. The optimized Kruskal implementation uses a disjoint-set structure and is generally more efficient than the classic component-merging approach, especially as graph size increases.

Dense graphs increase the workload for both algorithms because they introduce many more candidate edges.

## 6. Graphical Presentation

The generated plots are:

- `plots/mst_performance.png`
- `plots/mst_by_graph_type.png`

## 7. Conclusion

The results show that the number of nodes and graph density strongly influence MST algorithms.

- Prim and Kruskal both become slower as the graph grows.
- Optimized variants are usually more scalable than the classic variants.
- Dense graphs produce the highest running times because the number of candidate edges grows quickly.

The empirical results support the theoretical expectation that data structures play a major role in the practical efficiency of greedy graph algorithms.
