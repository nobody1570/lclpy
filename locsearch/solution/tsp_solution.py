from locsearch.solution.abstract_local_search_solution import AbstractLocalSearchSolution
import numpy
import math


class TspSolution(AbstractLocalSearchSolution):
    """Contains all the data needed to handle a TSP problem.

    Parameters
    ----------
    evaluation_function : AbstractEvaluationFunction
        The evaluation function that needs to be used for the problem
    move_function : AbstractMove
        The move function that needs to be used for the problem
    neighbourhood_size : int
        The size of the neighbourhood.
    order : numpy.ndarray, optional
        A 1 dimensional array that contains the order of the points to start
        with. All values are unique and are within the interval [0,size[. The
        default value is None. In this case a numpy array will be generated.
        The generated array will always be ordered from small to big.

    Attributes
    ----------
    evaluation_function : AbstractEvaluationFunction
        The evaluation function that needs to be used for the problem
    move_function : AbstractMove
        The move function that needs to be used for the problem
    neighbourhood_size : int
        The size of the neighbourhood.
    order : numpy.ndarray, optional
        A 1 dimensional array that contains the order of the points to start
        with. All values are unique and are within the interval [0,size[.
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
        >>> solution.order
        array([0, 1, 2, 3])
        >>> value = solution.evaluate()
        >>> value
        21
        >>> solution.set_as_best_order(value)
        >>> solution.best_order
        array([0, 1, 2, 3])
        >>> solution.best_order_value
        21
        >>> solution.neighbourhood_size
        3
        >>> solution.move(2)
        >>> solution.order
        array([0, 1, 3, 2])
        >>> value = solution.evaluate()
        >>> value
        15
        >>> solution.set_as_best_order(value)
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
        >>> solution.order
        array([0, 3, 2, 1])

    """

    def __init__(self, evaluation_function, move_function, size, order=None):
        super().__init__()

        # init variables
        self.evaluation_function = evaluation_function
        self.move_function = move_function
        self.neighbourhood_size = move_function.neighbourhood_size

        if order is None:
            self.order = numpy.arange(size)
        else:
            self.order = order

    def move(self, move_number):
        """Performs a move on self.order .

        Parameters
        ----------
        move_number : int
            Should be in the interval [0,neighbourhood_size[. Is used to
            choose a move.

        """

        self.move_function.move(self.order, move_number)

    def undo_move(self, move_number):
        """Undoes a move on self.order .

        Parameters
        ----------
        move_number : int
            Undoes the move that is called with the same move_number. Only use
            this function after you have called the corresponding
            move(move_number).

        """

        self.move_function.move(self.order, move_number)

    def evaluate(self):
        """A function to evaluate the current order.

        Returns
        -------
        int or float
            The calculated distance between the points.

        """

        return self.evaluation_function.evaluate(self.order)

    def set_as_best_order(self, evaluation_value):
        """Sets the current order as the new best_order

        Parameters
        ----------
        evaluation_value : int or float
            The evaluation value of the current order. If you haven't kept or
            calculated said value, it can always be calculated with
            evaluate(). The recalculation will take time, however.

        """

        self.best_order = numpy.copy(self.order)
        self.best_order_value = evaluation_value
