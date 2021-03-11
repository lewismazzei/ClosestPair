import random, math

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

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
    middle = left + right // 2
    # get value of first, middle and last elements
    a = lst[left]
    b = lst[middle]
    c = lst[right]
    # return index of a median element
    if b <= a <= c:
        return left
    elif a <= b <= c:
        return middle
    elif a <= c <= b:
        return right

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

if __name__ == '__main__':
    points = [Point(3, 4), Point(3, 5), Point(4, 6), Point(5, 5), Point(6, 6)]
    print(closest_pair(points))

