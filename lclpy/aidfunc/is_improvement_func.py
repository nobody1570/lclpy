"""This module contains functions to check if a value is an improvement."""


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

    Examples
    --------
    Some simple tests:

    .. doctest::

        >>> from lclpy.aidfunc.is_improvement_func import bigger
        >>> bigger(2, 5)
        True
        >>> bigger(5, 2)
        False
        >>> bigger(3,3)
        False

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

    Examples
    --------
    Some simple tests:

    .. doctest::

        >>> from lclpy.aidfunc.is_improvement_func import smaller
        >>> smaller(2, 5)
        False
        >>> smaller(5, 2)
        True
        >>> smaller(3,3)
        False

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

    Examples
    --------
    Some simple tests:

    .. doctest::

        >>> from lclpy.aidfunc.is_improvement_func import bigger_or_equal
        >>> bigger_or_equal(2, 5)
        True
        >>> bigger_or_equal(5, 2)
        False
        >>> bigger_or_equal(3,3)
        True

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

    Examples
    --------
    Some simple tests:

    .. doctest::

        >>> from lclpy.aidfunc.is_improvement_func import smaller_or_equal
        >>> smaller_or_equal(2, 5)
        False
        >>> smaller_or_equal(5, 2)
        True
        >>> smaller_or_equal(3,3)
        True

    """

    return value <= old_value
