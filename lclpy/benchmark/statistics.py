"""This module contains several functions to get statistical data from the
results of the function benchmark.
"""

from operator import itemgetter
import numpy
import statistics
from collections import namedtuple


def _func_on_best_values(benchmark_result, func):
    """The func will be performed on the list of best values.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.
    func
        The function that will be performed on all namedtuples of an
        algorithm-problem pair.

    Returns
    -------
    numpy.ndarray
        The 2 dimensional ndarray will contain the value that the function
        returns. Note that the indices of a certain algorithm-problem pair in
        the benchmark_result will be the same as the indices one needs to get
        the results for that pair.

    """

    position_getter = itemgetter(1)

    result = []

    for algorithm in benchmark_result:

        aid_list = []

        for problem in algorithm:

            aid_list.append(func(map(position_getter, problem)))

        result.append(aid_list)

    return numpy.array(result)


# Functions that do something with the best_value under here

def mean(benchmark_result):
    """A function to calculate the mean of the best_values.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the mean of the best_value for every
        algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_best_values(benchmark_result, statistics.mean)


def median(benchmark_result):
    """A function to calculate the median of the best_values.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the median of the best_value for every
        algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_best_values(benchmark_result, statistics.median)


def stdev(benchmark_result):
    """A function to calculate the standard deviation of the best_values.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the median of the standard variation for every
        algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_best_values(benchmark_result, statistics.stdev)


def biggest(benchmark_result):
    """A function to get the biggest best_values.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the biggest of the best_value for every
        algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_best_values(benchmark_result, max)


def smallest(benchmark_result):
    """A function to get the smallest best_values.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the smallest of the best_value for every
        algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_best_values(benchmark_result, min)


# Functions that do something with the data collected during the run under here


def _func_on_data(benchmark_result, func, position):
    """The func will be performed on the list of best values.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.
    func
        The function that will be performed on all namedtuples of an
        algorithm-problem pair.
    position : int
        The position of the value in the namedtuples that the function will
        use.

    Returns
    -------
    numpy.ndarray
        The 2 dimensional ndarray will contain the value that the function
        returns. Note that the indices of a certain algorithm-problem pair in
        the benchmark_result will be the same as the indices one needs to get
        the results for that pair.

    """

    result = []

    for algorithm in benchmark_result:

        aid_list = []

        for problem in algorithm:

            last_items = []

            for run in problem:
                last_items.append(run.data[position][-1])

            aid_list.append(func(last_items))

        result.append(aid_list)

    return numpy.array(result)


# time

def time_mean(benchmark_result):
    """A function to calculate the mean of the last time-point.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the mean of the last time-point for every
        algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_data(benchmark_result, statistics.mean, 0)


def time_median(benchmark_result):
    """A function to calculate the median of the last time-point.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the median of the last time-point for every
        algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_data(benchmark_result, statistics.median, 0)


def time_stdev(benchmark_result):
    """A function to calculate the standard deviation of the last time-point.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the standard deviation of the last time-point for
        every algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_data(benchmark_result, statistics.stdev, 0)


def time_max(benchmark_result):
    """A function to get the longest execution time.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the longest time for every algorithm-problem
        pair. Note that the indices of a certain algorithm-problem pair in the
        benchmark_result will be the same as the indices one needs to get the
        results for that pair.

    """

    return _func_on_data(benchmark_result, max, 0)


def time_min(benchmark_result):
    """A function to get the shortest execution time.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the shortest time for every algorithm-problem
        pair. Note that the indices of a certain algorithm-problem pair in the
        benchmark_result will be the same as the indices one needs to get the
        results for that pair.

    """

    return _func_on_data(benchmark_result, min, 0)


# iterations

