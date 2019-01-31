from locsearch.aidfunc.error_func import _not_implemented


# functions for array_swap

def array_swap_changed_distances(move):
    """Aid function for delta evaluation.

    Works with the array_swap move type.
    This function returns the locations who would have an altered evaluation
    value due to the move.

    Parameters
    ----------
    move : tuple of int
        A tuple of 2 ints that represents a single unique move.

    Returns
    -------
    set of int
        this set contains the locations that would have an altered evaluation
        value due to the move.

    Examples
    --------
    Some simple examples to demonstrate the behaviour:

    .. doctest::

        >>> from locsearch.evaluation.deltaeval.delta_qap \\
        ...     import array_swap_changed_distances \\
        ...         as changed_distances
        ... # init
        >>> size = 10
        ... # tests
        ... # since the order of the items in a set might be different,
        ... # they are compared to an equivalent set.
        >>> changed_distances((4, 8))
        [4, 8]
        >>> changed_distances((4, 9))
        [4, 9]
        >>> changed_distances((0, 8))
        [0, 8]
        >>> changed_distances((0, 9))
        [0, 9]

    """

    changed_dist = []

    changed_dist.append(move[0])
    changed_dist.append(move[1])

    return changed_dist


def array_swap_transform_next_index_to_current_index(position, move):
    """Transforms frm and to depending on a move

    Works with the array_swap move type.
    This function transforms the indices frm and to so that they can
    be used as indices in the unaltered array, yet return the value
    they would have had if the move was actually performed and they
    were used as indices.

    Parameters
    ----------
    position : int
        The index that one wants to use in the array if the move was performed.
    move : tuple of int
        A tuple with that represents a single, unique move.

    Returns
    -------
    int
        The index in the unaltered array that has the same value as the
        location in an array where the move was performed.

    Examples
    --------
    Some simple examples, the indices remain the same, but the move
    changes:

    .. doctest::

        >>> from locsearch.evaluation.deltaeval.delta_qap \\
        ...     import array_swap_transform_next_index_to_current_index \\
        ...         as transform_next_index_to_current_index
        >>> transform_next_index_to_current_index(0, (1, 3))
        0
        >>> transform_next_index_to_current_index(1, (1, 3))
        3
        >>> transform_next_index_to_current_index(2, (1, 3))
        2
        >>> transform_next_index_to_current_index(3, (1, 3))
        1
        >>> transform_next_index_to_current_index(4, (1, 3))
        4

    """

    # transform frm so it returns the value that from would have if the
    # move was performed.
    if position == move[0]:
        position = move[1]
    elif position == move[1]:
        position = move[0]

    return position


# functions for array_reverse_order


# shared delta_evaluate function for TSP problems

def delta_evaluate(eval_func, current_order, move):
    """Calculates the difference in quality if the move would be performed.

    Parameters
    ----------
    eval_func : AbstractEvaluationFunction
        The object the delta-evaluation is calculated for.
    current_order : numpy.ndarray
        A 1 dimensional array that contains the order of the points to
        visit. All values are unique and are within the interval [0,size[.
        This is the current order.
    move : tuple of int
        Contains the move one wishes to know the effects on the quality of.

    Returns
    -------
    int or float
        The difference in quality if the move would be performed.

    """

    # get the changed locations
    # these are represented as a set of ints
    changed = eval_func._changed_distances(move)

    # init values
    next_solution_value = 0
    current_solution_value = 0

    # calculate the value for all changed locations
    for location in changed:

        next_location = \
            eval_func._transform_next_index_to_current_index(location, move)

        for i in range(eval_func._size):
            current_solution_value += \
                eval_func._distance_matrix[location][i] * \
                eval_func._flow_matrix[
                    current_order[location]][current_order[i]]

            next_i = eval_func._transform_next_index_to_current_index(i, move)

            next_solution_value += \
                eval_func._distance_matrix[location][i] * \
                eval_func._flow_matrix[
                    current_order[next_location]][current_order[next_i]]

    return next_solution_value - current_solution_value


# The method to return the other methods

def delta_qap(move_type):
    """Returns delta-eval-aid methods for a QAP problem.

    Note that if no methods for the problem can be found, that a placeholder
    method will be used. This method will raise a NotImplementedError when
    called.

    Parameters
    ----------
    problem_type : str
        The name of the problem type.

    Returns
    -------
    delta_evaluate
        A function that can be used for the delta evaluation
    changed_distances
        Aid function to determine what should be recalculated.
    transform_next_index_to_current_index
        Aid function to determine the values that need to be used in the delta
        evaluation.
    """
    if move_type is 'array_swap':
        return (delta_evaluate, array_swap_changed_distances,
                array_swap_transform_next_index_to_current_index)
    if move_type is 'array_reverse_order':
        return (delta_evaluate, array_reverse_order_changed_distances,
                array_reverse_order_transform_next_index_to_current_index)
    else:
        return (delta_evaluate, _not_implemented, _not_implemented)
