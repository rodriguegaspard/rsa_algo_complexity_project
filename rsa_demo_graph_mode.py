# A Python implementation of the Quickselect algorithm, the median of medians selection algorithm, and the introselect selection algorithm.
# It compares the performance of those three algorithms using Timeit (more information on : https://docs.python.org/3/library/timeit.html#module-timeit)
import timeit
import random
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

def switchStrategy(name, threshold, number_list, left, right, subset_size_list): # Returns true if it's time to switch pivot selection strategies
    subset_size_list.append(right - left)
    if name == "Subset size sum": # This strategy sums the size of all subsets created so far. If it's greater than len(number_list) * threshold, switch to the median of medians algorithm.
        return sum(subset_size_list) > len(number_list) * threshold
    elif name == "Subset size reduction": # This strategy checks the differences between subset sizes at n recursions and n - k recursions. If the size hasn't been halved, switch to the median of median algorithm. 
        if len(subset_size_list) > threshold:
            return subset_size_list[-1] > (subset_size_list[-threshold] / 2)
    else:
        return None # Nothing to do

def medianOfMedians(number_list, left, right):
    if (left - right) < 5:  # If the subset is less than 5 elements, return the median.
        pivot = sorted(number_list[left:right])[len(number_list[left:right]) // 2]
        for i in range(left, right):
            if number_list[i] == pivot:
                return i
    subsets = [number_list[i:i+5] for i in range(left, right, 3)]   # Divides the list into subsets of 5 elements or less
    medians = [sorted(subset)[len(subset) // 2] for subset in subsets] # Find the median in each subset
    return medianOfMedians(medians, 0, len(medians) - 1)

def quickSelect(number_list, left, right, k, pivot_strategy = None, switching_strategy = None, threshold = 1, subset_size_list = []):
    if left == right: # If there's only one element in the subset, return it.
        return number_list[left]
    if switching_strategy:
        pivot_strategy = "Median of medians" if switchStrategy(switching_strategy, threshold, number_list, left, right, subset_size_list) else pivot_strategy
    # Pivot decision. By default, the pivot is chosen at random between one of the elements of the current subset.
    pivot_index = pivotStrategy(pivot_strategy, number_list, left, right)
    pivot_index = partition(number_list, left, right, pivot_index)
    if pivot_index == k : # If the pivot index is equal to k, we found the kth smallest.
        return number_list[k]
    elif k < pivot_index:   # If the pivot is bigger than k, look for it in the right subset. Else, look for it in the left subset.
        return quickSelect(number_list, left, pivot_index - 1, k, pivot_strategy, threshold, subset_size_list)
    else:
        return quickSelect(number_list, pivot_index + 1, right, k, pivot_strategy, threshold, subset_size_list)

def findKthSmallestQuickSelect(pivot_strategy = None, switching_strategy = None, threshold = 1, number_list = [random.randint(1, 10000) for _ in range(10000)], k = random.randint(0, 9999)):
    return quickSelect(number_list, 0, len(number_list) - 1, k, pivot_strategy, switching_strategy, threshold)

def findKthSmallestPerformanceTest():
    random_index_performance = timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(), number=100, globals=globals())
    moms_performance = timeit.timeit(stmt=lambda : findKthSmallestQuickSelect("Median of medians"), number=100, globals=globals())
    intro_sum_performance = timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(None, "Subset size sum", 5), number=100, globals=globals())
    intro_reduction_performance = timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(None, "Subset size reduction", 5), number=100, globals=globals())
    print("QUICK SELECT ALGORITHM : PERFORMANCE TEST (RANDOM ARRAY OF SIZE 10000, RANDOM K, 100 LOOPS)")
    print("RANDOM PIVOT : " + str(random_index_performance) + " seconds.")
    print("MEDIAN OF MEDIANS : " + str(moms_performance) + " seconds.")
    print("INTROSELECT ALGORITHM - SUBSET SIZE SUM CHECK (THRESHOLD = 5): " + str(intro_sum_performance) + " seconds.")
    print("INTROSELECT ALGORITHM - SUBSET SIZE REDUCTION CHECK (THRESHOLD = 5) : " + str(intro_reduction_performance) + " seconds.")

