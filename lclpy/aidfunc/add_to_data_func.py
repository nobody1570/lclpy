from time import perf_counter


def add_to_data_func(data, *args):
    """A function to add values to a list with a timestamp.

    The data will be kept into a tuple and added to the list.
    Note that a timestamp is always added as the first item in the tuple. This
    timestamp, however has no fixed epoch. So only differences in time have a
    real meaning.

    Parameters
    ----------
    data : list
        The list one wishes to append the data to.
    *args
        The data one wishes to append to data.

    """

    data.append((perf_counter(),) + args)
