from lclpy.evaluation.abstract_evaluation_function \
    import AbstractEvaluationFunction
from lclpy.evaluation.deltaeval.delta_eval_func import delta_eval_func


class QuadraticAssignmentEvaluationFunction(AbstractEvaluationFunction):
    """A class to evaluate QAP problems.

    This class contains the methods to evaluate the quality of a solution for a
    quadratic assignment problem (QAP). In the implementation, it was assumed
    that both the distance and the flow matrix are symmetric.

    Parameters
    ----------
    distance_matrix : numpy.ndarray
        The distance matrix of the problem. Should be symmetric.
    flow_matrix : numpy.ndarray
        The flow matrix for the problem. Should be symmetric.
    move_function : AbstractMove, optional
        Only needs to be passed if one wishes to use delta evaluation.

    Attributes
    ----------
    _distance_matrix : numpy.ndarray
        The distance matrix of the problem.
    _flow_matrix : numpy.ndarray
        The flow matrix of the problem.
    _size : int
        The amount of locations, derived from the distance matrix.

    Examples
    --------
    A simple example:

    .. doctest::

        >>> import numpy
        >>> from lclpy.evaluation.quadratic_assignment_evaluation_function \\
        ...     import QuadraticAssignmentEvaluationFunction
        ... # init distance matrix
        >>> dist_matrix = numpy.array(
        ... [[0, 2, 9, 5],
        ...  [2, 0, 4, 6],
        ...  [9, 4, 0, 3],
        ...  [5, 6, 3, 0]])
        ... # init flow matrix
        >>> flow_matrix = numpy.array(
        ... [[0, 2, 0, 0],
        ...  [2, 0, 4, 0],
        ...  [0, 4, 0, 8],
        ...  [0, 0, 8, 0]])
        ... # init evaluation function
        >>> eval_func = QuadraticAssignmentEvaluationFunction(dist_matrix,
        ...                                                   flow_matrix)
        ... # tests
        >>> order = numpy.array([0, 1, 2, 3])
        >>> eval_func.evaluate(order)
        44
        >>> order = numpy.array([0, 3, 1, 2])
        >>> eval_func.evaluate(order)
        78
        >>> order = numpy.array([2, 1, 0, 3])
        >>> eval_func.evaluate(order)
        56

    """

    def __init__(self, distance_matrix, flow_matrix, move_function=None):
        super().__init__()

        self._size = distance_matrix.shape[0]
        self._distance_matrix = distance_matrix
        self._flow_matrix = flow_matrix

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

        return 'QAP'

    def evaluate(self, order):
        """Calculates an evaluation value for the function.

        Parameters
        ----------
        order : numpy.ndarray
            A 1 dimensional array that maps facilities on locations. The
            index respresents a location, the corresponding value represents
            a facility.

        Returns
        -------
        int or float
            an indication of the quality of current_data

        """

        value = 0

        # all distances need to be checked once
        for i in range(self._size):
            for j in range(i + 1, self._size):
                value += self._distance_matrix[i][j] * \
                    self._flow_matrix[order[i]][order[j]]

        return value

    def delta_evaluate(self, current_order, move):
        """Evaluates the difference in quality between two solutions.

        The two compared solutions are the current solution and the solution
        if the move was performed. The move is not actually performed.

        This function does not need to be implemented. One should only
        consider to implement and use it if a delta evaluation is faster than
        the regular evaluate function or if it needs to be implemented to work
        with existing code.

        Parameters
        ----------
        current_order : numpy.ndarray
            A 1 dimensional array that maps facilities on locations. The
            index respresents a location, the corresponding value represents
            a facility.

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
            >>> from lclpy.evaluation.quadratic_assignment_evaluation_function \\
            ...     import QuadraticAssignmentEvaluationFunction
            >>> from lclpy.localsearch.move.array_swap \\
            ...     import ArraySwap
            ... # init distance matrix
            >>> dist_matrix = numpy.array(
            ... [[ 0, 22, 53, 53],
            ...  [22,  0, 40, 62],
            ...  [53, 40,  0, 55],
            ...  [53, 62, 55,  0]])
            ... # init flow matrix
            >>> flow_matrix = numpy.array(
            ... [[0, 3, 0, 2],
            ...  [3, 0, 0, 1],
            ...  [0, 0, 0, 4],
            ...  [2, 1, 4, 0]])
            ... # init move function
            >>> move_func = ArraySwap(4)
            ... # init evaluation function
            >>> eval_func = QuadraticAssignmentEvaluationFunction(
            ...     dist_matrix, flow_matrix, move_func)
            ... # tests
            >>> order = numpy.array([0, 1, 2, 3])
            >>> eval_func.delta_evaluate(order, (0, 1))
            9
            >>> eval_func.delta_evaluate(order, (0, 2))
            50
            >>> eval_func.delta_evaluate(order, (0, 3))
            72
            >>> eval_func.delta_evaluate(order, (1, 2))
            114
            >>> eval_func.delta_evaluate(order, (2, 3))
            -22

        """

        raise NotImplementedError
