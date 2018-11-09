from locsearch.evaluation.abstract_evaluation_function import AbstractEvaluationFunction


class TspEvaluationFunction(AbstractEvaluationFunction):
    """This class contains the methods to evaluate the quality of a tsp-solution


    Parameters
    ----------
    distance_matrix : numpy.ndarray
        The distance matrix of the tsp-problem. The weight from A to B does
        not need to be equal to the weight from B to A.

    Attributes
    ----------
    distance_matrix : numpy.ndarray
        The distance matrix of the tsp-problem.
    size : int
        the amount of points to visit

    Examples
    --------
    A simple example:

    .. doctest::

        >>> import numpy
        >>> from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
        >>> dist_matrix = numpy.array(
        ... [[0, 2, 9, 5],
        ...  [2, 0, 4, 6],
        ...  [9, 4, 0, 3],
        ...  [5, 6, 3, 0]])
        >>> eval_func = TspEvaluationFunction(dist_matrix)
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
        self.distance_matrix = distance_matrix
        self.size = distance_matrix.shape[0]

        if move_function is not None:
            self._changed_distances = move_function.changed_distances
            self._transform_next_index_to_current_index = \
                move_function.transform_next_index_to_current_index
        else:
            self.delta_evaluate = self._not_implemented

    def evaluate(self, order):
        """Calculates an evaluation value for the function

        Parameters
        ----------
        order : numpy.ndarray
            A 1 dimensional array that contains the order of the points to
            visit. All values are unique and are within the interval [0,size[.
        """
        value = 0

        for index in range(self.size - 1):
            value += self.distance_matrix[order[index]][order[index + 1]]

        value += self.distance_matrix[order[-1]][order[0]]

        return value

    def delta_evaluate(self, current_solution, move):
        """Calculates the difference in quality if the move would be performed.

        Note that a move function needs to be passed to the constructor of
        evaluation function for the delta_evaluate to work. The move
        function also needs to have changed_distances and
        transform_next_index_to_current_index properly implemented:

        Parameters
        ----------
        current_solution : numpy.ndarray
            The order that will be compared against.
        move : tuple of int
            Contains the move one wishes to know the effects of.

        Returns
        -------
        int or float
            The difference in quality if the move would be performed.

        Examples
        --------
        A simple example to demonstrate the use of delta_evaluate:

        .. doctest::

            >>> import numpy
            >>> from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
            >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
            >>> dist_matrix = numpy.array(
            ... [[0, 2, 9, 5],
            ...  [2, 0, 4, 6],
            ...  [9, 4, 0, 3],
            ...  [5, 6, 3, 0]])
            >>> move_func = TspArraySwap(4)
            >>> eval_func = TspEvaluationFunction(dist_matrix, move_func)
            >>> order = numpy.array([2, 0, 1, 3])
            >>> eval_func.delta_evaluate(order, (1, 2))
            -6
            >>> eval_func.delta_evaluate(order, (1, 3))
            0
            >>> eval_func.delta_evaluate(order, (2, 3))
            4

        A more elaborate example:

        .. doctest::

            >>> import numpy
            >>> from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
            >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
            >>> dist_matrix = numpy.array(
            ... [[0, 2, 9, 5, 8, 1],
            ...  [2, 0, 4, 6, 1, 2],
            ...  [9, 4, 0, 3, 6, 3],
            ...  [5, 6, 3, 0, 7, 4],
            ...  [8, 1, 6, 7, 0, 5],
            ...  [1, 2, 3, 4, 5, 0]])
            >>> move_func = TspArraySwap(6)
            >>> eval_func = TspEvaluationFunction(dist_matrix, move_func)
            >>> order = numpy.array([0, 5, 2, 1, 3, 4])
            >>> eval_func.delta_evaluate(order, (1, 4))
            -2
            >>> eval_func.delta_evaluate(order, (0, 1))
            3
            >>> eval_func.delta_evaluate(order, (2, 4))
            0


        """
        changed = self._changed_distances(move)

        next_solution_value = 0
        current_solution_value = 0

        for distances in changed:

            frm = distances[0]
            to = distances[1]

            # add difference to current value
            current_solution_value += self.distance_matrix[
                current_solution[frm]][current_solution[to]]

            # add difference to the "next" value

            (frm, to) = \
                self._transform_next_index_to_current_index(frm, to, move)

            next_solution_value += self.distance_matrix[
                current_solution[frm]][current_solution[to]]

        return next_solution_value - current_solution_value

    def _not_implemented(self, *not_used):
        raise NotImplementedError
