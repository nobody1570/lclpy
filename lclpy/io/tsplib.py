import string
import numpy
import math
import collections
import itertools

PI = 3.141592
RRR = 6378.388


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
    int
        The euclidian distance between the 2 points. Rounded to the nearest
        int.


    """

    return int(round(math.sqrt((to_x - from_x)**2 + (to_y - from_y)**2)))


def _euclidian_rounded_up(from_x, from_y, to_x, to_y):
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

    return int(math.ceil(math.sqrt((to_x - from_x)**2 + (to_y - from_y)**2)))


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
    int
        The manhattan distance between the 2 points. Rounded to the
        nearest int.


    """

    return int(round(abs(to_x - from_x) + abs(to_y - from_y)))


def _degrees_to_radian(angle_degrees):
    """Converts radian to degrees.

    The numbers behind the point are minutes, not degrees. This is simply a
    convention of tsplib, don't worry about it.

    Parameters
    ----------
    angle_degrees : float
        An angle in degrees.

    Returns
    -------
    float
        The angle in radian.

    """

    degrees = int(angle_degrees)
    minutes = angle_degrees - degrees

    return PI * (degrees + 5.0 * minutes / 3.0) / 180.0


def _geo(from_x, from_y, to_x, to_y):
    """Calculates the manhattan distance between 2 points on the globe.

    Parameters
    ----------
    from_x : int or float
        Latitude of the 1st point.
    from_y : int or float
        Longitude of the 1st point.
    to_x : int or float
        Latitude of the 2nd point.
    to_y : int or float
        Longitude of the 2nd point.

    Returns
    -------
    int
        The distance between the 2 points in km, rounded to the nearest int.


    """

    # convert degrees to radian

    from_x_radian = _degrees_to_radian(from_x)
    to_x_radian = _degrees_to_radian(to_x)

    from_y_radian = _degrees_to_radian(from_y)
    to_y_radian = _degrees_to_radian(to_y)

    # calculate distance

    q1 = math.cos(to_y_radian - from_y_radian)
    q2 = math.cos(to_x_radian - from_x_radian)
    q3 = math.cos(to_x_radian + from_x_radian)
    return int(
        RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)


def _att(from_x, from_y, to_x, to_y):
    """Calculates a special pseudo-euclidian distance between 2 points in 2D space.

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
        The distance between the 2 points.


    """

    xd = to_x - from_x
    yd = to_y - from_y
    rij = math.sqrt((xd * xd + yd * yd) / 10.0)
    tij = int(round(rij))

    if tij < rij:
        tij += 1

    return tij


def _default_processing(data, dist_func, type=numpy.float_):
    """Creates a dict and calculates the distance matrix for a 2D tsp problem.

    Parameters
    ----------
    data : list of list
        The lists in the list always contain the name of a point,
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

        # ditance between a point and itself is always zero.
        dist_matrix[i][i] = 0

        # get coordinates point
        i_dist_x = data[i][1]
        i_dist_y = data[i][2]

        for j in range(i + 1, size):
            # get coordinates all points
            j_dist_x = data[j][1]
            j_dist_y = data[j][2]

            # calculate distance
            dist_matrix[i][j] = dist_func(
                i_dist_x, i_dist_y, j_dist_x, j_dist_y)
            dist_matrix[j][i] = dist_func(
                i_dist_x, i_dist_y, j_dist_x, j_dist_y)

    return dist_matrix


def _upper_row_processing(data, dimension):
    """Creates a dict and initialises the distance matrix for a 2D tsp problem.

    Parameters
    ----------
    data : list of list
        The lists in the list contain the upper row of the distance matrix
    dimension : int
        The dimension of the distance matrix.
    Returns
    -------
    dist_matrix : numpy.ndarray
        The distance matrix for the problem.

    """

    # make distance matrix
    # all values of matrix are initialised as 0
    dist_matrix = numpy.full((dimension, dimension), 0, dtype=numpy.int_)

    # create iterator to iterate over all ints in list
    iterator = itertools.chain.from_iterable(data)

    # fill the distance matrix
    for i in range(dimension):
        for j in range(i, dimension):

            # skip first diagonal --> will always be 0
            if i != j:
                value = int(next(iterator))

                # if values of the first diagonal are included, skip them.
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
    # all values of matrix are initialised as 0
    dist_matrix = numpy.full((dimension, dimension), 0, dtype=numpy.int_)

    # create iterator to iterate over all ints in list
    iterator = itertools.chain.from_iterable(data)

    # fill the distance matrix
    for i in range(dimension):
        for j in range(i + 1):

            # skip first diagonal --> will always be 0
            if i != j:
                value = int(next(iterator))

                # if values of the first diagonal are included, skip them.
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

    # create iterator to iterate over all ints in list
    iterator = itertools.chain.from_iterable(data)

    # fill matrix
    for i in range(dimension):
        for j in range(dimension):

            value = int(next(iterator))
            dist_matrix[i][j] = int(value)
            dist_matrix[j][i] = int(value)

    return dist_matrix


def read_tsplib(filename):
    """Converts the tsplib file format to useable data structures.

    Currently this function only works for TSP problems. The crystallography
    problems can't be parsed with this function.

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
        name given in the data. This dict can be useful when generating output.
    metadata : list of str
        Contains the metadata of the problem. The last entry will always be
        EOF.

    Examples
    --------
    Read "testfile.tsp" from the map "data" in the current working directory:

    .. code-block:: python

        from lclpy.io.tsplib import read_tsplib
        read_tsplib('data/testfile.tsp')

    """

    # init
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
            dtype = numpy.int_
            dist_func = _euclidian
        elif 'MAN_2D' in type_metadata[1]:
            dtype = numpy.int_
            dist_func = _manhattan
        elif 'CEIL_2D' in type_metadata[1]:
            dtype = numpy.int_
            dist_func = _euclidian_rounded_up
        elif 'GEO' in type_metadata[1]:
            dtype = numpy.int_
            dist_func = _geo
        elif 'ATT' in type_metadata[1]:
            dtype = numpy.int_
            dist_func = _att

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
    # tsplib files start counting from 1, not from 0
    dictionary = {}

    for i in range(dist_matrix.shape[0]):
        dictionary[i] = i + 1

    # return results
    TsplibData = collections.namedtuple(
        'TsplibData', ['distance_matrix', 'dictionary', 'metadata'])
    return TsplibData(dist_matrix, dictionary, metadata)
