# Laboratory Work 2: Sorting Algorithms Analysis

## Overview
This laboratory work provides a comprehensive study and empirical analysis of four fundamental sorting algorithms: **QuickSort**, **MergeSort**, **HeapSort**, and **ShellSort**.

## 📁 Directory Structure

```
Lab2/
├── README.md                      # This file - project overview
├── Lab2_Report.md                 # Main laboratory report (academic format)
├── comprehensive_analysis.py      # Complete analysis implementation
├── comprehensive_analysis.png     # Generated visualizations
├── analysis_results.csv          # Raw performance data (generated when run)
├── QuickSort.py                   # Individual QuickSort implementation
├── MergeSort.py                   # Individual MergeSort implementation
├── HeapSort.py                    # Individual HeapSort implementation
└── ShellSort.py                   # Individual ShellSort implementation
```

## 🎯 Project Objectives

1. **Algorithm Implementation**: Implement QuickSort, MergeSort, HeapSort, and ShellSort in Python
2. **Data Properties Analysis**: Establish properties of input data for comprehensive testing
3. **Metrics Definition**: Choose appropriate metrics for algorithm comparison
4. **Empirical Testing**: Perform systematic empirical analysis across multiple test scenarios
5. **Data Visualization**: Create graphical presentations of collected performance data
6. **Analysis Conclusion**: Draw conclusions based on empirical results and theoretical expectations

## 🔬 Analysis Methodology

### Dataset Types Tested
1. **Random Large Dataset**: Random integers (1-1,000,000)
2. **Nearly Sorted Dataset**: Pre-sorted random data
3. **Small Dataset**: 50 elements for overhead analysis
4. **Integer Limited Range**: Values 1-100 for duplicate testing
5. **Floating-Point Dataset**: Random floats for numeric type testing

### Array Sizes Tested
- 1,000 → 2,000 → 5,000 → 10,000 → 20,000 → 50,000 → 100,000 elements

### Metrics Evaluated
- **Execution Time**: Wall-clock performance measurement
- **Memory Usage**: Peak memory consumption during sorting
- **Scalability**: Growth patterns across different array sizes
- **Correctness**: Verification of sorted output

## 📊 Key Findings Summary

### Overall Performance Rankings (50,000 elements, Random Data)
1. **QuickSort**: 0.554s ⭐ (Fastest)
2. **MergeSort**: 1.523s (Consistent)
3. **HeapSort**: 1.811s (Memory Efficient)
4. **ShellSort**: 4.599s (Simple)

### Memory Efficiency Rankings
1. **HeapSort & ShellSort**: ~0.25MB (In-place)
2. **QuickSort & MergeSort**: ~1.25MB (Additional memory)

### Dataset-Specific Winners
- **Random Data**: QuickSort (0.554s)
- **Nearly Sorted**: QuickSort (0.537s)
- **Small Arrays**: ShellSort (0.000054s)
- **Limited Range**: QuickSort (0.048s - exceptional)
- **Floating-Point**: QuickSort (0.565s)

## 🚀 How to Run the Analysis

### Prerequisites
```bash
pip install pandas matplotlib numpy
```

### Execute Complete Analysis
```bash
cd Lab2
python comprehensive_analysis.py
```

### Generated Outputs
- **comprehensive_analysis.png**: 6-panel visualization comparing all algorithms
- **analysis_results.csv**: Raw performance data for further analysis
- **Console Output**: Detailed performance summary and rankings

## 📈 Visualization Panels

The generated `comprehensive_analysis.png` includes:

1. **Algorithm Scalability**: Execution time vs. array size (log scale)
2. **Memory Usage Comparison**: Peak memory vs. array size
3. **Dataset Performance**: Bar chart across different data types
4. **Performance Heatmap**: Color-coded performance matrix
5. **Algorithm Comparison**: Direct comparison for 50K random elements
6. **Efficiency Trends**: Algorithm efficiency across dataset types

## 🏆 Algorithm Recommendations

### Use Case Guide
- **Large Random Data**: QuickSort (fastest)
- **Memory-Constrained**: HeapSort (5x less memory)
- **Guaranteed Performance**: MergeSort (stable O(n log n))
- **Small Arrays**: ShellSort (minimal overhead)
- **Nearly Sorted Data**: QuickSort or ShellSort
- **Many Duplicates**: QuickSort (exceptional performance)

## 📋 Laboratory Tasks Completed

- ✅ **Task 1**: Algorithm implementations in Python
- ✅ **Task 2**: Input data properties established and tested
- ✅ **Task 3**: Comparison metrics defined and measured
- ✅ **Task 4**: Empirical analysis performed across multiple scenarios
- ✅ **Task 5**: Graphical presentation created with 6 visualization panels
- ✅ **Task 6**: Comprehensive conclusions drawn from empirical results

## 🔗 Related Files

- **Course**: Algorithms and Algorithmic Languages
- **Branch**: Lab-2
- **Report Format**: Academic laboratory report with empirical validation
- **Implementation Language**: Python 3.12+

## 📝 Academic Report

See `Lab2_Report.md` for the complete academic laboratory report including:
- Theoretical background and complexity analysis
- Detailed algorithm implementations with code
- Comprehensive empirical results and analysis
- Performance comparison matrices
- Evidence-based conclusions and recommendations
- Future work suggestions

---

**Generated**: March 19, 2026
**Analysis Runtime**: ~2-3 minutes for complete evaluation
**Total Test Cases**: 40+ algorithm-dataset combinations