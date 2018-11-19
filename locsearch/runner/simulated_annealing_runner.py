from locsearch.runner.abstract_runner import AbstractRunner
from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
from locsearch.localsearch.simulatedannealing.simulated_annealing \
    import SimulatedAnnealing
from locsearch.localsearch.simulatedannealing.geometric_cooling_function \
    import GeometricCoolingFunction
from locsearch.localsearch.simulatedannealing.cnst_iterations_temp_function \
    import CnstIterationsTempFunction
from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
from locsearch.termination.max_seconds_termination_criterion \
    import MaxSecondsTerminationCriterion
from locsearch.io.tsplib import read_tsplib
from locsearch.solution.tsp_solution import TspSolution


# TODO adapt to inherit from AbstractRunner
class SimulatedAnnealingRunner():
    """docstring for SimulatedAnnealingRunner"""

    def __init__(self):
        super().__init__()

    def run(self):

        self._data = read_tsplib('data/bayg29.tsp')
        self._distance_matrix = self._data.distance_matrix
        self._size = self._distance_matrix.shape[0]

        self._move_function = TspArraySwap(self._size)

        self._evaluation_function = TspEvaluationFunction(
            self._distance_matrix, self._move_function)

        self._solution = TspSolution(
            self._evaluation_function, self._move_function, self._size)

        # create termination criterion
        # shared with other algorithms
        termination_criterion = MaxSecondsTerminationCriterion(10)

        # create cooling func

        cooling_func = GeometricCoolingFunction()

        # create iterations for temp func

        i_for_temp = CnstIterationsTempFunction()

        # calculate

        self._algorithm = SimulatedAnnealing(
            self._solution, termination_criterion, cooling_func, i_for_temp)

        self.results = self._algorithm.run()

        print(self.results)
