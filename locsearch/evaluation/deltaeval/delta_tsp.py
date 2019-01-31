from locsearch.aidfunc.error_func import _not_implemented


# functions for array_swap

def array_swap_changed_distances(size, move):
    """Aid function for delta evaluation.

    Works with the array_swap move type.
    This function returns the pairs who would have an altered evaluation
    value due to the move.

    Parameters
    ----------
    size : int
        The size of the array.
    move : tuple of int
        A tuple of 2 ints that represents a single unique move.

    Returns
    -------
    set of tuple
        this set contains a tuple with every (from,to) pair that would have
        an altered evaluation value due to the move.

    Examples
    --------
    Some simple examples to demonstrate the behaviour:

    .. doctest::

        >>> from locsearch.evaluation.deltaeval.delta_tsp \\
        ...     import array_swap_changed_distances \\
        ...         as changed_distances
        ... # init
        >>> size = 10
        ... # tests
        ... # since the order of the items in a set might be different,
        ... # they are compared to an equivalent set.
        >>> changed = changed_distances(size, (4, 8))
        >>> changed == {(3, 4), (4, 5), (7, 8), (8,9)}
        True
        >>> changed = changed_distances(size, (4, 9))
        >>> changed == {(3, 4), (4, 5), (8, 9), (9, 0)}
        True
        >>> changed = changed_distances(size, (0, 8))
        >>> changed == {(9, 0), (0, 1), (7, 8), (8, 9)}
        True
        >>> changed = changed_distances(size, (0, 9))
        >>> changed == {(0, 1), (8, 9), (9, 0)}
        True

    """

    changed_dist = []

    # iterating over the 2 swapped indices
    for order_index in move:

        # get the change in the lower indices
        if order_index != 0:
            changed_dist.append((order_index - 1, order_index))
        else:

            # between index 0 and index _size-1, the pair is
            # (_size - 1, 0), this because we move from _size-1 to 0
            changed_dist.append((size - 1, 0))

        # get the change in the higher indices
        if order_index != size - 1:
            changed_dist.append((order_index, order_index + 1))
        else:
            changed_dist.append((size - 1, 0))

    return set(changed_dist)


def array_swap_transform_next_index_to_current_index(frm, to, move):
    """Transforms frm and to depending on a move

    Works with the array_swap move type.
    This function transforms the indices frm and to so that they can
    be used as indices in the unaltered array, yet return the value
    they would have had if the move was actually performed and they
    were used as indices.

    Parameters
    ----------
    frm : int
        the from index that one wants to use in the array with if the
        move was performed.
    to : int
        the to index that one wants to use in the array with if the
        move was performed.
    move : tuple of int
        A tuple with that represents a single, unique move.

    Returns
    -------
    frm : int
        The index in the unaltered array that has the same value as the
        parameter frm in an array where the move was performed.
    to : int
        The index in the unaltered array that has the same value as the
        parameter to in an array where the move was performed.

    Examples
    --------
    Some simple examples, the indices remain the same, but the move
    changes:

    .. doctest::

        >>> from locsearch.evaluation.deltaeval.delta_tsp \\
        ...     import array_swap_transform_next_index_to_current_index \\
        ...         as transform_next_index_to_current_index
        >>> transform_next_index_to_current_index(1, 5, (1, 5))
        (5, 1)
        >>> transform_next_index_to_current_index(1, 5, (1, 3))
        (3, 5)
        >>> transform_next_index_to_current_index(1, 5, (0, 5))
        (1, 0)
        >>> transform_next_index_to_current_index(1, 5, (2, 3))
        (1, 5)


    """

    # check if the frm value is affected by the move
    if frm in move:

        # transform frm so it returns the value that from would have if the
        # move was performed.
        if frm == move[0]:
            frm = move[1]
        else:
            frm = move[0]

    # check if the to value is affected by the move
    if to in move:
        # transform to so it returns the value that from would have if the
        # move was performed.
        if to == move[0]:
            to = move[1]
        else:
            to = move[0]

    return (frm, to)


# functions for array_reverse_order

