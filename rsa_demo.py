# A Python implementation of the Quickselect algorithm, the median of medians selection algorithm, and the introselect selection algorithm.
# It compares the performance of those three algorithms using Timeit (more information on : https://docs.python.org/3/library/timeit.html#module-timeit)
import timeit
import random
import pdb

test_array = [random.randint(1, 100) for _ in range(20)]

def partition(number_list, left, right, pivot_index):
    pivot = number_list[pivot_index]
    number_list[pivot_index], number_list[right] = number_list[right], number_list[pivot_index] # The pivot is put at the end of the subset.
    partition_index = left
    for i in range(left, right):
        if number_list[i] <= pivot:
            number_list[i], number_list[partition_index] = number_list[partition_index], number_list[i]
            partition_index += 1
    number_list[right], number_list[partition_index] = number_list[partition_index], number_list[right]
    return partition_index

def quickSelect(number_list, left, right, k, starting_pivot = None):
    if left == right: # If there's only one element in the subset, return it.
        return number_list[left]
    pivot_index = random.randint(left, right) if starting_pivot is None else starting_pivot # Determines the pivot. If no starting pivot is specified, it is choosed at random. 
    pivot_index = partition(number_list, left, right, pivot_index)
    if pivot_index == k : # If the pivot index is equal to k, we found the kth smallest.
        return number_list[k]
    elif k < pivot_index:   # If the pivot is bigger than k, look for it in the right subset. Else, look for it in the left subset.
        return quickSelect(number_list, left, pivot_index - 1, k)
    else:
        return quickSelect(number_list, pivot_index + 1, right, k) 

def findKthSmallestQuickSelect(number_list = test_array, k = random.randint(0, len(test_array) - 1)):
    return quickSelect(number_list, 0, len(number_list) - 1, k)

runtime_performance = timeit.timeit(stmt=findKthSmallestQuickSelect, number=10000, globals=globals())
print(f"This took {runtime_performance} seconds for 10000 loops.")

random_array = [random.randint(1, 100) for _ in range(20)]
prompt = random.randint(0, 19)
print("\nPROMPT = " + str(prompt))
kth_smallest = findKthSmallestQuickSelect(random_array, prompt)
for n in random_array:
    print(n, end=" ")
print()
sorted_test = sorted(random_array)
print(str(sorted_test[prompt]) + " = " +  str(kth_smallest) + " ? " + str(sorted_test[prompt] == kth_smallest)) 
