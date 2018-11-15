import string
import numpy
import math
import collections
import itertools


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

    return dist_matrix


def _upper_row_processing(data, dimension):
    """Creates a dict and initialises the distance matrix for a 2D tsp problem.

    Parameters
    ----------
    data : list of string
        The strings in the list contain the upper row of the distance matrix
    dimension : int
        The dimension of the distance matrix.
    Returns
    -------
    dist_matrix : numpy.ndarray
        The distance matrix for the problem.

    """

    # make distance matrix
    dist_matrix = numpy.full((dimension, dimension), 0, dtype=numpy.int_)

    iterator = itertools.chain.from_iterable(data)

    for i in range(dimension):
        for j in range(i, dimension):
            if i != j:
                value = int(next(iterator))

                if value == 0:
                    value = int(next(iterator))
                dist_matrix[i][j] = int(value)
                dist_matrix[j][i] = int(value)

    return dist_matrix


def _lower_row_processing(data, dimension):
    """Creates a dict and initialises the distance matrix for a 2D tsp problem.

    Parameters
    ----------
    data : list of string
        The strings in the list contain the lower row of the distance matrix
    dimension : int
        The dimension of the distance matrix.
    Returns
    -------
    dist_matrix : numpy.ndarray
        The distance matrix for the problem.

    """

    # make distance matrix
    dist_matrix = numpy.full((dimension, dimension), 0, dtype=numpy.int_)

    iterator = itertools.chain.from_iterable(data)

    for i in range(dimension):
        for j in range(i + 1):
            if i != j:
                value = int(next(iterator))

                if value == 0:
                    value = int(next(iterator))
                dist_matrix[i][j] = int(value)
                dist_matrix[j][i] = int(value)

    return dist_matrix


def _matrix_processing(data, dimension):
    """Creates a dict and initialises the distance matrix for a 2D tsp problem.

    Parameters
    ----------
    data : list of string
        The strings in the list contain the full distance matrix
    dimension : int
        The dimension of the distance matrix.
    Returns
    -------
    dist_matrix : numpy.ndarray
        The distance matrix for the problem.

    """

    # make distance matrix
    dist_matrix = numpy.full((dimension, dimension), 0, dtype=numpy.int_)

    iterator = itertools.chain.from_iterable(data)

    for i in range(dimension):
        for j in range(dimension):

            value = int(next(iterator))
            dist_matrix[i][j] = int(value)
            dist_matrix[j][i] = int(value)

    return dist_matrix


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
    dist_func = None
    if 'TSP' in type_metadata[0]:
        solve = _default_processing

        if 'EUC_2D' in type_metadata[1]:
            dist_func = _euclidian
        elif 'MAN_2D' in type_metadata[1]:
            dist_func = _manhattan
        elif 'CEIL_2D' in type_metadata[1]:
            dtype = numpy.int_
            dist_func = _euclidian_rounded_up

        elif any('EXPLICIT' in s for s in metadata):

            if any('UPPER_ROW' in s for s in metadata) \
                    or any('UPPER_DIAG_ROW' in s for s in metadata):
                dtype = numpy.int_
                solve = _upper_row_processing
                dimension_metadata = [s for s in metadata if 'DIMENSION' in s]
                dimension = int(dimension_metadata[0].split()[-1])

            elif any('LOWER_ROW' in s for s in metadata) \
                    or any('LOWER_DIAG_ROW' in s for s in metadata):
                dtype = numpy.int_
                solve = _lower_row_processing
                dimension_metadata = [s for s in metadata if 'DIMENSION' in s]
                dimension = int(dimension_metadata[0].split()[-1])

            elif any('FULL_MATRIX' in s for s in metadata):
                dtype = numpy.int_
                solve = _matrix_processing
                dimension_metadata = [s for s in metadata if 'DIMENSION' in s]
                dimension = int(dimension_metadata[0].split()[-1])
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    if dist_func is None:
        dist_matrix = solve(data, dimension)
    elif dtype is None:
        dist_matrix = solve(data, dist_func)
    else:
        dist_matrix = solve(data, dist_func, dtype)

    # make dictionary, is the same in all cases
    dictionary = {}

    for i in range(dist_matrix.shape[0]):
        dictionary[i] = i + 1

    TsplibData = collections.namedtuple(
        'TsplibData', ['distance_matrix', 'dictionary', 'metadata'])
    return TsplibData(dist_matrix, dictionary, metadata)
