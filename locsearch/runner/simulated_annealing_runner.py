from locsearch.runner.abstract_runner import AbstractRunner
from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
from locsearch.localsearch.simulatedannealing.simulated_annealing \
    import SimulatedAnnealing
from locsearch.localsearch.simulatedannealing.geometric_cooling_function \
    import GeometricCoolingFunction
from locsearch.localsearch.simulatedannealing.cnst_iterations_temp_function \
    import CnstIterationsTempFunction
from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
from locsearch.termination.min_temperature_termination_criterion \
    import MinTemperatureTerminationCriterion
from locsearch.io.tsplib import read_tsplib
from locsearch.solution.tsp_solution import TspSolution


# TODO adapt to inherit from AbstractRunner
class SimulatedAnnealingRunner():
    """Loads a problem and performs simulated annealing on the problem.

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
    _termination_criterion : AbstractTerminationCriterion
        The termination criterion for the algorithm.
    _cooling_func : AbstractCoolingFunction
        The cooling function for the algorithm.
    _i_for_temp : AbstrIterationsTempFunction
        The amount of iterations for temperature function for the algorithm.
    _algorithm : SteepestDescent
        The steepest descent algorithm used.
    results
        The results from the localsearch.

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

    def define_termination_criterion(self):
        """Creating and initialising a termination criterion"""

        self._termination_criterion = MinTemperatureTerminationCriterion()

    def define_cooling_function(self):
        """Creating and initialising a cooling function"""

        self._cooling_func = GeometricCoolingFunction()

    def define_iteration_temp_f(self):
        """Create and init an amount of iterations for temperature function."""

        self._i_for_temp = CnstIterationsTempFunction()

    def define_algorithm(self):
        """Creating and initialising a steepest descent algorithm."""

        self._algorithm = SimulatedAnnealing(
            self._solution, self._termination_criterion,
            self._cooling_func, self._i_for_temp)

    def run_algorithm(self):
        """Starts running the algorithm."""

        return self._algorithm.run()

    def output(self):
        """Handles the output."""

        print(self.results)

    def run(self, path):
        """initializes and runs an instance of the SteepestDescent class.

        Parameters
        ----------
        path : str
            The relative or absolute path to the file.

        """

        print('Starting runner...')
        # read data
        self.read(path)
        print('--- data read')

        # create move

        self.define_move_function()
        print('--- move function defined')

        # create evaluation function

        self.define_evaluation_function()
        print('--- evaluation function defined')

        # create and initialize solution

        self.define_solution()
        print('--- solution object defined')

        # create and init termination criterion

        self.define_termination_criterion()
        print('--- termination criterion defined')

        # create and init cooling function

        self.define_cooling_function()
        print('--- cooling function defined')

        # create and init an amount of iterations for temperature function.

        self.define_iteration_temp_f()
        print('--- iterations for temperature function defined')

        # create instance of localsearch algorithm and set solution

        self.define_algorithm()
        print('--- algorithm defined')
        # get results from localsearch algorithm

        print('--- start running...')
        self.results = self.run_algorithm()
        print('--- ...running ended')

        # output
        self.output()
        print('--- output generated')
        print('... runner stopped')
