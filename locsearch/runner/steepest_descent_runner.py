from locsearch.runner.abstract_runner import AbstractRunner
from locsearch.localsearch.steepestdescent.steepest_descent \
    import SteepestDescent
from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
from locsearch.io.tsplib import read_tsplib
from locsearch.solution.tsp_solution import TspSolution


class SteepestDescentRunner(AbstractRunner):
    """Loads a problem and performs a steepestdescent on said problem.

    Note that the default implementation only works with tsp problems from
    tsplib.

    Attributes
    ---------
    _data
        The data read from a file.
    _distance_matrix : numpy.ndarray
        The distance matrix for the problem.
    _size : int
        The amount of points in the tsp problem.
    _move_function : AbstractMove
        The move function that needs to be used.
    _evaluation_function : AbstractEvaluationFunction
        The evaluation function used for the problem.
    _solution : AbstractLocalSearchSolution
        The solution object for the problem.
    _algorithm : SteepestDescent
        The steepest descent algorithm used.
    results
        The results from the localsearch.

    Examples
    --------
    Default running:

    .. code-block:: python

        from locsearch.runner.steepest_descent_runner import SteepestDescentRunner
        runner = SteepestDescentRunner()
        runner.run()


    """

    def __init__(self):
        super().__init__()

    def read(self, path):
        """Reads a file.

        Parameters
        ----------
        path : str
            The relative or absolute path to the file.

        """

        self._data = read_tsplib(path)
        self._distance_matrix = self._data.distance_matrix
        self._size = self._distance_matrix.shape[0]

    def define_move_function(self):
        """Creating and initialising a move function."""

        self._move_function = TspArraySwap(self._size)

    def define_evaluation_function(self):
        """Creating and initialising an evaluation function."""

        self._evaluation_function = TspEvaluationFunction(
            self._distance_matrix, self._move_function)

    def define_solution(self):
        """Creating and initialising the solution object."""

        self._solution = TspSolution(
            self._evaluation_function, self._move_function, self._size)

    def define_algorithm(self):
        """Creating and initialising a steepest descent algorithm."""

        self._algorithm = SteepestDescent(self._solution)

    def run_algorithm(self):
        """Starts running the algorithm."""

        return self._algorithm.run()

    def output(self):
        """Handles the output."""

        print(self.results)
