import string
import numpy
import math
import collections


def _euclidian(from_x, from_y, to_x, to_y):
    """Calculates the euclidian distance between 2 points in 2D space.

    Parameters
    ----------
    from_x : int or float
        The x coordinate of the 1st point.
    from_y : int or float
        The y coordinate of the 1st point.
    to_x : int or float
        The x coordinate of the 2nd point.
    to_y : int or float
        The y coordinate of the 2nd point.

    Returns
    -------
    float
        The euclidian distance between the 2 points.


    """
    return math.sqrt((to_x - from_x)**2 + (to_y - from_y)**2)


def _euclidian_rounded_up(from_x, from_y, to_x, to_y):
    return int(math.ceil(math.sqrt((to_x - from_x)**2 + (to_y - from_y)**2)))
    """Calculates the euclidian distance between 2 points in 2D space.

    Parameters
    ----------
    from_x : int or float
        The x coordinate of the 1st point.
    from_y : int or float
        The y coordinate of the 1st point.
    to_x : int or float
        The x coordinate of the 2nd point.
    to_y : int or float
        The y coordinate of the 2nd point.

    Returns
    -------
    int
        The euclidian distance between the 2 points, rounded up to the nearest
        int.


    """


def _manhattan(from_x, from_y, to_x, to_y):
    """Calculates the manhattan distance between 2 points in 2D space.

    Parameters
    ----------
    from_x : int or float
        The x coordinate of the 1st point.
    from_y : int or float
        The y coordinate of the 1st point.
    to_x : int or float
        The x coordinate of the 2nd point.
    to_y : int or float
        The y coordinate of the 2nd point.

    Returns
    -------
    int or float
        The manhattan distance between the 2 points.


    """
    return abs(to_x - from_x) + abs(to_y - from_y)


def _default_processing(data, dist_func, type=numpy.float_):
    """Creates a dict and calculates the distance matrix for a 2D tsp problem.

    Parameters
    ----------
    data : list of string
        The strings in the list always contain the name of a point,
        the x coordinate and the y coordinate in that order seperated by
        spaces.
    dist_func : function
        A function to calculate the distance between the points. This
        function's arguments must be the x and y coordinates of the first
        point, followed by the x and y coordinates of the second point.
    type : numpy.dtype, optional
        The data type used by the numpy array. The default is numpy.float_,
        which is the default datatype when creating a numpy.ndarray.

    Returns
    -------
    dist_matrix : numpy.ndarray
        The distance matrix for the problem.
    dictionary : {int : int}
        A dictionary that can convert a position the distance matrix to the
        name given in data.


    """

    # make dictionary
    dictionary = {}

    position = 0

    for point in data:
        dictionary[position] = int(point[0])
        position += 1

    # make dist_matrix
    size = len(data)

    # dist_matrix [from] [to]
    dist_matrix = numpy.full((size, size), numpy.inf, dtype=type)

    for i in range(size):

        # get coordinates point
        i_dist_x = data[i][1]
        i_dist_y = data[i][2]

        for j in range(size):
            # get coordinates all points
            j_dist_x = data[j][1]
            j_dist_y = data[j][2]

            # calculate distance
            dist_matrix[i][j] = dist_func(
                i_dist_x, i_dist_y, j_dist_x, j_dist_y)

    DefaultProcessingResults = collections.namedtuple(
        'DefaultProcessingResults', ['distance_matrix', 'dictionary'])

    return DefaultProcessingResults(dist_matrix, dictionary)


def read_tsplib(filename):
    """Converts the tsplib file format to useable data structures.

    Currently this function works for the sub types EUC_2D, MAN_2D and CEIL_2D.

    Parameters
    ----------
    filename : str
        absolute or relative path to the file that contains the data.

    Returns
    -------
    distance_matrix : numpy.ndarray
        The distance matrix for the problem.
    dictionary : {int : int}
        A dictionary that can convert a position the distance matrix to the
        name given in the data.
    metadata : list of str
        Contains the metadata of the problem. The last entry will always be
        EOF.

    Examples
    --------
    Read "testfile.tsp" from the map "data" in the current working directory:

    .. code-block:: python

        from locsearch.io.tsplib import read_tsplib
        read_tsplib('data/testfile.tsp')

    """

    metadata = []
    data = []

    # read data
    with open(filename) as f:
        for line in f:
            if line[:1] in string.ascii_uppercase:
                metadata.append(line)
            else:
                splitted = line.split()
                numbers = []
                for i in splitted:
                    numbers.append(float(i))
                data.append(numbers)

    # check problem type and data type
    type_metadata = [s for s in metadata if 'TYPE' in s]

    # choose problem type

    dtype = None
    if 'TSP' in type_metadata[0]:
        solve = _default_processing
    else:
        raise NotImplementedError

    if 'EUC_2D' in type_metadata[1]:
        dist_func = _euclidian
    elif 'MAN_2D' in type_metadata[1]:
        dist_func = _manhattan
    elif 'CEIL_2D' in type_metadata[1]:
        dtype = numpy.int_
        dist_func = _euclidian_rounded_up
    else:
        raise NotImplementedError

    if dtype is None:
        (dist_matrix, dictionary) = solve(data, dist_func)
    else:
        (dist_matrix, dictionary) = solve(data, dist_func, dtype)

    TsplibData = collections.namedtuple(
        'TsplibData', ['distance_matrix', 'dictionary', 'metadata'])
    return TsplibData(dist_matrix, dictionary, metadata)
