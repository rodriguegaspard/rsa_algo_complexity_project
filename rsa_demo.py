# A Python implementation of the Quickselect algorithm, the median of medians selection algorithm, and the introselect selection algorithm.
# It compares the performance of those three algorithms using Timeit (more information on : https://docs.python.org/3/library/timeit.html#module-timeit)
import timeit
import random

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quickselect(arr, low, high, k):
    if low < high:
        pivot_index = partition(arr, low, high)
        if pivot_index == k:
            return arr[pivot_index]
        elif pivot_index > k:
            return quickselect(arr, low, pivot_index - 1, k)
        else:
            return quickselect(arr, pivot_index + 1, high, k)
    return arr[low]

def find_kth_smallest(arr, k):
    if k < 1 or k > len(arr):
        return None
    return quickselect(arr, 0, len(arr) - 1, k - 1)

# Performance test on an unsorted array of 10000 random numbers (between 1 and 10000), and looking for a random kth smallest number in the array.
def find_kth_smallest_wrapper() :
    array = [random.randint(1,10000) for _ in range(10000)]
    k = random.randint(1,10000) 
    find_kth_smallest(array, k)

runtime_performance = timeit.timeit(stmt=find_kth_smallest_wrapper, number=100, globals=globals())
print(f"This took {runtime_performance} seconds for 100 loops.")
