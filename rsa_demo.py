# A Python implementation of the Quickselect algorithm, the median of medians selection algorithm, and the introselect selection algorithm.
# It compares the performance of those three algorithms using Timeit (more information on : https://docs.python.org/3/library/timeit.html#module-timeit)

import timeit
import random

# This is used to better visualize the differences in runtime performance between the three algorithms.

def testFunc():
    array = [random.randint(1, 10000) for _ in range(10000)]
    for number in array:
        print(number)

runtime_performance = timeit.timeit(stmt=testFunc, number=2)
print(f"Execution time: {runtime_performance} seconds.")