def findKthSmallestBenchmarkGraph(increment=10, max_range=10000, repetitions=1, low_threshold=10, high_threshold=50):
    x = []
    random_pivot = []
    median_of_medians = []
    intro_sum_low_threshold = []
    intro_sum_high_threshold = []
    intro_reduction_low_threshold = []
    intro_reduction_high_threshold = []
    i = increment
    print("Benchmark in progress. this may take a while.")
    while i <= max_range:
        x.append(i)
        random_pivot.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(None, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=repetitions, globals=globals())*1000)
        median_of_medians.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect("Median of medians", None, 0, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=repetitions, globals=globals())*1000)
        intro_sum_low_threshold.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(None, "Subset size sum", low_threshold, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=repetitions, globals=globals())*1000)
        intro_sum_high_threshold.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(None, "Subset size sum", high_threshold, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=repetitions, globals=globals())*1000)
        intro_reduction_low_threshold.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(None, "Subset size reduction", low_threshold, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=repetitions, globals=globals())*1000)
        intro_reduction_high_threshold.append(timeit.timeit(stmt=lambda : findKthSmallestQuickSelect(None, "Subset size reduction", high_threshold, [random.randint(1, i) for _ in range(i)], random.randint(0, i - 1)), number=repetitions, globals=globals())*1000)
        i += increment
    fig, ax = plt.subplots()
    ax.set_xlabel("Size of randomized list")
    ax.set_ylabel("Time in milliseconds")
    ax.plot(x, random_pivot, 'b', alpha=0.5, label="Random pivot (between left and right)")
    ax.plot(x, median_of_medians, 'r', alpha=0.5, label="Median of medians algorithm")
    ax.plot(x, intro_sum_low_threshold, 'y', alpha=0.5,  label="Introselect low threshold (Subset size sum strategy)")
    ax.plot(x, intro_sum_high_threshold, 'g', alpha=0.5, label="Introselect high threshold (Subset size sum strategy)")
    ax.plot(x, intro_reduction_low_threshold, 'c', alpha=0.5, label="Introselect low threshold (Subset size reduction strategy)")
    ax.plot(x, intro_reduction_high_threshold, 'm', alpha=0.5, label="Introselect high threshold (Subset size reduction strategy)")
    plt.legend()
    plt.show()

def correctDistance(distance, distances):
    if (type(distance) is not int) or (distance < 1):
        print("Incorrect value. Please try again.")
        return False
    elif distance in distances:
        print("This distance was already entered for another house. Please enter a new distance.")
        return False
    else:
        return True

def houseProblem():
    distances = []
    names = ["Andy", "Mary", "Joe", "Liz", "Phil", "Beatriz", "Terrance"]
    for name in names:
        print("Enter the distance between your house and " + name + "'s house :")
        house_distance = int(input())
        while not correctDistance(house_distance, distances):
            house_distance = int(input())
        distances.append(house_distance)

    print("""
Please choose algorithm to use :
--------------------------------
1) - Quickselect (Random pivot selection strategy)
2) - Quickselect (Median of medians pivot selection strategy)
3) - Introselect (Subset size list sum check)
4) - Introselect (Subset size reduction check)""")

    algorithm_selection = int(input())
    while (not int(algorithm_selection)) or (int(algorithm_selection) < 1):
        print("Incorrect value. Please enter a number between 1 and 4")
        algorithm_selection = int(input())

    print("Enter desired k value for the kth nearest house :")
    k = input()
    k = int(k) - 1
    while (not k) or (int(k) < 0) or (int(k) > 6):
        print("Incorrect k value. Please enter a new value for k.")
        k = input()
        k = int(k) - 1

    distances_temp = distances
    if algorithm_selection == 1:
        result = findKthSmallestQuickSelect(None, None, 1, distances_temp, int(k))
    elif algorithm_selection == 2:
        result = findKthSmallestQuickSelect("Median of medians", None, 1, distances_temp, int(k))
    elif algorithm_selection == 3:
        result =findKthSmallestQuickSelect(None, "Subset size sum", 2, distances_temp, int(k))
    else:
        result = findKthSmallestQuickSelect(None, "Subset size reduction", 2, distances_temp, int(k))

    print("The kth nearest house (k = " + str(int(k) + 1) + ") is " + str(names[distances.index(result)]) +"'s house with a distance of " + str(result))

def main():
    print("""
Welcome.
What do you want to do?
-----------------------
1) - House problem
2) - Benchmark performance test
-----------------------

Enter selection :""")
    selection = int(input())
    if selection == 1:
        houseProblem()
    elif selection == 2:
        findKthSmallestPerformanceTest()
    else:
        print("Nothing to do!")

if __name__ == "__main__":
    main()
#findKthSmallestPerformanceTest()
#findKthSmallestBenchmarkGraph(10,10000, 1)
