"""Helper functions for advent of code"""

import numpy as np


def read_file(location: str) -> str:
    """Parse the text data from advent of code as string"""
    with open(location, encoding="utf-8") as f:
        data = f.read()
    return data


def split_into_sections(data: str) -> list:
    """If the input contains multiple parts, they are split by a double newline"""
    return data.split("\n\n")


def string_to_array(string):
    """Turn string data into numpy array"""
    return np.array([list(line) for line in string.split("\n")])


def string_to_grid(string: str) -> list[list]:
    """Turn string data into list of lists"""
    return [list(line) for line in string.split("\n")]


def read(location, to_grid=False, to_array=False):
    """Generic reader function, splits into sections, optionally turns into array

    If the data is turned into a numpy array, it shall not be split into sections
    Determines itself whether sections exist; if so: split them
    """
    data = read_file(location)
    if to_grid:
        return string_to_grid(data)
    if to_array:
        return string_to_array(data)

    sections = split_into_sections(data)
    if len(sections) > 1:
        return sections
    return data


def to_ints(lst):
    """Return iterable all converted to int"""
    return list(map(int, lst))


def is_outside_bounds(position: tuple, size) -> bool:
    """Checks whether the position is inside a shape of this size

    Raises ValueError if length of position and size do not match
    """
    if len(position) != len(size):
        raise ValueError(f"Position not of same length as size, {position=}, {size=}")
    for p, s in zip(position, size):
        if p < 0 or p >= s:
            return True
    return False


DIRECTIONS = {
    "N": np.array([-1, 0]),
    "E": np.array([0, 1]),
    "S": np.array([1, 0]),
    "W": np.array([0, -1]),
}


def find_unique_value_coords(arr: np.ndarray, value):
    """Find the coordinates of a unique value in a NumPy array.

    Parameters
    ----------
    arr : np.ndarray
        The array to search
    value :
        the value to locate

    Returns
    -------
    tuple
        Coordinates of the value.

    Raises
    ------
    ValueError
        If the value is not found or occurs multiple times.
    """
    coords = np.argwhere(arr == value)
    if coords.shape[0] != 1:
        raise ValueError("Value occurs zero or multiple times.")
    return tuple(coords[0])


def display_arr(arr):
    """Display array for visual investigation"""
    print("\n".join("".join(row) for row in arr))


def find_first_true(func, options, low=None, high=None):
    """Finds the first option where func evaluates to True, performing binary search

    Parameters
    ----------
    func : callable
        Will be called with the option selected from options. func(options[0]) must be True,
        func(options[-1]) must be False
    options : Iterable
        A subscriptable iterable of options for which the lowest must be found where func evaluates to True
        It must be sorted in a way that before a certain index, func always evaluates to False, and afterwards always to True
    low : the highest known index for which func(option[index]) evaluates to False
    high : the lowest known index for which func(option[index]) evaluates to True

    Returns
    -------
    The first index for which func(options[index]) returns True

    """
    if low is None:
        if func(options[0]):
            return 0
        return find_first_true(func, options, 0, high)
    if high is None:
        high = len(options)
        if func(options[-1]):
            return find_first_true(func, options, low, high)
        raise RuntimeError("No True option found")

    if low == (high - 1):
        return high  # low is always False, high is always True

    mid = (low + high) // 2
    if func(options[mid]):
        return find_first_true(func, options, low, mid)
    return find_first_true(func, options, mid, high)
