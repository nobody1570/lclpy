import csv
import numpy
import collections


def read_csv(filename, dtype="int"):
    """Converts the csv file format to useable data structures.

    Note that the csv file should only contain the distance matrixes.
    Different matrixes should be seperated with an empty line. A maximum of 2
    distance matrixes can be read.

    Parameters
    ----------
    filename : str
        absolute or relative path to the file that contains the data.
    datatype : str, optional
        Determines the data type of the returned matrix(es).
        At the time, 2 datatypes are supported "float" and "int".
        The default float and int are respectively used if one of this
        parameter is used. The default is "int".

    Returns
    -------
    distance_matrix : numpy.ndarray
        The distance matrix for the problem.

    Examples
    --------
    Read "testfile.csv" from the map "data" in the current working directory:

    .. code-block:: python

        from lspy.io.csv_io import read_csv
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
