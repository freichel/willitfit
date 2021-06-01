'''Helper functions for plotter.py'''
import numpy as np

def get_split_indexes(arr):
    '''Find indexes of where to split an array of coordinates, where shapes are not connected
    Args:
        arr - 3 by n np.array
    returns:
        split_indexes list of indexes to split upon
    '''

    # get difference of each set of coordinates
    diffs = np.diff(arr,1)
    diff_min = np.min(abs(diffs),0)

    # apply a mask, to find which indexes are not connected
    boolmask = (diff_min > 1)
    split_indexes = np.where(boolmask)[0]

    return split_indexes

def split_array_by_index(arr, split_indexes):
    '''Splits an array based on a list of given indexes
    Args:
        split_arrs - 3 by n np.array
        split_indexes - list of indexes to split upon
    '''
    arr = arr.T
    prev = 0
    split_arrs = []
    for element in split_indexes:
        split_arrs.append(arr[prev:element+1].T)
        prev = element+1

    split_arrs.append(arr[prev:].T)

    return split_arrs