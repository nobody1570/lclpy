from numpy import array


def convert_data(data):
    """Converts a list made with add_to_data_func into seperate lists.

    Parameters
    ----------
    data : list of tuple
        A list created with add_to_data_func

    Returns
    -------
    tuple of numpy.ndarray
        All the data in seperate lists. The first list will always be the time
        passed.

    """

    size = len(data[0])

    all_lists = []

    for i in range(size):
        all_lists.append([])

    # convert to lists
    for data_point in data:
        for i in range(size):
            all_lists[i].append(data_point[i])


    # convert timestamps into the time passed
    offset = all_lists[0][0]
    for i in range(len(all_lists[0])):
        all_lists[0][i] -= offset

    # create tuple and convert lists to ndarray

    all_data = ()

    for l in all_lists:
        all_data = all_data + (array(l),)

    return all_data
