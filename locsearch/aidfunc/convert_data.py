from collections import namedtuple


def convert_data(data):
    """Converts a list made with add_to_data_func to 3 seperate lists.

    This is done to improve the ease of plotting.

    Parameters
    ----------
    data : list of tuple
        A list created with add_to_data_func

    Returns
    -------
    time : list of float
        The timestamps taken.
    value : list of float or list of int
        The values calculated for the current value at the timestamps.
    best_value : list of float or list of int
        The best found value for all timestamps.

    """

    time = []
    value = []
    best_value = []

    time_ref = data[0][0]

    for data_point in data:
        time.append(data_point[0] - time_ref)
        value.append(data_point[1])
        best_value.append(data_point[2])

    Data = namedtuple('Data', ['time', 'value', 'best_value'])

    return Data(time, value, best_value)
