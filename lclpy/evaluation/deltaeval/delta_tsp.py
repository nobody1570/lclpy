from lclpy.aidfunc.error_func import _not_implemented


# base class for the tsp delta evaluation

class TSPDeltaEvaluate():
    """Class to perform delta-evaluation for TSP problems.

    Parameters
    ----------
    eval_func : AbstractEvaluationFunction
        The used evaluation function
    changed_distances
        This function returns the pairs who would have an altered evaluation
        value due to the move.
    next_to_current
        This function transforms the indices so that they can be used as
        indices in the unaltered array, yet return the value they would have
        had if the move was actually performed and they were used as indices.

    Attributes
    ----------
    eval_func : AbstractEvaluationFunction
        The used evaluation function
    changed_distances
        This function returns the pairs who would have an altered evaluation
        value due to the move.
    next_to_current
        This function transforms the indices so that they can be used as
        indices in the unaltered array, yet return the value they would have
        had if the move was actually performed and they were used as indices.

    Returns
    -------
    int or float
        The difference in quality if the move would be performed.

    """

    def __init__(self, eval_func, changed_distances, next_to_current):
        self.eval_func = eval_func
        self.changed_distances = changed_distances
        self.next_to_current = next_to_current

    def delta_evaluate(self, current_order, move):
        """Calculates the difference in quality if the move would be performed.

        Parameters
        ----------
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
        # these are represented as a set of tuples of 2 ints that represent
        # the 2 unique indices between which the distance is changed.
        changed = self.changed_distances(self.eval_func._size, move)

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
            current_solution_value += self.eval_func._distance_matrix[
                current_order[frm]][current_order[to]]

            # add distance to the "next" value

            # transform the indices so the indices return the value if the
            # move was performed
            (frm, to) = self.next_to_current(frm, to, move)

            next_solution_value += self.eval_func._distance_matrix[
                current_order[frm]][current_order[to]]

        return next_solution_value - current_solution_value


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

        >>> from lclpy.evaluation.deltaeval.delta_tsp \\
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

    changed_dist = set()

    # iterating over the 2 swapped indices
    for order_index in move:

        # get the change in the lower indices
        if order_index != 0:
            changed_dist.add((order_index - 1, order_index))
        else:

            # between index 0 and index _size-1, the pair is
            # (_size - 1, 0), this because we move from _size-1 to 0
            changed_dist.add((size - 1, 0))

        # get the change in the higher indices
        if order_index != size - 1:
            changed_dist.add((order_index, order_index + 1))
        else:
            changed_dist.add((size - 1, 0))

    return changed_dist


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
        The from index that one wants to use in the array if the move was
        performed.
    to : int
        The to index that one wants to use in the array if the move was
        performed.
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

        >>> from lclpy.evaluation.deltaeval.delta_tsp \\
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

    # transform frm so it returns the value that from would have if the
    # move was performed.
    if frm == move[0]:
        frm = move[1]
    elif frm == move[1]:
        frm = move[0]

    # transform to so it returns the value that from would have if the
    # move was performed.
    if to == move[0]:
        to = move[1]
    elif to == move[1]:
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

        >>> from lclpy.evaluation.deltaeval.delta_tsp import \\
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

    changed_dist = set()

    # Calculating the distances that are always changed

    if (move[0] == 0):
        changed_dist.add((size - 1, 0))
    else:
        changed_dist.add((move[0] - 1, move[0]))

    if (move[1] == size - 1):
        changed_dist.add((size - 1, 0))
    else:
        changed_dist.add((move[1], move[1] + 1))

    # calculating the distances that are only changed if X -> Y causes a
    # different evaluation value than Y -> X

    for i in range(move[0], move[1]):

        changed_dist.add((i, i + 1))

    return changed_dist


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
        The from index that one wants to use in the array if the move was
        performed.
    to : int
        The to index that one wants to use in the array if the move was
        performed.
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

        >>> from lclpy.evaluation.deltaeval.delta_tsp import \\
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
    if (frm >= move[0]) & (frm <= move[1]):

        # alter the value as necessary
        offset = frm - move[0]
        frm = move[1] - offset

    # check if the to value is affected by the move
    if (to >= move[0]) & (to <= move[1]):

        # alter the value as necessary
        offset = to - move[0]
        to = move[1] - offset

    return (frm, to)


# The method to return the other stuff.

def delta_tsp(eval_func, move_func):
    """Returns delta-eval class for a TSP problem.

    Note that if no methods for the problem can be found, that a placeholder
    method will be used. The placeholder methods will raise a
    NotImplementedError when called.

    Parameters
    ----------
    eval_func : AbstractEvaluationFunction
        The used evaluation function object.
    move_func : AbstractMove
        The used move object.

    Returns
    -------
    TSPDeltaEvaluate
        Class useable for delta evaluation of TSP problems.

    """

    move_type = move_func.get_move_type()

    if move_type is 'array_swap':
        return TSPDeltaEvaluate(eval_func, array_swap_changed_distances,
                                array_swap_transform_next_index_to_current_index)
    if move_type is 'array_reverse_order':
        return TSPDeltaEvaluate(eval_func,
                                array_reverse_order_changed_distances,
                                array_reverse_order_transform_next_index_to_current_index)
    else:
        raise NotImplementedError
