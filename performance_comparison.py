# Name: Weevern Gong
# Project Title: MSCS532_Assignment5
# Description: This program compares deterministic and randomized quick sort.
# It saves median and mean execution times along with individual timing trials.

# Performance comparison explanation: Test 100, 200, 400, and 800 distinct values
# using random, sorted, and reverse-sorted input. Each paired trial uses identical
# input copies, and the algorithms alternate which runs first. Check one warm-up
# and ten measured trials per condition. Accept a timing only after checking the result.
# Input creation, copying, generator setup, verification, and output are outside timing.


import csv
import platform
import random
import statistics
import sys
import time
from pathlib import Path

from quick_sort import deterministic_quick_sort, randomized_quick_sort


INPUT_SIZES = [100, 200, 400, 800]
DISTRIBUTIONS = ["Random", "Sorted", "Reverse Sorted"]
NUMBER_OF_TRIALS = 10
RANDOM_SEED = 532
RECURSION_MARGIN = 100
OUTPUT_DIRECTORY = Path(__file__).resolve().parent
ALGORITHMS = {
    "Deterministic": deterministic_quick_sort,
    "Randomized": randomized_quick_sort,
}


def create_input(size, distribution, input_seed):

    arr = list(range(size))
    if distribution == "Random":
        input_generator = random.Random(input_seed)
        input_generator.shuffle(arr)
    elif distribution == "Reverse Sorted":
        arr.reverse()
    return arr


def verify_sorted_result(expected_arr, test_arr):

    if test_arr != expected_arr:
        raise ValueError("The sorting algorithm produced an incorrect result.")


def run_performance_comparison():

    # Ordered inputs can require one recursive level for almost every value
    recursion_limit = sys.getrecursionlimit()
    required_limit = max(INPUT_SIZES) + RECURSION_MARGIN
    if recursion_limit < required_limit:
        raise RuntimeError(
            f"The approved benchmark needs a recursion limit of at least {required_limit}; "
            f"the current limit is {recursion_limit}. No results were saved."
        )

    results = []
    trial_results = []
    python_version = platform.python_version()
    system_description = platform.platform()

    for size in INPUT_SIZES:
        for distribution_id, distribution in enumerate(DISTRIBUTIONS):
            execution_times = {name: [] for name in ALGORITHMS}

            # Trial zero is a separate checked warm-up and is not timed or saved
            for trial in range(NUMBER_OF_TRIALS + 1):
                input_seed = RANDOM_SEED + 100 * size + trial
                pivot_seed = RANDOM_SEED * 1000 + 1000 * size + 100 * distribution_id + trial
                input_arr = create_input(size, distribution, input_seed)
                expected_arr = sorted(input_arr)
                algorithm_names = list(ALGORITHMS)
                if trial > 0 and trial % 2 == 0:
                    algorithm_names.reverse()

                for execution_order, algorithm_name in enumerate(algorithm_names, start=1):
                    sort_function = ALGORITHMS[algorithm_name]
                    test_arr = input_arr.copy()
                    sort_arguments = (test_arr,)
                    if algorithm_name == "Randomized":
                        # Generator creation is setup; pivot draws remain inside the sorting call
                        pivot_generator = random.Random(pivot_seed)
                        sort_arguments = (test_arr, pivot_generator)

                    if trial == 0:
                        sort_function(*sort_arguments)
                        verify_sorted_result(expected_arr, test_arr)
                        continue

                    start_time = time.perf_counter_ns()
                    sort_function(*sort_arguments)
                    elapsed_ns = time.perf_counter_ns() - start_time
                    verify_sorted_result(expected_arr, test_arr)
                    elapsed_ms = elapsed_ns / 1_000_000
                    execution_times[algorithm_name].append(elapsed_ms)
                    trial_results.append({
                        "Algorithm": algorithm_name,
                        "Dataset": distribution,
                        "Input Size": size,
                        "Trial": trial,
                        "Execution Order": execution_order,
                        "Input Seed": input_seed if distribution == "Random" else "",
                        "Pivot Seed": pivot_seed if algorithm_name == "Randomized" else "",
                        "Execution Time (ms)": elapsed_ms,
                        "Python Version": python_version,
                        "Platform": system_description,
                        "Recursion Limit": recursion_limit,
                    })

            for algorithm_name, times in execution_times.items():
                results.append({
                    "Algorithm": algorithm_name,
                    "Dataset": distribution,
                    "Input Size": size,
                    "Trials": NUMBER_OF_TRIALS,
                    "Median Execution Time (ms)": statistics.median(times),
                    "Mean Execution Time (ms)": statistics.mean(times),
                })

    return results, trial_results


def save_csv(filename, rows):

    with (OUTPUT_DIRECTORY / filename).open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():

    print("Python version:", platform.python_version())
    print("Platform:", platform.platform())
    print("Processor:", platform.processor() or "Not reported")
    print("Recursion limit:", sys.getrecursionlimit())
    try:
        results, trials = run_performance_comparison()
    except (RecursionError, RuntimeError, ValueError) as error:
        raise SystemExit(f"Benchmark stopped before saving results: {error}") from error

    # Write results only after every warm-up and measured sort has passed validation
    save_csv("results.csv", results)
    save_csv("timing_trials.csv", trials)
    print(f"{'Algorithm':<16}{'Dataset':<18}{'Size':>6}{'Median (ms)':>16}{'Mean (ms)':>16}")
    for row in results:
        print(f"{row['Algorithm']:<16}{row['Dataset']:<18}{row['Input Size']:>6}"
              f"{row['Median Execution Time (ms)']:>16.6f}"
              f"{row['Mean Execution Time (ms)']:>16.6f}")
    print(f"Saved {len(results)} summaries and {len(trials)} measured trials.")
    print("Results saved to results.csv and timing_trials.csv")


if __name__ == "__main__":
    main()
