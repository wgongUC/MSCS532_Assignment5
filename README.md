# MSCS532_Assignment5 by Weevern Gong

## Description

This project implements deterministic and randomized quick sort in Python. Both versions sort the original list in place using the same Lomuto partition method. The deterministic version uses the last value as the pivot, while the randomized version selects a pivot from the current portion of the list.

## Requirements

- Python 3.10 or higher; tested with Python 3.14.3
- No third-party Python packages are required
- Git is needed only if the repository is cloned

## Instructions

1. Download the repository as a ZIP file or clone it:

```bash
git clone https://github.com/wgongUC/MSCS532_Assignment5.git
cd MSCS532_Assignment5
```

2. Run the quick sort demonstration:

```bash
python quick_sort.py
```

3. Run the unit tests:

```bash
python -m unittest -v
```

The four test methods check both versions on representative lists and edge cases. They also test fixed random seeds, partition boundaries, and whether the original values are preserved.

4. Run the performance comparison:

```bash
python performance_comparison.py
```

The comparison tests random, sorted, and reverse-sorted lists of distinct integers at sizes 100, 200, 400, and 800. Each condition includes one checked, untimed warm-up per algorithm and ten paired measured trials. Both algorithms receive copies of the same input, and their execution order alternates between trials.

Execution time is measured with `time.perf_counter_ns()`. Input generation, copying, expected-result calculation, random-generator creation, correctness checks, and file output occur outside the timed sorting call. Random pivot selections remain part of the randomized quick sort timing, and every result is checked against Python's `sorted()`.

For size `n` and trial `t`, the input seed is `532 + 100 * n + t`. The pivot seed is `532000 + 1000 * n + 100 * distribution_id + t`, where the distribution IDs are 0 for Random, 1 for Sorted, and 2 for Reverse Sorted. Measured trials use 1 through 10, while warm-ups use 0. Separate generators control inputs and pivots, and each random-input trial uses a fresh shuffled list.

Both versions use ordinary recursion. The benchmark requires a recursion limit of at least the largest tested input size plus 100 and does not change it. Larger ordered inputs may exceed the available recursion depth for the deterministic version because its partitions can become highly uneven. Failed recursion or correctness checks stop the run before result files are written.

The script saves 24 summary rows in `results.csv` and 240 measured trials in `timing_trials.csv`. Median time in milliseconds is the main comparison, while mean time is also included. The raw trial file stores execution order, seeds, Python version, platform, and recursion limit. Rerunning the benchmark replaces both CSV files after all results have been validated. Elapsed times will vary; use the same Python version to reproduce the seeded sequences.

## Files

| File | Purpose |
| --- | --- |
| `quick_sort.py` | Contains both quick sort implementations, the shared partition function, and a demonstration |
| `performance_comparison.py` | Runs the performance comparison and saves the verified measurements |
| `test_assignment5.py` | Contains four focused unit-test methods |
| `results.csv` | Stores median and mean execution times for each condition |
| `timing_trials.csv` | Stores individual timing trials, seeds, execution order, and runtime information |
| `WeevernGong_Assignment5_Quick_Sort_Algorithm_Implementation_Analysis_and_Randomization.docx` | Formal report covering the implementation, complexity analysis, experiment, results, and references |
| `.gitignore` | Excludes generated Python cache files |

## Example

Input:

```text
[5, 2, 20, 9, 1, 5, 6, 3, 71, 8, 4, 56, 12]
```

Both versions produce:

```text
[1, 2, 3, 4, 5, 5, 6, 8, 9, 12, 20, 56, 71]
```

## Summary of Findings

The deterministic version was faster on random input at all four tested sizes. At 800 elements, its median time was 0.506450 ms compared with 0.611550 ms for the randomized version. The additional pivot selection and swapping may add some overhead, but the experiment does not measure that effect separately from differences in partition behavior.

The randomized version was much faster on sorted and reverse-sorted input. At size 800, the sorted-input medians were 13.075300 ms for deterministic sorting and 0.366400 ms for randomized sorting. The reverse-sorted medians were 8.306350 ms and 0.375600 ms. These results show how the deterministic last-element pivot is sensitive to ordered input, while random pivot selection reduces that dependence.

The timing results also showed some variation. One deterministic reverse-sorted trial at size 400 took 11.173100 ms, while the median was 2.276700 ms. Both versions also showed a larger increase from 400 to 800 elements on random input than at the smaller sizes. The data does not show what caused these differences, and four tested sizes are not enough to prove the theoretical growth rates.

For distinct values, deterministic quick sort has O(n log n) average time under random input, while randomized quick sort has O(n log n) expected time. Both versions still have O(n²) worst-case time. Their recursive stack space is O(log n) on average or in expectation and O(n) in the worst case. All-equal input can also lead to O(n²) time in both versions because equal values are placed on the same side of the pivot. This case was tested for correctness but was not included in the timing comparison.
