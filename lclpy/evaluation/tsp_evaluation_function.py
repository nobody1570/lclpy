from lclpy.evaluation.abstract_evaluation_function \
    import AbstractEvaluationFunction
from lclpy.evaluation.deltaeval.delta_eval_func import delta_eval_func


class TspEvaluationFunction(AbstractEvaluationFunction):
    """A class to evaluate TSP problems.

    This class contains the methods to evaluate the quality of a solution for a
    travelling salesman problem (TSP). The distance matrix is allowed to be
    asymmetric.

    Parameters
    ----------
    distance_matrix : numpy.ndarray
        The distance matrix of the tsp-problem. The weight from A to B does
        not need to be equal to the weight from B to A.
    move_function : AbstractMove, optional
        Only needs to be passed if one wishes to use delta evaluation.

    Attributes
    ----------
    _distance_matrix : numpy.ndarray
        The distance matrix of the tsp-problem.
    _size : int
        the amount of points to visit, is derived from the distance matrix.

    Examples
    --------
    A simple example:

    .. doctest::

        >>> import numpy
        >>> from lclpy.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        ... # init
        >>> dist_matrix = numpy.array(
        ... [[0, 2, 9, 5],
        ...  [2, 0, 4, 6],
        ...  [9, 4, 0, 3],
        ...  [5, 6, 3, 0]])
        >>> eval_func = TspEvaluationFunction(dist_matrix)
        ... # tests
        >>> order = numpy.array([0, 1, 2, 3])
        >>> eval_func.evaluate(order)
        14
        >>> order = numpy.array([0, 3, 1, 2])
        >>> eval_func.evaluate(order)
        24
        >>> order = numpy.array([2, 0, 1, 3])
        >>> eval_func.evaluate(order)
        20


    """

    def __init__(self, distance_matrix, move_function=None):
        super().__init__()
        self._distance_matrix = distance_matrix
        self._size = distance_matrix.shape[0]

        if move_function is not None:
            self._delta_evaluate_object = delta_eval_func(self, move_function)
            self.delta_evaluate = self._delta_evaluate_object.delta_evaluate

    def get_problem_type(self):
        """Returns the problem type.

        Returns
        -------
        str
            The problem type.

        """

        return 'TSP'

    def evaluate(self, order):
        """Calculates an evaluation value for the function.

        Parameters
        ----------
        order : numpy.ndarray
            A 1 dimensional array that contains the order of the points to
            visit. All values are unique and are within the interval [0,size[.

        Returns
        -------
        int, float
            An indication of the quality of the solution, the lower this
            value, the better the quality.
        """

        # init value
        value = 0

        # add all distances to value
        for index in range(self._size - 1):
            value += self._distance_matrix[order[index]][order[index + 1]]

        value += self._distance_matrix[order[-1]][order[0]]

        return value

    def delta_evaluate(self, current_order, move):
        """Calculates the difference in quality if the move would be performed.

        Note that a move function needs to be passed to the constructor of
        evaluation function for the delta_evaluate to work. The move
        function also needs to have changed_distances and
        transform_next_index_to_current_index properly implemented:

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

        Raises
        ------
        NotImplementedError
            If no move_function was given in the constructor.

        Examples
        --------
        A simple example to demonstrate the working of delta_evaluate.
        Note that other move types than array_swap can be used:

        .. doctest::

            >>> import numpy
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.localsearch.move.tsp_array_swap \\
            ...     import TspArraySwap
            ... # init distance matrix
            >>> dist_matrix = numpy.array(
            ... [[0, 2, 9, 5],
            ...  [2, 0, 4, 6],
            ...  [9, 4, 0, 3],
            ...  [5, 6, 3, 0]])
            ... # init move function
            >>> move_func = TspArraySwap(4)
            ... # init evaluation function
            >>> eval_func = TspEvaluationFunction(dist_matrix, move_func)
            ... # init of the order
            >>> order = numpy.array([2, 0, 1, 3])
            ... # tests
            >>> eval_func.delta_evaluate(order, (1, 2))
            -6
            >>> eval_func.delta_evaluate(order, (1, 3))
            0
            >>> eval_func.delta_evaluate(order, (2, 3))
            4

        A more elaborate example:

        .. doctest::

            >>> import numpy
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.localsearch.move.array_swap \\
            ...     import ArraySwap
            ... # init distance matrix
            >>> dist_matrix = numpy.array(
            ... [[0, 2, 9, 5, 8, 1],
            ...  [2, 0, 4, 6, 1, 2],
            ...  [9, 4, 0, 3, 6, 3],
            ...  [5, 6, 3, 0, 7, 4],
            ...  [8, 1, 6, 7, 0, 5],
            ...  [1, 2, 3, 4, 5, 0]])
            ... # init move function
            >>> move_func = TspArraySwap(6)
            ... # init evaluation function
            >>> eval_func = TspEvaluationFunction(dist_matrix, move_func)
            ... # init of the order
            >>> order = numpy.array([0, 5, 2, 1, 3, 4])
            ... # tests
            >>> eval_func.delta_evaluate(order, (1, 4))
            -2
            >>> eval_func.delta_evaluate(order, (0, 1))
            3
            >>> eval_func.delta_evaluate(order, (2, 4))
            0


        """

        raise NotImplementedError
