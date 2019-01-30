from locsearch.evaluation.abstract_evaluation_function \
    import AbstractEvaluationFunction
from locsearch.aidfunc.error_func import _not_implemented


class QuadraticAssignmentEvaluationFunction(AbstractEvaluationFunction):
    """Template to create evaluation functions.

    This class contains the methods to evaluate the quality of a solution for a
    quadratic assignment problem (QAP). In the implementation, it was assumed
    that both the distance and the flow matrix are symmetric.

    Parameters
    ----------
    distance_matrix : numpy.ndarray
        The distance matrix of the problem. Should be symmetric.
    flow_matrix : numpy.ndarray
        The flow matrix for the problem. Should ne symmetric.

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
        >>> from locsearch.evaluation.quadratic_assignment_evaluation_function \\
        ...     import QuadraticAssignmentEvaluationFunction
        ... # init matrixes
        >>> dist_matrix = numpy.array(
        ... [[0, 2, 9, 5],
        ...  [2, 0, 4, 6],
        ...  [9, 4, 0, 3],
        ...  [5, 6, 3, 0]])
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

        # add functions from move_function
        if move_function is not None:
            self._changed_distances = move_function.changed_distances
            self._transform_next_index_to_current_index = \
                move_function.transform_next_index_to_current_index
        else:
            self.delta_evaluate = _not_implemented

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

        # all distances need to be checked
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

        """
        raise NotImplementedError
