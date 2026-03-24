# Laboratory Work 3: Empirical Analysis of DFS and BFS Algorithms

## Subject
Empirical analysis of algorithms: Depth First Search (DFS), Breadth First Search (BFS)

## Overview
This laboratory work implements and analyzes two fundamental graph traversal algorithms:
- **Depth First Search (DFS)** - explores as far as possible along each branch before backtracking
- **Breadth First Search (BFS)** - explores all neighbors at the current depth before moving to the next level

## Files Structure

```
Lab3/
├── dfs.py                    # DFS algorithm implementation
├── bfs.py                    # BFS algorithm implementation
├── graph_generator.py        # Various graph generation utilities
├── comprehensive_analysis.py # Main benchmarking and analysis script
├── plot_results.py          # Visualization script
├── performance_data.csv     # Generated performance data (after running analysis)
├── plots/                   # Generated visualization plots
└── README.md               # This documentation
```

## Algorithm Implementations

### DFS (Depth First Search)
- **Recursive Implementation**: Uses call stack for traversal
- **Iterative Implementation**: Uses explicit stack data structure
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)

### BFS (Breadth First Search)
- **Implementation**: Uses queue (deque) data structure
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)

## Input Data Properties

The analysis is performed against graphs with the following properties:

### Graph Sizes (Vertices)
- Density sweep sizes: 100 evenly spaced vertex counts from 2 to 1000 (inclusive)

### Graph Types
1. **Sparse Graph**: ~n edges for n vertices
2. **Dense Graph**: High edge probability (p=0.5)
3. **Tree Structure**: n-1 edges, no cycles
4. **Linear/Path Graph**: Simple chain structure
5. **Grid Graph**: 2D lattice structure
6. **Binary Tree**: Complete binary tree structure

### Edge Densities
- 0%, 5%, 10%, ..., 100% (step 5%)
- Density mapping for each vertex count n:
	- 0% corresponds to n-1 edges (connected tree baseline)
	- 100% corresponds to n(n-1)/2 edges (complete graph)
	- Intermediate levels use linear scaling between these two bounds

## Metrics for Comparison

1. **Execution Time (ms)**: Measured using `time.perf_counter()`
2. **Peak Memory Usage (KB)**: Measured using `tracemalloc`
3. **Vertices Visited**: Number of vertices successfully traversed
4. **Success Rate**: Whether the algorithm completed without errors
5. **Trials per Configuration**: 20 runs per algorithm and configuration (median reported)

## How to Run

### 1. Run the Analysis
```bash
cd Lab3
python comprehensive_analysis.py
```
This will:
- Run a density-only size x density matrix benchmark using the 0%-to-100% edge mapping rule
- Use stepped sizes from 2 to 1000 to keep runtime practical
- Show per-size progress with elapsed time and ETA in the terminal
- Generate `performance_data.csv`

### 2. Generate Visualizations
```bash
python plot_results.py
```
This creates visualizations in the `plots/` directory:
- `dfs_performance_vs_nodes.png`
- `bfs_performance_vs_nodes.png`
- `dfs_vs_bfs_performance_nodes.png`
- `dfs_vs_bfs_performance_edges.png`
- `memory_usage_comparison.png`
- `performance_by_graph_type.png`
- `comprehensive_analysis.png`

### 3. Run Individual Algorithms
```bash
python dfs.py  # Demo of DFS
python bfs.py  # Demo of BFS
```

## Theoretical Background

### DFS (Depth First Search)
DFS uses a stack (either implicit via recursion or explicit) to explore vertices. It goes as deep as possible along each branch before backtracking.

**Characteristics:**
- Uses less memory for wide graphs
- May not find shortest path
- Good for detecting cycles, topological sorting
- Can cause stack overflow on very deep graphs (recursive version)

### BFS (Breadth First Search)
BFS uses a queue to explore vertices level by level, visiting all neighbors at the current depth before moving deeper.

**Characteristics:**
- Finds shortest path in unweighted graphs
- Uses more memory for wide graphs
- Level-order traversal
- Good for finding shortest paths, level-order operations

## Expected Results

### Time Complexity Analysis
Both DFS and BFS have theoretical time complexity of O(V + E):
- For sparse graphs (E ≈ V): O(V)
- For dense graphs (E ≈ V²): O(V²)

### Performance Patterns
1. **Sparse Graphs**: Both algorithms perform similarly
2. **Dense Graphs**: Performance degrades quadratically with vertices
3. **Tree Structures**: Both algorithms are efficient
4. **Linear Graphs**: DFS recursive may cause stack issues; iterative versions perform well

### Memory Usage
- **DFS Iterative**: Stack size ≤ V
- **DFS Recursive**: Call stack depth can reach V (stack overflow risk)
- **BFS**: Queue size can approach V for wide graphs

## Conclusions

### 1. Time Complexity Verification
Both DFS and BFS exhibit O(V + E) time complexity as expected. The empirical analysis confirms that:
- Execution time scales linearly with the sum of vertices and edges
- Dense graphs require significantly more time due to higher edge count

### 2. Algorithm Comparison
- **DFS Iterative** is generally slightly faster due to lower overhead
- **BFS** provides consistent performance and is preferred when shortest paths are needed
- **DFS Recursive** risks stack overflow on large or deep graphs

### 3. Graph Structure Impact
- **Tree structures** show optimal performance for both algorithms
- **Dense graphs** significantly increase execution time
- **Linear graphs** can cause issues with recursive DFS due to deep recursion

### 4. Memory Considerations
- BFS typically uses more memory (queue stores entire levels)
- DFS iterative is more memory-efficient for deep graphs
- Both scale linearly with the number of vertices

### 5. Practical Recommendations
- Use **BFS** when finding shortest paths in unweighted graphs
- Use **DFS Iterative** for memory-efficient traversal
- Avoid **DFS Recursive** for potentially deep graphs
- Choose based on the specific problem requirements (path finding, cycle detection, etc.)

## References

1. [GeeksforGeeks - BFS](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)
2. [GeeksforGeeks - DFS](https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/)
3. [YouTube - Graph Algorithms](https://www.youtube.com/watch?v=zaBhtODEL0w)

## Author
Laboratory Work 3 - Algorithm Analysis Course
