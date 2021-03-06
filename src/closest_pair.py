import select, sys, math, random, time

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
    with open(sys.argv[1]) as input_file:
        try:
            for i, line in enumerate(input_file):
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

if __name__ == '__main__':
    # get points from input file
    points = read_input()
    # find distance between closest pair
    d = closest_pair(points)
    # print distance
    print(format_number(signif(d, 9)))

