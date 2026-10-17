# Name: Weevern Gong
# Project Title: MSCS532_Assignment5
# Description: This program checks both quick sort versions and their shared partition.
# The tests cover representative inputs, edge cases, and reproducible generated lists.


import random
import unittest

from quick_sort import deterministic_quick_sort, partition, randomized_quick_sort


CORRECTNESS_CASES = [
    [5, 2, 20, 9, 1, 5, 6, 3],
    [],
    [5],
    [2, 1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 1, 3, 2, 1, 3],
    [7, 7, 7, 7, 7],
    [-5, 0, 3, -1, 2, -5],
]


class QuickSortTests(unittest.TestCase):

    def test_deterministic_correctness(self):

        for arr in CORRECTNESS_CASES:
            with self.subTest(input_arr=arr):
                test_arr = arr.copy()
                result = deterministic_quick_sort(test_arr)
                self.assertEqual(test_arr, sorted(arr))
                self.assertIs(result, test_arr)

    def test_randomized_correctness(self):

        for arr in CORRECTNESS_CASES:
            with self.subTest(input_arr=arr):
                test_arr = arr.copy()
                result = randomized_quick_sort(test_arr, random.Random(532))
                self.assertEqual(test_arr, sorted(arr))
                self.assertIs(result, test_arr)

        # Also check the public function when no generator is supplied
        self.assertEqual(randomized_quick_sort([3, 1, 2]), [1, 2, 3])

    def test_seeded_inputs(self):

        input_generator = random.Random(532)
        for size in [2, 10, 50, 100]:
            arr = [input_generator.randint(-size, size) for index in range(size)]
            with self.subTest(size=size, algorithm="Deterministic"):
                self.assertEqual(deterministic_quick_sort(arr.copy()), sorted(arr))
            for seed in [0, 532, 2026]:
                with self.subTest(size=size, algorithm="Randomized", seed=seed):
                    self.assertEqual(
                        randomized_quick_sort(arr.copy(), random.Random(seed)), sorted(arr)
                    )

    def test_partition_correctness(self):

        cases = [
            ([4, 1, 3, 2], 0, 3),
            ([3, 2, 3, 1, 3], 0, 4),
            ([7, 7, 7], 0, 2),
            ([5], 0, 0),
            ([99, 4, -1, 3, 2, -99], 1, 4),
        ]
        for arr, low, high in cases:
            with self.subTest(input_arr=arr, low=low, high=high):
                test_arr = arr.copy()
                pivot = arr[high]
                pivot_index = partition(test_arr, low, high)
                self.assertTrue(low <= pivot_index <= high)
                self.assertEqual(test_arr[pivot_index], pivot)
                self.assertTrue(all(value <= pivot for value in test_arr[low:pivot_index]))
                self.assertTrue(all(value > pivot for value in test_arr[pivot_index + 1:high + 1]))
                self.assertEqual(sorted(test_arr[low:high + 1]), sorted(arr[low:high + 1]))
                # Partitioning must leave values outside its bounds untouched
                self.assertEqual(test_arr[:low], arr[:low])
                self.assertEqual(test_arr[high + 1:], arr[high + 1:])


if __name__ == "__main__":
    unittest.main(verbosity=2)
