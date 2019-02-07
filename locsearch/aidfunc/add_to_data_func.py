from time import perf_counter


def add_to_data_func(data, current_value, best_value):
    """A function to add the best and the current value to a list with a timestamp.

    Parameters
    ----------
    data : list
        The list one wishes to append the data to.
    current_value : int or float
        The evaluation value of the current solution.
    best_value : int or float
        The best evaluation value found.

    """

    data.append((perf_counter(), current_value, best_value))
