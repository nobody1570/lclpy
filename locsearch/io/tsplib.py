import string
import numpy
import math


def _euclidian(from_x, from_y, to_x, to_y):
    return math.sqrt((to_x - from_x)**2 + (to_y - from_y)**2)


def _euclidian_rounded_up(from_x, from_y, to_x, to_y):
    return int(math.ceil(math.sqrt((to_x - from_x)**2 + (to_y - from_y)**2)))


def _manhattan(from_x, from_y, to_x, to_y):
    return abs(to_x - from_x) + abs(to_y - from_y)


def _default_processing(data, dist_func, type=numpy.float_):

    # make dict
    dictionary = {}

    position = 0

    for point in data:
        dictionary[position] = int(point[0])
        position += 1

    # make dist_matrix
    size = len(data)

    # dist_matrix [from] [to]
    dist_matrix = numpy.full((size, size), numpy.inf, dtype=numpy.float_)

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

    return (dist_matrix, dictionary)


def read_tsplib(filename):

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

    return (dist_matrix, dictionary, metadata)
