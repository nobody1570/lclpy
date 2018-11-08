from locsearch.runner.abstract_runner import AbstractRunner
from locsearch.localsearch.steepestdescent.steepest_descent import SteepestDescent
from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
from locsearch.io.tsplib import read_tsplib
from locsearch.solution.tsp_solution import TspSolution


class SteepestDescentRunner(AbstractRunner):
    """Loads a tsp problem, etc.

    """

    def __init__(self):
        super().__init__()

    def run(self):
        """initializes and runs an instance of the SteepestDescent class

        """

        # read data
        data = read_tsplib('data/a280.tsp')

        distance_matrix = data.distance_matrix

        size = distance_matrix.shape[0]

        # create move

        move = TspArraySwap(size)

        # create evaluation function

        evaluation = TspEvaluationFunction(distance_matrix)

        # create and initialize solution

        solution = TspSolution(evaluation, move, size)

        # create instance of localsearch algorithm and set solution

        steepest_descent = SteepestDescent(solution)

        # get results from localsearch algorithm

        results = steepest_descent.run()

        # output

        print(results)

