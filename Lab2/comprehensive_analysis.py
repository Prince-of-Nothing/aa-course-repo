import random
import time
import tracemalloc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

# ===============================
# SORTING ALGORITHM IMPLEMENTATIONS
# ===============================

def quick_sort(array):
    """QuickSort implementation with random pivot selection"""
    if len(array) <= 1:
        return array
    pivot_index = random.randint(0, len(array) - 1)
    pivot = array[pivot_index]

    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(array):
    """MergeSort implementation"""
    if len(array) <= 1:
        return array

    middle = len(array) // 2
    left_array = array[:middle]
    right_array = array[middle:]

    return merge(merge_sort(left_array), merge_sort(right_array))


def merge(left, right):
    """Helper function for merge sort"""
    sorted_array = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_array.append(left[i])
            i += 1
        else:
            sorted_array.append(right[j])
            j += 1
    return sorted_array + left[i:] + right[j:]


def heap_sort(array):
    """HeapSort implementation (in-place sorting)"""
    arr = array.copy()  # Make a copy to avoid modifying original
    n = len(arr)

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements from the heap one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)

    return arr


def heapify(arr, n, i):
    """Helper function for heap sort"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def shell_sort(array):
    """ShellSort implementation"""
    arr = array.copy()  # Make a copy to avoid modifying original
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

    return arr


# ===============================
# BENCHMARK AND ANALYSIS FUNCTIONS
# ===============================

def benchmark_algorithm(algorithm, array, algorithm_name):
    """Benchmark a single algorithm and return timing and memory data"""
    array_copy = deepcopy(array)

    # Start memory tracking
    tracemalloc.start()

    # Time the algorithm
    start_time = time.perf_counter()
    result = algorithm(array_copy)
    end_time = time.perf_counter()

    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time
    peak_memory_mb = peak / (1024 ** 2)

    return {
        'algorithm': algorithm_name,
        'execution_time': execution_time,
        'peak_memory_mb': peak_memory_mb,
        'sorted_correctly': result == sorted(array)
    }


def generate_datasets(n=100000):
    """Generate various test datasets for analysis"""
    datasets = [
        ("Random Large Dataset", [random.randint(1, 1000000) for _ in range(n)]),
        ("Nearly Sorted Dataset", sorted([random.randint(1, 1000000) for _ in range(n)])),
        ("Small Dataset", [random.randint(1, 100) for _ in range(50)]),
        ("Integer Limited Range (1-100)", [random.randint(1, 100) for _ in range(n)]),
        ("Floating-Point Dataset", [random.uniform(0.0, 1000000.0) for _ in range(n)])
    ]
    return datasets


def run_comprehensive_analysis():
    """Run comprehensive analysis of all sorting algorithms"""
    print("=" * 80)
    print("COMPREHENSIVE SORTING ALGORITHMS ANALYSIS")
    print("Laboratory Work 2: QuickSort, MergeSort, HeapSort, ShellSort")
    print("=" * 80)

    algorithms = {
        'QuickSort': quick_sort,
        'MergeSort': merge_sort,
        'HeapSort': heap_sort,
        'ShellSort': shell_sort
    }

    # Test different array sizes
    sizes = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
    datasets_list = generate_datasets()

    # Store all results
    all_results = []

    print("\n1. SCALABILITY ANALYSIS (Different Array Sizes)")
    print("-" * 50)

    # Test scalability with random data (first dataset)
    random_dataset_name, random_data = datasets_list[0]  # "Random Large Dataset"

    for size in sizes:
        test_array = random_data[:size]
        print(f"\nTesting with array size: {size:,}")

        for algo_name, algo_func in algorithms.items():
            try:
                result = benchmark_algorithm(algo_func, test_array, algo_name)
                result['size'] = size
                result['dataset'] = 'Random Large Dataset'
                all_results.append(result)
                print(f"  {algo_name:12}: {result['execution_time']:.6f}s, {result['peak_memory_mb']:.2f}MB")
            except RecursionError:
                print(f"  {algo_name:12}: RECURSION ERROR (stack overflow)")
                result = {
                    'algorithm': algo_name,
                    'size': size,
                    'dataset': 'Random Large Dataset',
                    'execution_time': float('inf'),
                    'peak_memory_mb': float('inf'),
                    'sorted_correctly': False
                }
                all_results.append(result)

    print("\n2. INPUT DATA TYPE ANALYSIS (Size: 50,000)")
    print("-" * 50)

    # Test different data types with fixed size
    test_size = 50000

    for dataset_name, dataset in datasets_list:
        if dataset_name == "Small Dataset":
            # Use the small dataset as-is (50 elements)
            test_array = dataset
            actual_size = len(test_array)
        else:
            # Use specified test_size for other datasets
            test_array = dataset[:test_size]
            actual_size = test_size

        print(f"\nTesting with {dataset_name} dataset (size: {actual_size:,}):")

        for algo_name, algo_func in algorithms.items():
            try:
                result = benchmark_algorithm(algo_func, test_array, algo_name)
                result['size'] = actual_size
                result['dataset'] = dataset_name
                all_results.append(result)
                print(f"  {algo_name:12}: {result['execution_time']:.6f}s, {result['peak_memory_mb']:.2f}MB")
            except RecursionError:
                print(f"  {algo_name:12}: RECURSION ERROR (stack overflow)")
                result = {
                    'algorithm': algo_name,
                    'size': actual_size,
                    'dataset': dataset_name,
                    'execution_time': float('inf'),
                    'peak_memory_mb': float('inf'),
                    'sorted_correctly': False
                }
                all_results.append(result)

    return all_results, algorithms, datasets_list


def create_visualizations(results_df):
    """Create comprehensive visualizations of the analysis results"""
    plt.rcParams['figure.facecolor'] = 'white'

    # Set up the subplot layout
    fig = plt.figure(figsize=(20, 15))

    # 1. Scalability Analysis - Execution Time vs Array Size
    plt.subplot(2, 3, 1)
    scalability_data = results_df[results_df['dataset'] == 'Random Large Dataset']

    for algo in scalability_data['algorithm'].unique():
        algo_data = scalability_data[scalability_data['algorithm'] == algo]
        valid_data = algo_data[algo_data['execution_time'] != float('inf')]
        if not valid_data.empty:
            plt.plot(valid_data['size'], valid_data['execution_time'],
                    marker='o', linewidth=2, markersize=6, label=algo)

    plt.xlabel('Array Size')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Algorithm Scalability Analysis\n(Execution Time vs Array Size)')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # 2. Memory Usage Comparison
    plt.subplot(2, 3, 2)
    for algo in scalability_data['algorithm'].unique():
        algo_data = scalability_data[scalability_data['algorithm'] == algo]
        valid_data = algo_data[algo_data['peak_memory_mb'] != float('inf')]
        if not valid_data.empty:
            plt.plot(valid_data['size'], valid_data['peak_memory_mb'],
                    marker='s', linewidth=2, markersize=6, label=algo)

    plt.xlabel('Array Size')
    plt.ylabel('Peak Memory Usage (MB)')
    plt.title('Memory Usage Comparison')
    plt.xscale('log')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # 3. Dataset Type Performance (use 50k for large datasets, actual size for small)
    plt.subplot(2, 3, 3)
    # Get data for different dataset sizes and remove duplicates
    dataset_analysis = results_df[
        ((results_df['size'] == 50000) & (~results_df['dataset'].str.contains('Small'))) |
        ((results_df['dataset'] == 'Small Dataset') & (results_df['size'] == 50))
    ]
    dataset_analysis = dataset_analysis[dataset_analysis['execution_time'] != float('inf')]

    # Remove duplicates by taking the mean if there are multiple entries for same dataset-algorithm combo
    if not dataset_analysis.empty:
        dataset_analysis_grouped = dataset_analysis.groupby(['dataset', 'algorithm'])['execution_time'].mean().reset_index()
        pivot_data = dataset_analysis_grouped.pivot(index='dataset', columns='algorithm', values='execution_time')
        if not pivot_data.empty:
            pivot_data.plot(kind='bar', ax=plt.gca(), width=0.8)
            plt.title('Performance on Different Dataset Types')
            plt.xlabel('Dataset Type')
            plt.ylabel('Execution Time (seconds)')
            plt.yscale('log')
            plt.xticks(rotation=45, ha='right')
            plt.legend(title='Algorithm')

    # 4. Algorithm Comparison Heatmap (using imshow instead of seaborn)
    plt.subplot(2, 3, 4)
    heatmap_data = results_df[
        ((results_df['size'] == 50000) & (~results_df['dataset'].str.contains('Small'))) |
        ((results_df['dataset'] == 'Small Dataset') & (results_df['size'] == 50))
    ]
    heatmap_data = heatmap_data[heatmap_data['execution_time'] != float('inf')]

    if not heatmap_data.empty:
        # Remove duplicates by taking the mean
        heatmap_data_grouped = heatmap_data.groupby(['dataset', 'algorithm'])['execution_time'].mean().reset_index()
        heatmap_pivot = heatmap_data_grouped.pivot(index='dataset', columns='algorithm', values='execution_time')

        if not heatmap_pivot.empty:
            # Create heatmap using matplotlib
            im = plt.imshow(heatmap_pivot.values, cmap='YlOrRd', aspect='auto')

            # Set ticks and labels
            plt.xticks(range(len(heatmap_pivot.columns)), heatmap_pivot.columns, rotation=45)
            plt.yticks(range(len(heatmap_pivot.index)), heatmap_pivot.index)

            # Add text annotations
            for i in range(len(heatmap_pivot.index)):
                for j in range(len(heatmap_pivot.columns)):
                    value = heatmap_pivot.iloc[i, j]
                    if not pd.isna(value):
                        plt.text(j, i, f'{value:.4f}',
                                ha='center', va='center', fontsize=8)

            plt.title('Algorithm Performance Heatmap\n(Execution Time in seconds)')
            plt.xlabel('Algorithm')
            plt.ylabel('Dataset Type')
            plt.colorbar(im, label='Execution Time (seconds)', shrink=0.8)

    # 5. Relative Performance Comparison (Large datasets at 50k)
    plt.subplot(2, 3, 5)
    random_50k = results_df[
        (results_df['dataset'] == 'Random Large Dataset') & (results_df['size'] == 50000)
    ]
    random_50k = random_50k[random_50k['execution_time'] != float('inf')]

    if not random_50k.empty:
        algorithms = random_50k['algorithm'].values
        times = random_50k['execution_time'].values
        colors = plt.cm.Set3(np.linspace(0, 1, len(algorithms)))

        bars = plt.bar(algorithms, times, color=colors, alpha=0.8, edgecolor='black')
        plt.title('Algorithm Comparison\n(Random Dataset, 50k elements)')
        plt.xlabel('Algorithm')
        plt.ylabel('Execution Time (seconds)')
        plt.yscale('log')

        # Add value labels on bars
        for bar, time in zip(bars, times):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'{time:.4f}s', ha='center', va='bottom', fontsize=8)

    # 6. Efficiency Ratio Analysis
    plt.subplot(2, 3, 6)
    efficiency_data = results_df[
        ((results_df['size'] == 50000) & (~results_df['dataset'].str.contains('Small'))) |
        ((results_df['dataset'] == 'Small Dataset') & (results_df['size'] == 50))
    ]
    efficiency_data = efficiency_data[efficiency_data['execution_time'] != float('inf')]

    if not efficiency_data.empty:
        # Calculate efficiency as 1/time (higher is better)
        efficiency_data = efficiency_data.copy()
        efficiency_data['efficiency'] = 1 / efficiency_data['execution_time']

        # Remove duplicates by taking the mean
        efficiency_data_grouped = efficiency_data.groupby(['dataset', 'algorithm'])['efficiency'].mean().reset_index()
        efficiency_pivot = efficiency_data_grouped.pivot(index='dataset', columns='algorithm', values='efficiency')
        if not efficiency_pivot.empty:
            efficiency_pivot.plot(kind='line', marker='o', linewidth=2, markersize=6, ax=plt.gca())
            plt.title('Algorithm Efficiency Comparison\n(1/execution_time, higher is better)')
            plt.xlabel('Dataset Type')
            plt.ylabel('Efficiency (1/time)')
            plt.xticks(rotation=45, ha='right')
            plt.legend(title='Algorithm')
            plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('c:\\Users\\Unknown\\Documents\\Repos\\aa-course-repo\\Lab2\\comprehensive_analysis.png',
                dpi=300, bbox_inches='tight')
    plt.show()


def generate_summary_report(results_df):
    """Generate a comprehensive summary report"""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE ANALYSIS SUMMARY REPORT")
    print("=" * 80)

    # Filter out infinite values
    valid_results = results_df[results_df['execution_time'] != float('inf')]

    print("\n3. ALGORITHM PERFORMANCE SUMMARY")
    print("-" * 50)

    # Performance summary for each algorithm
    for algo in valid_results['algorithm'].unique():
        algo_data = valid_results[valid_results['algorithm'] == algo]
        print(f"\n{algo}:")
        print(f"  Average execution time: {algo_data['execution_time'].mean():.6f}s")
        print(f"  Best performance: {algo_data['execution_time'].min():.6f}s")
        print(f"  Worst performance: {algo_data['execution_time'].max():.6f}s")
        print(f"  Average memory usage: {algo_data['peak_memory_mb'].mean():.2f}MB")
        print(f"  Success rate: {(algo_data['sorted_correctly'].sum() / len(algo_data) * 100):.1f}%")

    print("\n4. DATASET IMPACT ANALYSIS")
    print("-" * 50)

    # Get data for appropriate sizes per dataset
    dataset_comparison = valid_results[
        ((valid_results['size'] == 50000) & (~valid_results['dataset'].str.contains('Small'))) |
        ((valid_results['dataset'] == 'Small Dataset') & (valid_results['size'] == 50))
    ]

    if not dataset_comparison.empty:
        for dataset in dataset_comparison['dataset'].unique():
            dataset_data = dataset_comparison[dataset_comparison['dataset'] == dataset]
            if not dataset_data.empty:
                best_algo = dataset_data.loc[dataset_data['execution_time'].idxmin(), 'algorithm']
                best_time = dataset_data['execution_time'].min()
                dataset_size = dataset_data['size'].iloc[0]
                print(f"\n{dataset} (Size: {dataset_size:,}):")
                print(f"  Best algorithm: {best_algo} ({best_time:.6f}s)")
                print(f"  Algorithm ranking:")
                sorted_algos = dataset_data.sort_values('execution_time')
                for i, (_, row) in enumerate(sorted_algos.iterrows(), 1):
                    print(f"    {i}. {row['algorithm']}: {row['execution_time']:.6f}s")

    print("\n5. SCALABILITY ANALYSIS")
    print("-" * 50)

    scalability_data = valid_results[valid_results['dataset'] == 'Random Large Dataset']
    for algo in scalability_data['algorithm'].unique():
        algo_data = scalability_data[scalability_data['algorithm'] == algo].sort_values('size')
        if len(algo_data) >= 2:
            time_growth = algo_data['execution_time'].iloc[-1] / algo_data['execution_time'].iloc[0]
            size_growth = algo_data['size'].iloc[-1] / algo_data['size'].iloc[0]
            growth_factor = time_growth / size_growth
            print(f"\n{algo}:")
            print(f"  Time growth factor: {growth_factor:.2f}x per unit size increase")
            print(f"  From {algo_data['size'].iloc[0]:,} to {algo_data['size'].iloc[-1]:,} elements:")
            print(f"    Time: {algo_data['execution_time'].iloc[0]:.6f}s -> {algo_data['execution_time'].iloc[-1]:.6f}s")

    return valid_results


def save_results_to_csv(results_df):
    """Save results to CSV file for further analysis"""
    output_file = 'c:\\Users\\Unknown\\Documents\\Repos\\aa-course-repo\\Lab2\\analysis_results.csv'
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")


def main():
    """Main function to run the comprehensive analysis"""
    print("Starting Comprehensive Sorting Algorithms Analysis...")

    # Run the analysis
    results, algorithms, datasets_list = run_comprehensive_analysis()

    # Convert to DataFrame for easier analysis
    results_df = pd.DataFrame(results)

    # Generate visualizations
    create_visualizations(results_df)

    # Generate summary report
    final_results = generate_summary_report(results_df)

    # Save results
    save_results_to_csv(results_df)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print(f"Total tests conducted: {len(results)}")
    print(f"Successful tests: {len(final_results)}")
    print("Results saved to analysis_results.csv")
    print("Visualization saved to comprehensive_analysis.png")
    print("=" * 80)


if __name__ == "__main__":
    main()