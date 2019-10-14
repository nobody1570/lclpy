from lclpy.problem.abstract_local_search_problem \
    import AbstractLocalSearchProblem
import numpy
from lclpy.aidfunc.error_func import not_multi_move_type
from lclpy.aidfunc.error_func import NoNextNeighbourhood

from statistics import mean, StatisticsError


class ArrayProblem(AbstractLocalSearchProblem):
    """Contains all the data needed to handle a problem.

    Parameters
    ----------
    evaluation_function : AbstractEvaluationFunction
        The evaluation function that needs to be used for the problem.
    move_function : AbstractMove
        The move function that needs to be used for the problem.
    order : numpy.ndarray or list, optional
        A one dimensional array that contains the order of the points to start
        with. All values are int, unique and are within the interval
        [0,size[.
        The default value is None.
        In the default case a numpy array will be generated. The generated
        array's values will always be ordered from small to big.

    Attributes
    ----------
    _evaluation_function : AbstractEvaluationFunction.
        The evaluation function that is used for the problem
    _move_function : AbstractMove
        The move function that is used for the problem.
    _order : numpy.ndarray
        A 1 dimensional array that contains the current order of the points.
        All values are int, unique and are within the interval [0,size[.
    _starting_order : numpy.ndarray
        The initial value of _order.
    best_order : numpy.ndarray
        Contains the order of the best found problem.
    best_order_value: int or float
        The evaluation value of the best found problem.

    Examples
    --------

    A simple example, demonstrates the use of move, undo_move, evaluate and
    set_as_best. Note that problem.set_as_best_order does NOT check if the
    value actually belongs to the order NOR does it check if the value is
    better than the previous best value:

    .. doctest::

        >>> import numpy
        >>> from lclpy.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from lclpy.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from lclpy.problem.array_problem import ArrayProblem
        ... # init distance matrix
        >>> distance_matrix = numpy.array(
        ... [[0, 2, 5, 8],
        ...  [2, 0, 4, 1],
        ...  [5, 4, 0, 7],
        ...  [8, 1, 7, 0]])
        ... # init move function
        >>> size = distance_matrix.shape[0]
        >>> move_func = TspArraySwap(size)
        ... # init evaluation function
        >>> evaluation_func = TspEvaluationFunction(distance_matrix)
        ... # init problem
        >>> problem = ArrayProblem(evaluation_func, move_func, size)
        ... # default generated order
        >>> problem._order
        array([0, 1, 2, 3])
        >>> # evaluating the current order
        >>> value = problem.evaluate()
        >>> value
        21
        >>> # saving the current order as the best order.
        >>> problem.set_as_best(value)
        ... # get the best order and it's value
        >>> problem.best_order
        array([0, 1, 2, 3])
        >>> problem.best_order_value
        21
        >>> # perform a move and evaluate the new order
        >>> problem.move((2,3))
        >>> problem._order
        array([0, 1, 3, 2])
        >>> value = problem.evaluate()
        >>> value
        15
        >>> # saving the current order as the best order
        >>> problem.set_as_best(value)
        >>> problem.best_order
        array([0, 1, 3, 2])
        >>> problem.best_order_value
        15
        >>> # undoing move and rechecking value.
        >>> # Note that best_order and best_order_value don't change.
        >>> problem.undo_move((2,3))
        >>> problem._order
        array([0, 1, 2, 3])
        >>> problem.best_order
        array([0, 1, 3, 2])
        >>> problem.best_order_value
        15

    Initialising with a non-default order:

    .. doctest::

        >>> import numpy
        >>> from lclpy.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from lclpy.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from lclpy.problem.array_problem import ArrayProblem
        ... # init distance matrix
        >>> distance_matrix = numpy.array(
        ... [[0, 2, 5, 8],
        ...  [2, 0, 4, 1],
        ...  [5, 4, 0, 7],
        ...  [8, 1, 7, 0]])
        ... # wanted order is the order we want.
        >>> wanted_order = numpy.array([0, 3, 2, 1])
        ... # init move function
        >>> size = distance_matrix.shape[0]
        >>> move_func = TspArraySwap(size)
        ... # init evaluation function
        >>> evaluation_func = TspEvaluationFunction(distance_matrix)
        ... # init problem
        >>> problem = ArrayProblem(
        ...     evaluation_func, move_func, size, wanted_order)
        ... # the order of the problem
        >>> problem._order
        array([0, 3, 2, 1])

    """

    def __init__(self, evaluation_function, move_function, size, order=None):
        super().__init__()

        # init variables
        self._evaluation_function = evaluation_function
        self._move_function = move_function

        if self._move_function.get_move_type() is not 'multi_neighbourhood':
            self.first_neighbourhood = not_multi_move_type
            self.next_neighbourhood = not_multi_move_type
            self.previous_neighbourhood = not_multi_move_type
            self.select_get_moves = not_multi_move_type
            self.select_random_move = not_multi_move_type
        else:
            self.current_neighbourhood = 0
            self.neighbourhood_size = move_function.size()

        if order is None:
            self._order = numpy.arange(size)
        else:
            self._order = numpy.array(order)

        self._starting_order = numpy.array(self._order)

    def move(self, move):
        """Performs a move on _order.

        Parameters
        ----------
        move_number : tuple of int
            Represents a unique valid move.

        """

        self._move_function.move(self._order, move)

    def undo_move(self, move):
        """Undoes a move on _order .

        Parameters
        ----------
        move_number : tuple of int
            Represents a unique valid move.

        """

        self._move_function.undo_move(self._order, move)

    def get_moves(self):
        """An iterable that returns all valid moves in the complete neighbourhood.

        Yields
        -------
        tuple of int
            The next move in the neighbourhood.

        Examples
        --------
        Gets all moves from the neigbourhood, you should NEVER do this. You
        should evaluate only one move at a time. This example is simply to
        show the behaviour of get_moves.

        .. doctest::

            >>> import numpy
            >>> from lclpy.localsearch.move.tsp_array_swap \\
            ...     import TspArraySwap
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.problem.array_problem import ArrayProblem
            ... # init distance matrix
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            ... # init move function
            >>> size = distance_matrix.shape[0]
            >>> move_func = TspArraySwap(size)
            ... # init evaluation function
            >>> evaluation_func = TspEvaluationFunction(distance_matrix)
            ... # init problem
            >>> problem = ArrayProblem(evaluation_func, move_func, size)
            ... # retrieve all moves with get_moves
            >>> all_moves = []
            >>> for move in problem.get_moves():
            ...     all_moves.append(move)
            >>> all_moves
            [(1, 2), (1, 3), (2, 3)]

        """

        return self._move_function.get_moves()

    def get_random_move(self):
        """A function to return a random move from the complete neighbourhood.

        Returns
        -------
        tuple of int
            Represents one unique valid move in the neighbourhood.

        Examples
        --------
        Get a random valid move:

        .. doctest::

            >>> import numpy
            >>> from lclpy.localsearch.move.tsp_array_swap \\
            ...     import TspArraySwap
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.problem.array_problem import ArrayProblem
            ... # init distance matrix
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            ... # init move function
            >>> size = distance_matrix.shape[0]
            >>> move_func = TspArraySwap(size)
            ... # init evaluation function
            >>> evaluation_func = TspEvaluationFunction(distance_matrix)
            ... # init problem
            >>> problem = ArrayProblem(evaluation_func, move_func, size)
            ... # get a random move and check if it's in the neighboorhood.
            >>> move = problem.get_random_move()
            >>> move in [(1, 2), (1, 3), (2, 3)]
            True

        """

        return self._move_function.get_random_move()

    def evaluate_move(self, move):
        """Evaluates the quality gained or lost by a potential move.

        Can lead to considerable speedups. Is equivalent to a delta evaluation
        between _order and _order after the move is performed. Note that
        delta-evaluation needs to be implemented for the evaluation function
        and the move type for this method to work.

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
        A simple example:

        .. doctest::

            >>> import numpy
            >>> from lclpy.localsearch.move.tsp_array_swap \\
            ...     import TspArraySwap
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.problem.array_problem import ArrayProblem
            ... # init distance matrix
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            ... # init move function
            >>> size = distance_matrix.shape[0]
            >>> move_func = TspArraySwap(size)
            ... # init evaluation function
            >>> evaluation_func = TspEvaluationFunction(distance_matrix,
            ...                                         move_func)
            ... # init problem
            >>> problem = ArrayProblem(evaluation_func, move_func, size)
            ... # tests
            >>> problem.evaluate_move((1, 2))
            -3
            >>> problem.evaluate_move((1, 3))
            0
            >>> problem.evaluate_move((2, 3))
            -6

        """

        return self._evaluation_function.delta_evaluate(self._order, move)

    def evaluate(self):
        """A function to evaluate the current _order.

        Returns
        -------
        int or float
            An evaluation of the current state of _order.

        """

        return self._evaluation_function.evaluate(self._order)

    def set_as_best(self, evaluation_value):
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

    def state(self):
        """Returns an immutable hashable object that describes the current state.

        Returns
        -------
        tuple
            A hashable object associated with the current state.

        Examples
        --------
        A simple example:

        .. doctest::

            >>> import numpy
            >>> from lclpy.localsearch.move.tsp_array_swap \\
            ...     import TspArraySwap
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.problem.array_problem import ArrayProblem
            ... # init distance matrix
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            ... # init move function
            >>> size = distance_matrix.shape[0]
            >>> move_func = TspArraySwap(size)
            ... # init evaluation function
            >>> evaluation_func = TspEvaluationFunction(distance_matrix,
            ...                                         move_func)
            ... # init problem
            >>> problem = ArrayProblem(evaluation_func, move_func, size)
            >>> problem.state()
            (0, 1, 2, 3)
            >>> problem.move((1, 3))
            >>> problem.state()
            (0, 3, 2, 1)

        """

        return tuple(self._order)

    def first_neighbourhood(self):
        """Changes the current neighbourhood to the first neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.

        Raises
        ------
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

        """

        self.current_neighbourhood = 0

    def next_neighbourhood(self):
        """Changes the current neighbourhood to the next neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.
        If this function is called when the last neighbourhood is the current
        neighbourhood, the last neighbourhood will remain the current
        neighbourhood and an exception will be raised.

        Raises
        ------
        NoNextNeighbourhood
            If there is no next neighbourhood. This is simply an indication
            that the current neighbourhood was the last neighbourhood.
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

        """

        self.current_neighbourhood += 1

        if self.current_neighbourhood is self.neighbourhood_size:
            self.current_neighbourhood -= 1
            raise NoNextNeighbourhood('There is no next neighbourhood.')

    def previous_neighbourhood(self):
        """Changes the current neighbourhood to the previous neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.
        If this function is called when the first neighbourhood is the current
        neighbourhood, the first neighbourhood will remain the current
        neighbourhood.

        Raises
        ------
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

        """

        if self.current_neighbourhood is not 0:
            self.current_neighbourhood -= 1

    def select_get_moves(self):
        """Function to get all moves from the current neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.

        Returns
        -------
        generator
            An iterable generator object that contains all the moves of the
            current neighbourhood.

        Raises
        ------
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

        """

        return self._move_function.select_get_moves(self.current_neighbourhood)

    def select_random_move(self):
        """A method used to generate a random move from the current neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.

        Returns
        -------
        tuple of int
            A random valid move from the current neighbourhood.

        Raises
        ------
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

        """

        return self._move_function.select_random_move(
            self.current_neighbourhood)

    def reset(self):
        """Resets the object back to it's state after init.

        _order is replaced by a copy of _starting_order.

        Examples
        --------
        A simple example with the default order:

        .. doctest::

            >>> import numpy
            >>> from lclpy.localsearch.move.tsp_array_swap \\
            ...     import TspArraySwap
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.problem.array_problem import ArrayProblem
            ... # init distance matrix
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            ... # init move function
            >>> size = distance_matrix.shape[0]
            >>> move_func = TspArraySwap(size)
            ... # init evaluation function
            >>> evaluation_func = TspEvaluationFunction(distance_matrix,
            ...                                         move_func)
            ... # init problem
            >>> problem = ArrayProblem(evaluation_func, move_func, size)
            ... # tests
            >>> problem.state()
            (0, 1, 2, 3)
            >>> problem.move((1, 3))
            >>> problem.state()
            (0, 3, 2, 1)
            >>> problem.reset()
            >>> problem.state()
            (0, 1, 2, 3)
            >>> problem.move((1, 3))
            >>> problem.state()
            (0, 3, 2, 1)
            >>> problem.reset()
            >>> problem.state()
            (0, 1, 2, 3)

        An example with a non-default order:

        .. doctest::

            >>> import numpy
            >>> from lclpy.localsearch.move.tsp_array_swap \\
            ...     import TspArraySwap
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.problem.array_problem import ArrayProblem
            ... # init distance matrix
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            ... # init move function
            >>> size = distance_matrix.shape[0]
            >>> move_func = TspArraySwap(size)
            ... # init evaluation function
            >>> evaluation_func = TspEvaluationFunction(distance_matrix,
            ...                                         move_func)
            ... # init problem
            >>> problem = ArrayProblem(evaluation_func, move_func,
            ...                          size, [0, 1, 3, 2])
            ... # tests
            >>> problem.state()
            (0, 1, 3, 2)
            >>> problem.move((1, 3))
            >>> problem.state()
            (0, 2, 3, 1)
            >>> problem.reset()
            >>> problem.state()
            (0, 1, 3, 2)
            >>> problem.move((1, 3))
            >>> problem.state()
            (0, 2, 3, 1)
            >>> problem.reset()
            >>> problem.state()
            (0, 1, 3, 2)

        """

        self._order = numpy.array(self._starting_order)