def iterations_mean(benchmark_result):
    """A function to calculate the mean of the amount of iterations.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the mean of the amount of iterations for every
        algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_data(benchmark_result, statistics.mean, 1)


def iterations_median(benchmark_result):
    """A function to calculate the median of the amount of iterations.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the median of the amount of iterations for every
        algorithm-problem pair. Note that the indices of a certain
        algorithm-problem pair in the benchmark_result will be the same as the
        indices one needs to get the results for that pair.

    """

    return _func_on_data(benchmark_result, statistics.median, 1)


def iterations_stdev(benchmark_result):
    """A function to calculate the standard deviation of the amount of iterations.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the standard deviation of the amount of
        iterations for every algorithm-problem pair. Note that the indices of a
        certain algorithm-problem pair in the benchmark_result will be the same
        as the indices one needs to get the results for that pair.

    """

    return _func_on_data(benchmark_result, statistics.stdev, 1)


def iterations_max(benchmark_result):
    """A function to get the most iterations.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the most iterations for every algorithm-problem
        pair. Note that the indices of a certain algorithm-problem pair in the
        benchmark_result will be the same as the indices one needs to get the
        results for that pair.

    """

    return _func_on_data(benchmark_result, max, 1)


def iterations_min(benchmark_result):
    """A function to get the least iterations.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.

    Returns
    -------
    numpy.ndarray
        A 2D array containing the least iterations for every algorithm-problem
        pair. Note that the indices of a certain algorithm-problem pair in the
        benchmark_result will be the same as the indices one needs to get the
        results for that pair.

    """

    return _func_on_data(benchmark_result, min, 1)


def stat(benchmark_result, algorithm_names=None, problem_names=None):
    """A function to get some common characteristics from a benchmark.

    Parameters
    ----------
    benchmark_result : list of list of list of namedtuple
        The result from a benchmark.
    print : bool, optional
        If True, the results will be printed to the command line.
        If False the results will not be printed to the command line.

    Returns
    -------
    namedtuple of namedtuple of numpy.ndarray
        The result is divided in 3 main parts: best_value, time and iterations.
        Every main part contains the results of different statistics:

        - mean
        - median
        - stdev
        - max
        - min

        The result for each of those are kept in a 2D array. Note that the
        indices of a certain algorithm-problem pair in the benchmark_result
        will be the same as the indices one needs to get the results for that
        pair.

    """

    # get the data
    # best_value

    best_value_tuple_class = namedtuple('best_value_statistics', (
        'mean', 'median', 'stdev', 'max', 'min'))

    _mean = mean(benchmark_result)

    _median = median(benchmark_result)

    _stdev = stdev(benchmark_result)

    _biggest = biggest(benchmark_result)

    _smallest = smallest(benchmark_result)

    best_value_tuple = best_value_tuple_class(
        _mean, _median, _stdev, _biggest, _smallest)

    # time

    time_tuple_class = namedtuple('time_statistics', (
        'mean', 'median', 'stdev', 'max', 'min'))

    _time_mean = time_mean(benchmark_result)

    _time_median = time_median(benchmark_result)

    _time_stdev = time_stdev(benchmark_result)

    _time_max = time_max(benchmark_result)

    _time_min = time_min(benchmark_result)

    time_tuple = time_tuple_class(
        _time_mean, _time_median, _time_stdev, _time_max, _time_min)

    # iterations

    iterations_tuple_class = namedtuple('iterations_statistics', (
        'mean', 'median', 'stdev', 'max', 'min'))

    _iterations_mean = iterations_mean(benchmark_result)

    _iterations_median = iterations_median(benchmark_result)

    _iterations_stdev = iterations_stdev(benchmark_result)

    _iterations_max = iterations_max(benchmark_result)

    _iterations_min = iterations_min(benchmark_result)

    iterations_tuple = iterations_tuple_class(
        _iterations_mean, _iterations_median,
        _iterations_stdev, _iterations_max, _iterations_min)

    # combine namedtuples

    combined_tuple_class = namedtuple(
        'benchmark_statistics', ('best_value', 'time', 'iterations'))

    return combined_tuple_class(best_value_tuple, time_tuple, iterations_tuple)
