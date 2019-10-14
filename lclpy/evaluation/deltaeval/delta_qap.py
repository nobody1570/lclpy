from lclpy.aidfunc.error_func import _not_implemented


# base class for the tsp delta evaluation

class QAPDeltaEvaluate():
    """Class to perform delta-evaluation for QAP problems.

    Parameters
    ----------
    eval_func : AbstractEvaluationFunction
        The used evaluation function
    changed_points
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
    changed_locations
        This function returns the locations who would have an altered
        evaluation value due to the move.
    next_to_current
        This function transforms the indices so that they can be used as
        indices in the unaltered array, yet return the value they would have
        had if the move was actually performed and they were used as indices.

    """

    def __init__(self, eval_func, changed_locations, next_to_current):
        self.eval_func = eval_func
        self.changed_locations = changed_locations
        self.next_to_current = next_to_current

    def delta_evaluate(self, current_order, move):
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
        changed = self.changed_locations(move)

        # init values
        next_solution_value = 0
        current_solution_value = 0

        visited = set()

        # calculate the value for all changed locations
        for location in changed:

            visited.add(location)

            next_location = self.next_to_current(location, move)

            for i in range(self.eval_func._size):

                if i not in visited:

                    current_solution_value += \
                        self.eval_func._distance_matrix[location][i] * \
                        self.eval_func._flow_matrix[
                            current_order[location]][current_order[i]]

                    next_i = self.next_to_current(i, move)

                    next_solution_value += \
                        self.eval_func._distance_matrix[location][i] * \
                        self.eval_func._flow_matrix[
                            current_order[next_location]][current_order[next_i]]

        return next_solution_value - current_solution_value


# functions for array_swap

def array_swap_changed_locations(move):
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
    tuple of int
        A tuple containing the locations that would have an altered evaluation
        value due to the move.

    Examples
    --------
    Some simple examples to demonstrate the behaviour:

    .. doctest::

        >>> from lclpy.evaluation.deltaeval.delta_qap \\
        ...     import array_swap_changed_locations \\
        ...         as changed_locations
        ... # tests
        >>> changed_locations((4, 8))
        (4, 8)
        >>> changed_locations((4, 9))
        (4, 9)
        >>> changed_locations((0, 8))
        (0, 8)
        >>> changed_locations((0, 9))
        (0, 9)

    """

    return move


def array_swap_transform_next_index_to_current_index(position, move):
    """Transforms the position depending on the move.

    Works with the array_swap move type.
    This function transforms the position so that it can be used as the indice
    in the unaltered array, yet return the value it would have had if the move
    was actually performed and the position was used as indice.

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
    Some simple examples, the move remains the same, but the position changes:

    .. doctest::

        >>> from lclpy.evaluation.deltaeval.delta_qap \\
        ...     import array_swap_transform_next_index_to_current_index \\
        ...         as transform_next_index_to_current_index
        ... # tests
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

def array_reverse_order_changed_locations(move):
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
    range
        A range containing the locations that would have an altered evaluation
        value due to the move.

    Examples
    --------
    Some simple examples to demonstrate the behaviour:

    .. doctest::

        >>> from lclpy.evaluation.deltaeval.delta_qap \\
        ...     import array_reverse_order_changed_locations \\
        ...         as changed_locations
        ... # tests
        >>> changed_locations((4, 5))
        range(4, 6)
        >>> changed_locations((4, 9))
        range(4, 10)
        >>> changed_locations((0, 8))
        range(0, 9)

    """

    return range(move[0], move[1] + 1)


def array_reverse_order_transform_next_index_to_current_index(position, move):
    """Transforms the position depending on the move.

    Works with the array_swap move type.
    This function transforms the position so that it can be used as the indice
    in the unaltered array, yet return the value it would have had if the move
    was actually performed and the position was used as indice.

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
    Some simple examples, the move remains the same, but the position changes:

    .. doctest::

        >>> from lclpy.evaluation.deltaeval.delta_qap \\
        ...     import array_reverse_order_transform_next_index_to_current_index \\
        ...         as transform_next_index_to_current_index
        ... # tests
        >>> transform_next_index_to_current_index(0, (1, 4))
        0
        >>> transform_next_index_to_current_index(1, (1, 4))
        4
        >>> transform_next_index_to_current_index(2, (1, 4))
        3
        >>> transform_next_index_to_current_index(3, (1, 4))
        2
        >>> transform_next_index_to_current_index(4, (1, 4))
        1
        >>> transform_next_index_to_current_index(5, (1, 4))
        5

    """

    # check if position is altered by the move

    if (position >= move[0]) & (position <= move[1]):

        # alter the position
        offset = position - move[0]
        position = move[1] - offset

    return position


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

    visited = set()

    # calculate the value for all changed locations
    for location in changed:

        visited.add(location)

        next_location = \
            eval_func._transform_next_index_to_current_index(location, move)

        for i in range(eval_func._size):

            if i not in visited:

                current_solution_value += \
                    eval_func._distance_matrix[location][i] * \
                    eval_func._flow_matrix[
                        current_order[location]][current_order[i]]

                next_i = eval_func._transform_next_index_to_current_index(
                    i, move)

                next_solution_value += \
                    eval_func._distance_matrix[location][i] * \
                    eval_func._flow_matrix[
                        current_order[next_location]][current_order[next_i]]

    return next_solution_value - current_solution_value


# The method to return the other stuff

def delta_qap(eval_func, move_func):
    """Returns delta-eval class for a QAP problem.

    Note that if a method for the problem can't be found, that a placeholder
    method will be used. This method will raise a NotImplementedError when
    called.

    Parameters
    ----------
    eval_func : AbstractEvaluationFunction
        The used evaluation function object.
    move_func : AbstractMove
        The used move object.

    Returns
    -------
    QAPDeltaEvaluate
        Class useable for delta evaluation of TSP problems.

    """

    move_type = move_func.get_move_type()

    if move_type is 'array_swap':
        return QAPDeltaEvaluate(eval_func,
                                array_swap_changed_locations,
                                array_swap_transform_next_index_to_current_index)
    if move_type is 'array_reverse_order':
        return QAPDeltaEvaluate(eval_func,
                                array_reverse_order_changed_locations,
                                array_reverse_order_transform_next_index_to_current_index)
    else:
        raise NotImplementedError
