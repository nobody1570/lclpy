from operator import itemgetter
import numpy
import statistics


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
