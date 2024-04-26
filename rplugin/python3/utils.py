import itertools


def with_default_values(arr, default_arr):
    if len(arr) < len(default_arr):
        while len(arr) < len(default_arr):
            arr.append(default_arr[len(arr)])
    return arr