def array_reverse_order_changed_distances(size, move):
    """Aid function for delta evaluation.

    Works with the array_reverse_order move type.
    This function returns the pairs who would have an altered evaluation
    value due to the move.

    Parameters
    ----------
    size : int
        The size of the array.
    move : tuple of int
        A tuple of 2 ints that represents a single valid move.

    Returns
    -------
    set of tuple
        this set contains a tuple with every (from,to) pair that would have
        an altered evaluation value due to the move.
        A pair (x, y) and a pair (y, x) are assumed to have different
        evaluation values.

    Examples
    --------
    Some simple examples to demonstrate the behaviour:

    .. doctest::

        >>> from locsearch.evaluation.deltaeval.delta_tsp import \\
        ...     array_reverse_order_changed_distances as \\
        ...         changed_distances
        ... # init
        >>> size = 10
        ... # tests
        ... # since the order of the items in a set might be different,
        ... # they are compared to an equivalent set.
        >>> changed = changed_distances(size, (4, 8))
        >>> changed == {(3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)}
        True
        >>> changed = changed_distances(size, (4, 9))
        >>> changed == {(3, 4), (4, 5), (5, 6),
        ...             (6, 7), (7, 8), (8, 9), (9, 0)}
        True
        >>> changed = changed_distances(size, (0, 4))
        >>> changed == {(9, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5)}
        True
        >>> changed = changed_distances(size, (0, 9))
        >>> changed == {(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
        ...             (5, 6), (6, 7), (7, 8), (8, 9), (9, 0)}
        True

    """

    changed_dist = []

    # Calculating the distances that are always changed

    if (move[0] == 0):
        changed_dist.append((size - 1, 0))
    else:
        changed_dist.append((move[0] - 1, move[0]))

    if (move[1] == size - 1):
        changed_dist.append((size - 1, 0))
    else:
        changed_dist.append((move[1], move[1] + 1))

    # calculating the distance that are only changed if X -> Y causes a
    # different evaluation value than Y -> X

    for i in range(move[0], move[1]):

        changed_dist.append((i, i + 1))

    return set(changed_dist)


def array_reverse_order_transform_next_index_to_current_index(frm, to, move):
    """Transforms frm and to depending on a move

    Works with the array_reverse_order move type.
    This function transforms the indices frm and to so that they can
    be used as indices in the unaltered array, yet return the value
    they would have had if the move was actually performed and they
    were used as indices.

    Parameters
    ----------
    frm : int
        the from index that one wants to use in the array with if the
        move was performed.
    to : int
        the to index that one wants to use in the array with if the
        move was performed.
    move : tuple of int
        A tuple with that represents a single, unique move.

    Returns
    -------
    frm : int
        The index in the unaltered array that has the same value as the
        parameter frm in an array where the move was performed.
    to : int
        The index in the unaltered array that has the same value as the
        parameter to in an array where the move was performed.

    Examples
    --------
    Some simple examples, the move remains the same, but the indices
    change:

    .. doctest::

        >>> from locsearch.evaluation.deltaeval.delta_tsp import \\
        ...     array_reverse_order_transform_next_index_to_current_index \\
        ...         as transform_next_index_to_current_index
        >>> transform_next_index_to_current_index(0, 10, (1, 8))
        (0, 10)
        >>> transform_next_index_to_current_index(0, 6, (1, 8))
        (0, 3)
        >>> transform_next_index_to_current_index(2, 3, (1, 8))
        (7, 6)
        >>> transform_next_index_to_current_index(1, 8, (1, 8))
        (8, 1)
        >>> transform_next_index_to_current_index(5, 10, (1, 8))
        (4, 10)


    """

    # check if the frm value is affected by the move
    if frm in range(move[0], move[1] + 1):

        # alter the value as necessary
        offset = frm - move[0]
        frm = move[1] - offset

    # check if the to value is affected by the move
    if to in range(move[0], move[1] + 1):

        # alter the value as necessary
        offset = to - move[0]
        to = move[1] - offset

    return (frm, to)


# shared delta_evaluate function for TSP problems

def delta_evaluate(eval_func, current_order, move):
    """Calculates the difference in quality if the move would be performed.

    Note that a move function needs to be passed to the constructor of
    evaluation function for the delta_evaluate to work. The move
    function also needs to have changed_distances and
    transform_next_index_to_current_index properly implemented:

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

    # get the changed distances
    # these are represented as a list of tuples of 2 ints that represent
    # the 2 unique indices between which the distance is changed.
    changed = eval_func._changed_distances(eval_func._size, move)

    # init values
    next_solution_value = 0
    current_solution_value = 0

    # for all changed distances:
    # - add the original value to current_solution_value
    # - add the "changed" value to next_solution_value
    for distances in changed:

        # get indices
        frm = distances[0]
        to = distances[1]

        # add distance to current value
        current_solution_value += eval_func._distance_matrix[
            current_order[frm]][current_order[to]]

        # add distance to the "next" value

        # transform the indices so the indices return the value if the
        # move was performed
        (frm, to) = \
            eval_func._transform_next_index_to_current_index(frm, to, move)

        next_solution_value += eval_func._distance_matrix[
            current_order[frm]][current_order[to]]

    return next_solution_value - current_solution_value


# The method to return the other methods.

def delta_tsp(move_type):
    """Returns delta-eval-aid methods for a problem using ArraySwap move class.

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
