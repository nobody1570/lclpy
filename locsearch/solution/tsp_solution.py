from locsearch.solution.abstract_local_search_solution import AbstractLocalSearchSolution
import numpy


class TspSolution(AbstractLocalSearchSolution):
    """Contains all the data needed to handle a TSP problem.

    Parameters
    ----------
    evaluation_function : AbstractEvaluationFunction
        The evaluation function that needs to be used for the problem
    move_function : AbstractMove
        The move function that needs to be used for the problem
    order : numpy.ndarray, optional
        A 1 dimensional array that contains the order of the points to start
        with. All values are int, unique and are within the interval [0,size[.
        The default value is None. In this case a numpy array will be
        generated. The generated array will always be ordered from small to
        big.

    Attributes
    ----------
    _evaluation_function : AbstractEvaluationFunction
        The evaluation function that is used for the problem
    _move_function : AbstractMove
        The move function that is used for the problem
    _order : numpy.ndarray
        A 1 dimensional array that contains the order of the points. All
        values are int, unique and are within the interval [0,size[.
    best_order : numpy.ndarray
        Contains the order of the best found solution
    best_order_value: int or float
        The evaluation value of the best found solution

    Examples
    --------

    A simple example, note that solution.set_as_best_order does NOT check if
    the value is actually belongs to the order NOR does it check if the value
    is better than the previous best value:

    .. doctest::

        >>> import numpy
        >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
        >>> from locsearch.solution.tsp_solution import TspSolution
        >>> distance_matrix = numpy.array(
        ... [[0, 2, 5, 8],
        ...  [2, 0, 4, 1],
        ...  [5, 4, 0, 7],
        ...  [8, 1, 7, 0]])
        >>> size = distance_matrix.shape[0]
        >>> move_func = TspArraySwap(size)
        >>> evaluation_func = TspEvaluationFunction(distance_matrix)
        >>> solution = TspSolution(evaluation_func, move_func, size)
        >>> solution._order
        array([0, 1, 2, 3])
        >>> value = solution.evaluate()
        >>> value
        21
        >>> solution.set_as_best_order(value)
        >>> solution.best_order
        array([0, 1, 2, 3])
        >>> solution.best_order_value
        21
        >>> solution.move((2,3))
        >>> solution._order
        array([0, 1, 3, 2])
        >>> value = solution.evaluate()
        >>> value
        15
        >>> solution.set_as_best_order(value)
        >>> solution.best_order
        array([0, 1, 3, 2])
        >>> solution.undo_move((2,3))
        >>> solution._order
        array([0, 1, 2, 3])
        >>> solution.best_order
        array([0, 1, 3, 2])

    Initialising with a non-default order:

    .. doctest::

        >>> import numpy
        >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
        >>> from locsearch.solution.tsp_solution import TspSolution
        >>> distance_matrix = numpy.array(
        ... [[0, 2, 5, 8],
        ...  [2, 0, 4, 1],
        ...  [5, 4, 0, 7],
        ...  [8, 1, 7, 0]])
        >>> wanted_order = numpy.array([0, 3, 2, 1])
        >>> size = distance_matrix.shape[0]
        >>> move_func = TspArraySwap(size)
        >>> evaluation_func = TspEvaluationFunction(distance_matrix)
        >>> solution = TspSolution(evaluation_func, move_func, size, wanted_order)
        >>> solution._order
        array([0, 3, 2, 1])

    """

    def __init__(self, evaluation_function, move_function, size, order=None):
        super().__init__()

        # init variables
        self._evaluation_function = evaluation_function
        self._move_function = move_function

        if order is None:
            self._order = numpy.arange(size)
        else:
            self._order = order

    def move(self, move):
        """Performs a move on self._order .

        Parameters
        ----------
        move_number : tuple of int
            Represents a unique valid move.

        """

        self._move_function.move(self._order, move)

    def undo_move(self, move):
        """Undoes a move on self._order .

        Parameters
        ----------
        move_number : tuple of int
            Represents a unique valid move.

        """

        self._move_function.undo_move(self._order, move)

    def get_moves(self):
        """An iterable that returns all valid moves in the neighboorhood.

        Returns
        -------
        tuple of int
            Represents one unique valid move in the neighbourhood.

        Examples
        --------
        Get all moves from the neigbourhood, you should NEVER do this. You
        should evaluate only one move at a time. This example is simply to
        show the behaviour of get_moves.

        .. doctest::

            >>> import numpy
            >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
            >>> from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
            >>> from locsearch.solution.tsp_solution import TspSolution
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            >>> size = distance_matrix.shape[0]
            >>> move_func = TspArraySwap(size)
            >>> evaluation_func = TspEvaluationFunction(distance_matrix)
            >>> solution = TspSolution(evaluation_func, move_func, size)
            >>> all_moves = []
            >>> for move in solution.get_moves():
            ...     all_moves.append(move)
            >>> all_moves
            [(1, 2), (1, 3), (2, 3)]

        """

        return self._move_function.get_moves()

    def get_random_move(self):
        """A function to generate and return a random move from the neighbourhood.

        Returns
        -------
        tuple of int
            Represents one unique valid move in the neighbourhood.

        Examples
        --------
        Get a random valid move:

        .. doctest::

            >>> import numpy
            >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
            >>> from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
            >>> from locsearch.solution.tsp_solution import TspSolution
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            >>> size = distance_matrix.shape[0]
            >>> move_func = TspArraySwap(size)
            >>> evaluation_func = TspEvaluationFunction(distance_matrix)
            >>> solution = TspSolution(evaluation_func, move_func, size)
            >>> move = solution.get_random_move()
            >>> move in [(1, 2), (1, 3), (2, 3)]
            True

        """

        return self._move_function.get_random_move()

    def evaluate_move(self, move):
        """Evaluates the quality gained or lost by a potential move.

        Does not need to be implemented, but can lead to considerable
        speedups. Is equivalent to a delta evaluation between _order and
        _order after the move is performed.

        Parameters
        ----------
        move : tuple of int
            Represents a unique valid move.

        Returns
        -------
        int or float
            The change in value of the eval-function if the move is performed.

        Examples
        --------
        A simple example, note that the move function needs to be passed to
        the evaluation function for the evaluation of moves to work. The move
        function also needs to have changed_distances and
        transform_next_index_to_current_index properly implemented:

        .. doctest::

            >>> import numpy
            >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
            >>> from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
            >>> from locsearch.solution.tsp_solution import TspSolution
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            >>> size = distance_matrix.shape[0]
            >>> move_func = TspArraySwap(size)
            >>> evaluation_func = TspEvaluationFunction(distance_matrix, move_func)
            >>> solution = TspSolution(evaluation_func, move_func, size)
            >>> solution.evaluate_move((1, 2))
            -3
            >>> solution.evaluate_move((1, 3))
            0
            >>> solution.evaluate_move((2, 3))
            -6

        """

        return self._evaluation_function.delta_evaluate(self._order, move)

    def evaluate(self):
        """A function to evaluate the current _order.

        Returns
        -------
        int or float
            The calculated distance between the points.

        """

        return self._evaluation_function.evaluate(self._order)

    def set_as_best_order(self, evaluation_value):
        """Sets the current _order as the new best_order

        Parameters
        ----------
        evaluation_value : int or float
            The evaluation value of the current order. If you haven't kept or
            calculated said value, it can always be calculated with
            evaluate(). The recalculation will take time, however.

        """

        self.best_order = numpy.copy(self._order)
        self.best_order_value = evaluation_value
