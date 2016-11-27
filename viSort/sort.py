
import random
import time

def quicksorter(lst):
    pass

def quicksort_helper(lst, start=0, end=None):
    pass

def partition(lst, start, end):
    pivot = lst[0]

def mergesorter(lst):
    to_sort = [[x] for x in lst]
    i = 0
    while len(to_sort) > 1:
        if i >= len(to_sort) - 1:
            i = 0
        to_sort.insert(i, merge(to_sort.pop(i), to_sort.pop(i)))
        i += 1
        yield [x for sub_list in to_sort for x in sub_list]

def merge(lst1, lst2):
    if not lst1:
        return lst2
    elif not lst2:
        return lst1
    elif lst1[0] < lst2[0]:
        return [lst1.pop(0)] + merge(lst1, lst2)
    else:
        return [lst2.pop(0)] + merge(lst1, lst2)

def insertionsorter(lst):
    for i in range(len(lst)):
        while i > 0 and lst[i - 1] > lst[i]:
            lst[i], lst[i - 1] = lst[i - 1], lst[i]
            i -= 1
            yield(lst)
        yield(lst)
        time.sleep(0.0005)


def heapsorter(lst):
    pass

def heapify(lst):
    pass

def bubblesorter(lst):
    pass


def selectionsorter(lst):
    for i in range(len(lst)):
        min_ind, min_elem = min(enumerate(lst[i:]), key=lambda x: x[1])
        lst[i], lst[min_ind + i] = lst[min_ind + i], lst[i]
       	yield lst
