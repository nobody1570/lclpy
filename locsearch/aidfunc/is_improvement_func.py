

def bigger(old_value, value):
    """Checks if a value is an improvement. Bigger values are improvements.

    Parameters
    ----------
    old_value : int or float
        The old value.
    value : int or float
        The new value that is checked.

    Returns
    -------
    bool
        Returns true if the new value is bigger than the old value, else
        returns false.


    """

    return value > old_value


def smaller(old_value, value):
    """Checks if a value is an improvement. Smaller values are improvements.

    Parameters
    ----------
    old_value : int or float
        The old value.
    value : int or float
        The new value that is checked.

    Returns
    -------
    bool
        Returns true if the new value is smaller than the old value, else
        returns false.

    """

    return value < old_value


def bigger_or_equal(old_value, value):
    """Checks if a value is an improvement. Bigger values are improvements.

    Parameters
    ----------
    old_value : int or float
        The old value.
    value : int or float
        The new value that is checked.

    Returns
    -------
    bool
        Returns true if the new value is bigger or equal to the old value, else
        returns false.


    """

    return value >= old_value


def smaller_or_equal(old_value, value):
    """Checks if a value is an improvement. Smaller values are improvements.

    Parameters
    ----------
    old_value : int or float
        The old value.
    value : int or float
        The new value that is checked.

    Returns
    -------
    bool
        Returns true if the new value is smaller or equal to the old value,
        else returns false.

    """

    return value <= old_value
