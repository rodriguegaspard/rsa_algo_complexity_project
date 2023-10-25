# A Python implementation of the Quickselect algorithm, the median of medians selection algorithm, and the introselect selection algorithm.
# It compares the performance of those three algorithms using Timeit (more information on : https://docs.python.org/3/library/timeit.html#module-timeit)
import timeit
import random
import numpy as np
import matplotlib.pyplot as plt


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

def quickSelect(number_list, left, right, k, function_number = 0):
    if left == right: # If there's only one element in the subset, return it.
        return number_list[left]
    # Pivot decision. By default, the pivot is chosen at random between one of the elements of the current subset.
    pivot_strategy = { 0 : random.randint(left, right),
                       1 : left,
                       2 : right,
    }
    pivot_index = pivot_strategy[function_number] 
    pivot_index = partition(number_list, left, right, pivot_index)
    if pivot_index == k : # If the pivot index is equal to k, we found the kth smallest.
        return number_list[k]
    elif k < pivot_index:   # If the pivot is bigger than k, look for it in the right subset. Else, look for it in the left subset.
        return quickSelect(number_list, left, pivot_index - 1, k)
    else:
        return quickSelect(number_list, pivot_index + 1, right, k) 

def findKthSmallestQuickSelect(function_number = 0, number_list = [random.randint(1, 1000) for _ in range(1000)], k = random.randint(0, 999)):
    return quickSelect(number_list, 0, len(number_list) - 1, k, function_number)

def findKthSmallestPerformanceTest():
    # Left index as the pivot
    left_index_performance = timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(1), number=10000, globals=globals())
    # Right index as the pivot
    right_index_performance = timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(2), number=10000, globals=globals())
    # Random pivot (between left and right indexes)
    random_index_performance = timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(), number=10000, globals=globals())
    print("QUICK SELECT ALGORITHM : PERFORMANCE TEST (RANDOM ARRAY OF SIZE 1000, RANDOM K, 10000 LOOPS)")
    print("LEFT PIVOT : " + str(left_index_performance) + " seconds.")
    print("RIGHT PIVOT : " + str(right_index_performance) + " seconds.")
    print("RANDOM PIVOT : " + str(random_index_performance) + " seconds.")

def findKthSmallestBenchmarkGraph(increment, max_range):
    x = []
    left_pivot = []
    right_pivot = []
    random_pivot = []
    i = increment
    print("Benchmark in progress. this may take a while.")
    while i <= max_range:
        x.append(i)
        left_pivot.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(1, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=1, globals=globals())*1000)
        right_pivot.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(2, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=1, globals=globals())*1000)
        random_pivot.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(0, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=1, globals=globals())*1000)
        i += increment
    fig, ax = plt.subplots()
    ax.set_xlabel("Size of randomized list")
    ax.set_ylabel("Time in milliseconds")
    ax.plot(x, left_pivot, 'r.', label="Left pivot")
    ax.plot(x, right_pivot, 'g.', label="Right pivot")
    ax.plot(x, random_pivot, 'b.', label="Random pivot (between left and right)")
    plt.legend()
    plt.show()

findKthSmallestBenchmarkGraph(10,10000)
#random_array = [random.randint(1, 100) for _ in range(20)]
#prompt = random.randint(0, 19)
#print("\nPROMPT = " + str(prompt))
#kth_smallest = findKthSmallestQuickSelect(random_array, prompt)
#for n in random_array:
#    print(n, end=" ")
#print()
#sorted_test = sorted(random_array)
#print(str(sorted_test[prompt]) + " = " +  str(kth_smallest) + " ? " + str(sorted_test[prompt] == kth_smallest)) 
