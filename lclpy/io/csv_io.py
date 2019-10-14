import csv
import numpy
import collections
import os


def read_csv(filename, dtype="int"):
    """Converts the csv file format to useable data structures.

    Note that the csv file should only contain the cost matrixes.
    Different matrixes should be seperated with an empty line. A maximum of 2
    distance matrixes can be read.

    Parameters
    ----------
    filename : str
        Absolute or relative path to the file that contains the data.
    datatype : str, optional
        Determines the data type of the returned matrix(es).
        At the time, 2 datatypes are supported "float" and "int".
        The default float and int are respectively used if one of this
        parameter is used. The default is "int".

    Returns
    -------
    matrix_1 : numpy.ndarray
        A matrix for the problem.
    matrix_2 : numpy.ndarray
        A matrix for the problem, note that this matriw won't always be
        returned.

    Examples
    --------
    Read "testfile.csv" from the map "data" in the current directory:

    .. code-block:: python

        from lclpy.io.csv_io import read_csv
        read_csv('data/testfile.csv')

    """

    if dtype is "int":
        datatype = numpy.int_
    elif dtype is "float":
        datatype = numpy.float_

    matrix_1 = []
    matrix_2 = []

    current_matrix = matrix_1

    with open(filename, newline='') as file:

        spamreader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)

        for row in spamreader:

            if len(row) == 0:
                current_matrix = matrix_2
                continue

            current_matrix.append(row)

    if len(matrix_2) == 0:
        CsvData = collections.namedtuple('CsvData', ['matrix_1'])
        return CsvData(numpy.array(matrix_1, dtype=datatype))

    else:
        CsvData = collections.namedtuple('CsvData', ['matrix_1', 'matrix_2'])
        return CsvData(numpy.array(matrix_1, dtype=datatype),
                       numpy.array(matrix_2, dtype=datatype))


def write_csv(result, filename):
    """Writes the result of an algorithm to a csv file.

    Parameters
    ----------
    result : collections.namedtuple
        The result from a localsearch algorithm
    filename : str
        Absolute or relative path to the file that one wishes to write too.
        It doesn't need to exist.

    """

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(("best state", ))
        writer.writerow(result[0])
        writer.writerow(tuple())

        writer.writerow(("best value", ))
        writer.writerow((result[1], ))
        writer.writerow(tuple())

        if result[2] is not None:

            writer.writerow(("data", ))
            data_size = len(result[2]._fields)
            size = len(result[2][0])
            writer.writerow(result[2]._fields)

            for i in range(size):

                data_row = []

                for j in range(data_size):
                    data_row.append(result[2][j][i])

                writer.writerow(data_row)


def write_benchmark_csv(benchmark_result, pathname,
                        algorithm_names=None, problem_names=None):
    """Writes the result of a benchmark to several csv files in a single map.

    Note that the name of the map can be chosen, but the csv files will always
    be named as follows: \n
    "alg\_" + algorithm_name + "_problem_" + problem_name + _run_ + run +
    ".csv" \n
    The runs always start from 0.

    Parameters
    ----------
    result : list of list of list of collections.namedtuple
        The result from a benchmark.
    pathname : str
        Absolute or relative path to the map that one wishes to write too.
        It doesn't need to exist.
    algorithm_names : list of str or tuple of str, optional
        Must be the same length as the algorithm list given to the original
        benchmark. The indices of a name corresponds with the indices of the
        algorithms given to the original benchmark.
    problem_names : list of str or tuple of str, optional
        Must be the same length as the problem list given to the original
        benchmark. The indices of a name corresponds with the indices of the
        problems given to the original benchmark.

    """

    if algorithm_names is None:
        algorithm_names = tuple(range(len(benchmark_result)))

    if problem_names is None:
        problem_names = tuple(range(len(benchmark_result[0])))

    os.makedirs(pathname, exist_ok=True)

    for i in range(len(benchmark_result)):
        for j in range(len(benchmark_result[0])):
            for k in range(len(benchmark_result[0][0])):

                filename = 'alg_' + str(algorithm_names[i]) + \
                    '_problem_' + \
                    str(problem_names[j]) + '_run_' + str(k) + '.csv'

                path = os.path.join(pathname, filename)

                write_csv(benchmark_result[i][j][k], path)
