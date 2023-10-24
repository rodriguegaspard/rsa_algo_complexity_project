# A Python implementation of the Quickselect algorithm, the median of medians selection algorithm, and the introselect selection algorithm.
# It compares the performance of those three algorithms using Timeit (more information on : https://docs.python.org/3/library/timeit.html#module-timeit)
import timeit
import random

test_array = [1, 3, 7, 3, 4, 5, 6, 7, 9, 7, 5, 8, 4, 2, 1, 1, 2, 4]

# Partitions a list given as argument into two subsets, depending on the value of the pivot.
def partition(number_list, left, right, pivot_index):
    pivot = number_list[pivot_index]
    number_list[pivot_index], number_list[right] = number_list[right], number_list[pivot_index] # The pivot is put at the end of the subset.
    partition_index = left # The partition index is put at the beginning of the subset.
    for i in range(left, right - 1):
        if number_list[i] < pivot:
            number_list[partition_index], number_list[i] = number_list[i], number_list[partition_index] # If the current value is smaller than the pivot, put it "behind" the partition index
            partition_index = partition_index + 1
    number_list[right], number_list[partition_index] = number_list[partition_index], number_list[right] 
    return partition_index # Put the partition index at the end of the subset and returns it. This ensures that every value left of the partition index are smaller than the pivot.

# Performance test on an unsorted array of 10000 random numbers (between 1 and 10000), and looking for a random kth smallest number in the array.
#def find_kth_smallest_wrapper() :
#    array = [random.randint(1,10000) for _ in range(10000)]
#    k = random.randint(1,10000) 
#    find_kth_smallest(array, k)

#runtime_performance = timeit.timeit(stmt=find_kth_smallest_wrapper, number=100, globals=globals())
#print(f"This took {runtime_performance} seconds.")

print(partition(test_array, 0, len(test_array) -1, 11))
