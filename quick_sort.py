# Name: Weevern Gong
# Project Title: MSCS532_Assignment5
# Description: This program implements deterministic and randomized quick sort.
# Both versions sort in place using the same partition method.

# Quick sort explanation: Partition the current portion, then recursively sort both sides.
# The deterministic version uses the last value as the pivot. The randomized version
# moves a randomly selected value into that position before partitioning.
# For distinct values, average or expected time is O(n log n), with O(n^2) worst-case time.
# Recursive stack space is O(log n) on average or in expectation and O(n) in the worst case.
# Random pivot selection does not prevent quadratic work when all values are equal.


import random


def partition(arr, low, high):

    pivot = arr[high]
    boundary = low

    # Keep values at most equal to the pivot before the boundary
    for index in range(low, high):
        if arr[index] <= pivot:
            arr[boundary], arr[index] = arr[index], arr[boundary]
            boundary += 1

    # Place the pivot between the two portions so it needs no further sorting
    arr[boundary], arr[high] = arr[high], arr[boundary]
    return boundary


def deterministic_quick_sort_recursive(arr, low, high):

    if low < high:
        pivot_index = partition(arr, low, high)
        deterministic_quick_sort_recursive(arr, low, pivot_index - 1)
        deterministic_quick_sort_recursive(arr, pivot_index + 1, high)


def randomized_quick_sort_recursive(arr, low, high, random_generator):

    if low < high:
        # Select from the entire active portion, including both endpoints
        selected_index = random_generator.randint(low, high)
        arr[selected_index], arr[high] = arr[high], arr[selected_index]
        pivot_index = partition(arr, low, high)
        randomized_quick_sort_recursive(arr, low, pivot_index - 1, random_generator)
        randomized_quick_sort_recursive(arr, pivot_index + 1, high, random_generator)


def deterministic_quick_sort(arr):

    deterministic_quick_sort_recursive(arr, 0, len(arr) - 1)
    return arr


def randomized_quick_sort(arr, random_generator=None):

    # Reuse one generator throughout the recursion; callers can supply a seeded one
    if random_generator is None:
        random_generator = random.Random()
    randomized_quick_sort_recursive(arr, 0, len(arr) - 1, random_generator)
    return arr


def main():

    numbers_arr = [5, 2, 20, 9, 1, 5, 6, 3, 71, 8, 4, 56, 12]
    print("Input array:", numbers_arr)
    print("Deterministic Quick Sort:", deterministic_quick_sort(numbers_arr.copy()))
    print("Randomized Quick Sort:", randomized_quick_sort(numbers_arr.copy()))


if __name__ == "__main__":
    main()
