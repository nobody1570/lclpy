from locsearch.localsearch.abstract_local_search import AbstractLocalSearch

from locsearch.aidfunc.is_improvement_func import bigger, smaller
from locsearch.aidfunc.pass_func import pass_func
from locsearch.aidfunc.add_to_data_func import add_to_data_func
from locsearch.aidfunc.convert_data import convert_data

from collections import namedtuple


class VariableNeighbourhood(AbstractLocalSearch):
    """Performs a steepest descent algorithm on the given solution.

    Parameters
    ----------
    solution : AbstractLocalSearchSolution
        Contains all the data needed for the specific problem. This solution
        must have been initialed a move_function class of the type
        MultiNeighbourhood. This MultiNeighbourhood needs to contain multiple
        move function classes.
    minimise : bool, optional
        If the goal is to minimise the evaluation function, this  should be
        True. If the goal is to maximise the evlauation function, this should
        be False. The default is True.
    termination_criterion : AbstractTerminationCriterion, optional
        The termination criterion that is used.
    benchmarking : bool, optional
        Should be True if one wishes benchmarks to be kept, should be False if
        one wishes no benchmarks to be made. Default is True.

    Attributes
    ----------
    _solution : AbstractLocalSearchSolution
        Contains all the data needed for the specific problem.
    _termination_criterion : AbstractTerminationCriterion
        Ends the algorithm if no more improvements can be found.
    _function
        The function used to determine if a delta value is better than another
        delta value.
    _best_found_delta_base_value : float
        Initialisation value for the delta value of each iteration. It's
        infinite when minimising or minus infinite when maximising.
    data : list of tuple
        Data useable for benchmarking will be None if no benchmarks are made.
    _data_append
        Function to append new data-points to data. Will do nothing if no
        benchmarks are made.

    Examples
    --------
    An example of minimising:

    .. doctest::

        >>> import numpy
        >>> from locsearch.localsearch.vns.variable_neighbourhood \\
        ...     import VariableNeighbourhood
        >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from locsearch.localsearch.move.array_reverse_order \\
        ...     import ArrayReverseOrder
        >>> from locsearch.localsearch.move.multi_neighbourhood \\
        ...     import MultiNeighbourhood
        >>> from locsearch.localsearch.vns.variable_neighbourhood \\
        ...     import VariableNeighbourhood
        >>> from locsearch.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from locsearch.solution.array_solution import ArraySolution
        >>> from locsearch.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        ... # init distance matrix
        >>> distance_matrix = numpy.array(
        ... [[0, 2, 5, 8],
        ...  [2, 0, 4, 1],
        ...  [5, 4, 0, 7],
        ...  [8, 1, 7, 0]])
        ... # init MultiNeighbourhood
        >>> size = distance_matrix.shape[0]
        >>> move_1 = TspArraySwap(size)
        >>> move_2 = ArrayReverseOrder(size)
        >>> move = MultiNeighbourhood([move_1, move_2])
        >>> evaluation = TspEvaluationFunction(distance_matrix, move)
        >>> solution = ArraySolution(evaluation, move, size)
        ... # init termination criterion
        >>> termination = MaxSecondsTerminationCriterion(2)
        ... # init VariableNeighbourhood
        >>> algorithm = VariableNeighbourhood(solution, termination,
        ...                                   benchmarking=False)
        ... # run algorithm
        >>> algorithm.run()
        Results(best_order=array([0, 1, 3, 2]), best_value=15, data=None)

    An example of maximising, note that the distance matrix is different:

    .. doctest::

        >>> import numpy
        >>> from locsearch.localsearch.vns.variable_neighbourhood \\
        ...     import VariableNeighbourhood
        >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from locsearch.localsearch.move.array_reverse_order \\
        ...     import ArrayReverseOrder
        >>> from locsearch.localsearch.move.multi_neighbourhood \\
        ...     import MultiNeighbourhood
        >>> from locsearch.localsearch.vns.variable_neighbourhood \\
        ...     import VariableNeighbourhood
        >>> from locsearch.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from locsearch.solution.array_solution import ArraySolution
        >>> from locsearch.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        ... # init distance matrix
        >>> distance_matrix = numpy.array(
        ... [[0, 8, 5, 2],
        ...  [8, 0, 4, 7],
        ...  [5, 4, 0, 1],
        ...  [2, 7, 1, 0]])
        ... # init MultiNeighbourhood
        >>> size = distance_matrix.shape[0]
        >>> move_1 = TspArraySwap(size)
        >>> move_2 = ArrayReverseOrder(size)
        >>> move = MultiNeighbourhood([move_1, move_2])
        >>> evaluation = TspEvaluationFunction(distance_matrix, move)
        >>> solution = ArraySolution(evaluation, move, size)
        ... # init termination criterion
        >>> termination = MaxSecondsTerminationCriterion(2)
        ... # init SteepestDescent
        ... # init VariableNeighbourhood
        >>> algorithm = VariableNeighbourhood(solution, termination, False,
        ...                                   benchmarking=False)
        ... # run algorithm
        >>> algorithm.run()
        Results(best_order=array([0, 1, 3, 2]), best_value=21, data=None)



    """

    def __init__(self, solution, termination_criterion, minimise=True,
                 benchmarking=True):

        super().__init__()

        self._solution = solution

        self._termination_criterion = termination_criterion

        if minimise:
            self._function = smaller
            self._best_found_delta_base_value = float("inf")
        else:
            self._function = bigger
            self._best_found_delta_base_value = float("-inf")

        if benchmarking:
            self.data = []
            self._data_append = add_to_data_func
        else:
            self.data = None
            self._data_append = pass_func

    def run(self):
        """Starts running the variable neighbourhood search.

        Returns
        -------
        best_order : numpy.ndarray
            The best found order.
        best_value : int or float
            The evaluation value of the best found order.
        data : list of tuple
            Data useable for benchmarking. If no benchmarks were made, it will
            be None. The tuples contain the following data:
            timestamp, value of solution, best value found
            Note that the timestamp's reference point is undefined.

        """

        # get amount of neighbourhoods
        neighbourhoods_amount = self._solution.multi_neighbourhood_size()
        current_neighbourhood = 0

        # init solution
        base_value = self._solution.evaluate()
        self._solution.set_as_best(base_value)

        # add to data
        self._data_append(self.data, base_value, base_value)

        # init termination criterion
        self._termination_criterion.check_new_value(base_value)
        self._termination_criterion.start_timing()

        while self._termination_criterion.keep_running():

            # search the neighbourhood for the best move
            best_found_delta = self._best_found_delta_base_value
            best_found_move = None

            for move in self._solution.select_get_moves(current_neighbourhood):
                # check quality move
                delta = self._solution.evaluate_move(move)

                # keep data best move
                if self._function(best_found_delta, delta):
                    best_found_delta = delta
                    best_found_move = move

            # check if the best_found_move improves the delta, if this is the
            # case perform the move and set a new best solution
            base_value = base_value + best_found_delta

            self._termination_criterion.check_new_value(base_value)

            if self._function(self._solution.best_order_value, base_value):

                self._solution.move(best_found_move)
                self._solution.set_as_best(base_value)

                # add to data
                self._data_append(self.data, base_value, base_value)

            else:
                # if move is worse, change neighbourhood
                current_neighbourhood = \
                    (current_neighbourhood + 1) % neighbourhoods_amount

            self._termination_criterion.iteration_done()

        # if we have data:
        # convert data to something easier to plot
        if self.data is not None:
            data = convert_data(self.data)
        else:
            data = None

        # return results

        Results = namedtuple('Results', ['best_order', 'best_value', 'data'])

        return Results(self._solution.best_order,
                       self._solution.best_order_value,
                       data)
