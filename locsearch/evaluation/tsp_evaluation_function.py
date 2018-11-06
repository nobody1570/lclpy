from locsearch.evaluation.abstract_evaluation_function import AbstractEvaluationFunction


class TspEvaluationFunction(AbstractEvaluationFunction):
    """This class contains the methods to evaluate the quality of a tsp-solution

    Parameters
    ----------
    distance_matrix : numpy.ndarray
        The distance matrix of the tsp-problem. The weight from A to B does
        not need to be equal to the weight from B to A.

    Atributes
    ---------
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

    def __init__(self, distance_matrix):
        super().__init__()
        self.distance_matrix = distance_matrix
        self.size = distance_matrix.shape[0]

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

    def delta_evaluate(self, other_solution, current_solution):
        # TODO: depends heavily on the move-type, might be better in the move
        # class.
        raise NotImplementedError
