import numpy
from collections import namedtuple


def read_qaplib(filename):
    """Converts the qaplib file format to useable data structures.

    This function can be used to convert files in the qaplib format to useable
    data structures.

    Parameters
    ----------
    filename : str
        absolute or relative path to the file that contains the data.

    Returns
    -------
    distance_matrix : numpy.ndarray
        The distance matrix for the problem.
    flow_matrix : numpy.ndarray
        The flow matrix for the problem.
    dictionary : {int : int}
        A dictionary that can convert a position the distance matrix to the
        name given in the data. This dict can be useful when generating output.

    Examples
    --------
    Read "testfile.tsp" from the map "data" in the current working directory:

    .. code-block:: python

        from lclpy.io.qaplib import read_qaplib
        read_tsplib('data/testfile.tsp')

    """

    data = []
    # read the data
    with open(filename) as f:
        for line in f:
            splitted = line.split()

            if len(splitted) > 0:

                for i in splitted:
                    data.append(int(i))

    # create iterator

    size = data[0]

    # remove size from matrix
    data = data[1:]

    # create the 2 matrixes

    half = int(len(data) / 2)
    matrix_1 = numpy.array(data[:half], dtype=numpy.int_)
    matrix_1 = matrix_1.reshape(size, size)

    matrix_2 = numpy.array(data[half:], dtype=numpy.int_)
    matrix_2 = matrix_2.reshape(size, size)

    # check if matrix_1 has the least zeroes
    # if this is the case, we assume it's the distance matrix
    # if this isn't the case, we assume matrix_2 is the distance matrix
    if numpy.count_nonzero(matrix_1) < numpy.count_nonzero(matrix_2):
        matrix_1, matrix_2 = matrix_2, matrix_1

    # generate dictionary (we start counting from 0, not 1)
    dictionary = {}

    for i in range(size):
        dictionary[i] = i + 1

    TsplibData = namedtuple(
        'TsplibData', ['distance_matrix', 'flow_matrix', 'dictionary'])
    return TsplibData(matrix_1, matrix_2, dictionary)
