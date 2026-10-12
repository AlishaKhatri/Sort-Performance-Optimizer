
"""
Sorting Assignment
Sorting Algorithms, Stability Analysis, and Performance Benchmarking
"""

import json
import time
import tracemalloc


# ============================================================
# PART 1: SORTING IMPLEMENTATIONS
# ============================================================

def bubble_sort(arr, key=lambda x: x):
    """Sort using Bubble Sort."""
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


def selection_sort(arr, key=lambda x: x):
    """Sort using Selection Sort."""
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if key(arr[j]) < key(arr[min_index]):
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


def insertion_sort(arr, key=lambda x: x):
    """Sort using Insertion Sort."""
    arr = arr.copy()

    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1

        while j >= 0 and key(arr[j]) > key(current):
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = current

    return arr


def merge_sort(arr, key=lambda x: x):
    """Sort using Merge Sort."""

    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2

    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ============================================================
# PART 2: STABILITY DEMONSTRATION
# ============================================================

def demonstrate_stability():

    products = [
        {"name": "Widget A", "price": 1999, "original_position": 0},
        {"name": "Gadget B", "price": 999, "original_position": 1},
        {"name": "Widget C", "price": 1999, "original_position": 2},
        {"name": "Tool D", "price": 999, "original_position": 3},
        {"name": "Widget E", "price": 1999, "original_position": 4},
    ]

    algorithms = {
        "bubble_sort": bubble_sort,
        "selection_sort": selection_sort,
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort
    }

    results = {}

    for name, algorithm in algorithms.items():

        sorted_products = algorithm(
            products,
            key=lambda item: item["price"]
        )

        stable = True
        positions_by_price = {}

        for product in sorted_products:
            price = product["price"]

            if price not in positions_by_price:
                positions_by_price[price] = []

            positions_by_price[price].append(
                product["original_position"]
            )

        for positions in positions_by_price.values():
            if positions != sorted(positions):
                stable = False

        if stable:
            results[name] = "Stable"
        else:
            results[name] = "Unstable"

    return results


# ============================================================
# PART 3: PERFORMANCE BENCHMARKING
# ============================================================

def load_dataset(filename):
    """Load a dataset from JSON file."""

    with open(f"datasets/{filename}", "r") as f:
        return json.load(f)


def load_test_cases():
    """Load test cases for validation."""

    with open("datasets/test_cases.json", "r") as f:
        return json.load(f)


def test_sorting_correctness():

    print("=" * 70)
    print("TESTING SORTING CORRECTNESS")
    print("=" * 70)

    test_cases = load_test_cases()

    test_names = [
        "small_random",
        "small_sorted",
        "small_reverse",
        "small_duplicates"
    ]

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort
    }

    for test_name in test_names:

        print(f"\nTest: {test_name}")

        data = test_cases[test_name]
        expected = test_cases["expected_sorted"][test_name]

        print(f"Input: {data}")
        print(f"Expected: {expected}")

        for algo_name, algo_func in algorithms.items():

            try:
                result = algo_func(data.copy())

                if result == expected:
                    status = "PASS"
                else:
                    status = "FAIL"

                print(f"{algo_name}: {status}")

            except Exception as e:
                print(f"{algo_name}: ERROR - {e}")


def benchmark_algorithm(sort_func, data):
    """
    Measure execution time and peak memory usage.

    Returns:
        execution_time_ms, peak_memory_kb
    """

    data_copy = data.copy()

    tracemalloc.start()

    start_time = time.perf_counter()

    result = sort_func(data_copy)

    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if result != sorted(data):
        raise ValueError("Sorting algorithm produced incorrect results")

    execution_time_ms = (end_time - start_time) * 1000

    peak_memory_kb = peak / 1024

    return execution_time_ms, peak_memory_kb


def benchmark_all_datasets():

    print("\n" + "=" * 70)
    print("BENCHMARKING SORTING ALGORITHMS")
    print("=" * 70)

    datasets = {
        "orders.json": ("Order Processing Queue", 50000, 5000),
        "products.json": ("Product Catalog", 100000, 5000),
        "inventory.json": ("Inventory Reconciliation", 25000, 5000),
        "activity_log.json": ("Customer Activity Log", 75000, 5000)
    }

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort
    }

    all_results = {}

    for filename, (description, full_size, sample_size) in datasets.items():

        print(f"\nDataset: {description}")
        print(f"Sample Size: {sample_size:,}")
        print("-" * 70)

        data = load_dataset(filename)

        data_sample = data[:sample_size]

        all_results[description] = {}

        for algo_name, algo_func in algorithms.items():

            try:
                exec_time, memory = benchmark_algorithm(
                    algo_func,
                    data_sample
                )

                print(
                    f"{algo_name:20s}: "
                    f"{exec_time:10.2f} ms | "
                    f"{memory:10.2f} KB"
                )

                all_results[description][algo_name] = {
                    "runtime_ms": round(exec_time, 3),
                    "memory_kb": round(memory, 3)
                }

            except Exception as e:
                print(f"{algo_name}: ERROR - {e}")

        print()

    with open("benchmark_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

    print("Benchmark results saved to benchmark_results.json")

    return all_results


# ============================================================
# PART 4: STABILITY ANALYSIS
# ============================================================

def analyze_stability():

    print("\n" + "=" * 70)
    print("STABILITY ANALYSIS")
    print("=" * 70)

    results = demonstrate_stability()

    for algo_name, stability in results.items():
        print(f"{algo_name:20s}: {stability}")

    print()


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("SORTING ASSIGNMENT")
    print("Testing sorting algorithms and performance\n")

    test_sorting_correctness()

    analyze_stability()

    benchmark_all_datasets()

    print("\nAll tests and benchmarks completed.")
