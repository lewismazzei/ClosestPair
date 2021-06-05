#!/bin/env python3
import select, sys, math, random, time
# import matplotlib.pyplot as plt

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

# calculate euclidian distance between two points
def distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# return the closest pair through brute force
def closest_pair_brute_force(points):
    d = float('inf')
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            d_temp = distance(points[i], points[j])
            if d_temp < d:
                d = d_temp
    return d

# return index of median of three
def median_of_three(lst, left, right):
    # determine index of middle element
    middle = (left + right) // 2
    # get value of first, middle and last elements
    a = lst[left]
    b = lst[middle]
    c = lst[right]
    # return index of a median element
    if b <= a <= c or c <= a <= b:
        return left
    elif a <= b <= c or c <= b <= a:
        return middle
    elif a <= c <= b or b <= c <= a:
        return right

# partition a list using a provided pivot
def partition(lst, left, right, pivot_index):
    # get value of pivot
    pivot_value = lst[pivot_index]
    # move pivot to end of list
    lst[pivot_index], lst[right] = lst[right], lst[pivot_index]

    # loop through list
    partition_index = left
    for i in range(left, right):
        # if less than pivot
        if lst[i] < pivot_value:
            # swap element with element at partition
            lst[partition_index], lst[i] = lst[i], lst[partition_index]
            # move partition
            partition_index += 1

    # swap pivot with element at partition
    lst[right], lst[partition_index] = lst[partition_index], lst[right]
    # return index of partition
    return partition_index

# return the kth smallest element in lst
def quickselect(lst, left, right, k):
    # if list has one element
    if left == right:
        # return the element
        return lst[left]

    # pick an element as a pivot using the median of three strategy
    pivot_index = median_of_three(lst, left, right)
    # split list using pivot and return index of partition
    partition_index = partition(lst, left, right, pivot_index)
    # if list is suitably sorted
    if k == partition_index:
        # return element at partition
        return lst[partition_index]
    # if list is not suitably sorted
    elif k < partition_index:
        # recurse with elements to the left of the partition
        return quickselect(lst, left, partition_index - 1, k)
    else:
        # recurse with elements to the right of the partition
        return quickselect(lst, partition_index + 1, right, k)

# return the closest pair out of a set of points
def closest_pair(points):
    # base case: brute force
    if len(points) <= 3:
        return closest_pair_brute_force(points)
    # find median x coordinate
    median = quickselect([p.x for p in points], 0, len(points) - 1, len(points) // 2)
    # find closest pair on either side of median
    dl = closest_pair([p for p in points if p.x <= median])
    dr = closest_pair([p for p in points if p.x > median])
    # determine the  closer of these two pairs
    d = min(dl, dr)
    # filter points within d of the median
    points = [p for p in points if median - d < p.x < median + d]
    # sort points by y
    points.sort(key = lambda p: p.y)
    # slide window from bottom to top
    for i, p in enumerate(points):
        j = i + 1
        while j < i + 7 and j < len(points):
            if points[j].y - points[i].y < d:
                d_temp = distance(points[i], points[j])
                if d_temp < d:
                    d = d_temp
                j += 1
            else:
                break
    return d

# exit program gracefully on erroneous input
def exit_program(reason):
    if reason == 'format':
        print('Incorrectly formatted input\n')
    exit(0)

# credit: https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
def signif(x, digits=6):
    if x == 0 or not math.isfinite(x):
        return x
    digits -= math.ceil(math.log10(abs(x)))
    return round(x, digits)

# credit: https://stackoverflow.com/questions/38282697/how-can-i-remove-0-of-float-numbers
def format_number(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num

# return random point
def random_point():
    return Point(random.random() * sys.maxsize, random.random() * sys.maxsize)

# read input from file
def read_input():
    n = 0
    points = []
    try:
        for i, line in enumerate(sys.stdin):
            if i == 0:
                n = int(line)
            else:
                try:
                    # python does not use the plus symbol for scientific notation
                    line = line.replace('+', '')
                    line = line.split(' ')
                    points.append(Point(float(line[0]), float(line[1])))

                except (AttributeError, IndexError, ValueError) as e:
                    exit_program('format')

    except (UnicodeDecodeError, ValueError) as e:
        exit_program('format')

    if n < 2 or len(points) != n:
        exit_program('format')

    return points

# run program once and print solution
def run_program(points):
    d = closest_pair(points)
    print(format_number(signif(d, 9)))

# run program multiple times for a range of n, record times for each
def run_experiment(max_n, test='random'):
    with open(f'../experiments/output-{test}-{max_n}.csv', 'w') as file:
        # file.write(f'n,time\n')
        x = []
        y = []
        for n in range(2, max_n + 1):
            if n % 100 == 0:
                print(n)
            for _ in range(10):
                points = [random_point() for p in range(n)]
                if test == 'random':
                    time_started = time.process_time()
                    closest_pair(points)
                    time_elapsed = time.process_time_ns() - time_started
                if test == 'worst-case':
                    points = sorted(points, key=lambda p: [p.y, p.x])
                    time_started = time.process_time()
                    closest_pair(points)
                    time_elapsed = time.process_time_ns() - time_started
                x.append(n)
                y.append(time_elapsed)
                file.write(f'{n},{time_elapsed}\n')

# plot n against time on a graph
def graph_results(filepath):
    x = []; y = []
    with open(filepath) as file:
        for line in file:
            line = line.replace('\n', '').split(',')
            x.append(float(line[0]))
            y.append(float(line[1]))

        # plt.plot(x, y)
        # plt.show()

# modified version to simulate worst case
def modified_quickselect(lst, left, right, k):
    if left == right:
        return lst[left]

    # pick worst pivot for sorted list
    pivot_index = left
    partition_index = partition(lst, left, right, pivot_index)
    if k == partition_index:
        return lst[partition_index]
    elif k < partition_index:
        return quickselect(lst, left, partition_index - 1, k)
    else:
        return quickselect(lst, partition_index + 1, right, k)

def analyse_results(filepath):
    with open(filepath) as file:
        for line in file:
            line = line.replace('\n', '').split(',')

if __name__ == '__main__':
    # run program with points from an input file
    run_program(read_input())

    # run experiment - max_n, 'random' or 'worst-case' (i.e. sorted points plus first-element pivot)
    # run_experiment(2000, 'worst-case')

    # analyse results
    # analyse_results('../experiments/output-worst-case.csv')

    # graph results
    # graph_results('../experiments/output-worst-case-2000.csv')

