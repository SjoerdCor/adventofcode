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


def read(location, to_array=False):
    """Generic reader function, splits into sections, optionally turns into array

    If the data is turned into a numpy array, it shall not be split into sections
    Determines itself whether sections exist; if so: split them
    """
    data = read_file(location)
    if to_array:
        return string_to_array(data)

    sections = split_into_sections(data)
    if len(sections) > 1:
        return sections
    return data
