# A Python implementation of the Quickselect algorithm, the median of medians selection algorithm, and the introselect selection algorithm.
# It compares the performance of those three algorithms using Timeit (more information on : https://docs.python.org/3/library/timeit.html#module-timeit)
import timeit
import random
#import numpy as np
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

def pivotStrategy(name, number_list, left, right):
    if name == "Median of medians":
        return medianOfMedians(number_list, left, right)
    else:
        return random.randint(left, right)

def medianOfMedians(number_list, left, right):
    if (left - right) < 5:  # If the subset is less than 5 elements, return the median.
        pivot = sorted(number_list[left:right])[len(number_list[left:right]) // 2]
        for i in range(left, right):
            if number_list[i] == pivot:
                return i
    subsets = [number_list[i:i+5] for i in range(left, right, 3)]   # Divides the list into subsets of 5 elements or less
    medians = [sorted(subset)[len(subset) // 2] for subset in subsets] # Find the median in each subset
    return medianOfMedians(medians, 0, len(medians) - 1)

def quickSelect(number_list, left, right, k, pivot_strategy = None):
    if left == right: # If there's only one element in the subset, return it.
        return number_list[left]
    # Pivot decision. By default, the pivot is chosen at random between one of the elements of the current subset.
    pivot_index = pivotStrategy(pivot_strategy, number_list, left, right)
    pivot_index = partition(number_list, left, right, pivot_index)
    if pivot_index == k : # If the pivot index is equal to k, we found the kth smallest.
        return number_list[k]
    elif k < pivot_index:   # If the pivot is bigger than k, look for it in the right subset. Else, look for it in the left subset.
        return quickSelect(number_list, left, pivot_index - 1, k, pivot_strategy)
    else:
        return quickSelect(number_list, pivot_index + 1, right, k, pivot_strategy) 

def findKthSmallestQuickSelect(pivot_strategy = None, number_list = [random.randint(1, 10000) for _ in range(10000)], k = random.randint(0, 9999)):
    return quickSelect(number_list, 0, len(number_list) - 1, k, pivot_strategy)

def findKthSmallestPerformanceTest():
    # Random pivot (between left and right indexes)
    random_index_performance = timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(), number=100, globals=globals())
    # Medians of medians algorithm
    moms_performance = timeit.timeit(stmt=lambda : findKthSmallestQuickSelect("Median of medians"), number=100, globals=globals())
    print("QUICK SELECT ALGORITHM : PERFORMANCE TEST (RANDOM ARRAY OF SIZE 10000, RANDOM K, 100 LOOPS)")
    print("RANDOM PIVOT : " + str(random_index_performance) + " seconds.")
    print("MEDIAN OF MEDIANS : " + str(moms_performance) + " seconds.")

def findKthSmallestBenchmarkGraph(increment, max_range, repetitions):
    x = []
    random_pivot = []
    median_of_medians = []
    i = increment
    print("Benchmark in progress. this may take a while.")
    while i <= max_range:
        x.append(i)
        random_pivot.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(None, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=repetitions, globals=globals())*1000)
        median_of_medians.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect("Median of medians", [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=repetitions, globals=globals())*1000)
        i += increment
    fig, ax = plt.subplots()
    ax.set_xlabel("Size of randomized list")
    ax.set_ylabel("Time in milliseconds")
    ax.plot(x, random_pivot, 'b.', label="Random pivot (between left and right)")
    ax.plot(x, median_of_medians, 'r.', label="Median of medians algorithm")
    plt.legend()
    plt.show()

findKthSmallestPerformanceTest()
findKthSmallestBenchmarkGraph(10,10000, 1)

#random_array = [random.randint(1, 100) for _ in range(20)]
#prompt = random.randint(0, 19)
#print("\nPROMPT = " + str(prompt))
#kth_smallest = findKthSmallestQuickSelect("Median of medians", random_array, prompt)
#for n in random_array:
#    print(n, end=" ")
#print()
#sorted_test = sorted(random_array)
#print(str(sorted_test[prompt]) + " = " +  str(kth_smallest) + " ? " + str(sorted_test[prompt] == kth_smallest)) 
