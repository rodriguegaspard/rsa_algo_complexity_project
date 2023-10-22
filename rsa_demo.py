# A Python implementation of the Quickselect algorithm, the median of medians selection algorithm, and the introselect selection algorithm.
# It compares the performance of those three algorithms using Timeit (more information on : https://docs.python.org/3/library/timeit.html#module-timeit)

import timeit

# Example
execution_time = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
print("This took " + str(execution_time) + " seconds.");
