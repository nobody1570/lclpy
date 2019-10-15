from lclpy.localsearch.abstract_local_search import AbstractLocalSearch

from lclpy.aidfunc.is_improvement_func import bigger, smaller
from lclpy.aidfunc.pass_func import pass_func
from lclpy.aidfunc.add_to_data_func import add_to_data_func
from lclpy.aidfunc.convert_data import convert_data
from lclpy.aidfunc.logging import log_improvement

from lclpy.localsearch.tabusearch.tabu_list import TabuList

from collections import namedtuple


class TabuSearch(AbstractLocalSearch):
    """Performs a tabu search on the given problem.

    Parameters
    ----------
    problem : AbstractLocalSearchProblem
        Contains all the data needed for the specific problem.
    termination_criterion : AbstractTerminationCriterion
        Implements a termination criterion to terminate the algorithm.
    diff_state_func : AbstractDiffState
        A class that implement a diff_state_func for tabu search.
    list_size : int, optional
        The size of the tabu list. The default is 7.
    minimise : bool, optional
        Will minimise if this parameter is True, maximise if it is False.
        The default is True.
    benchmarking : bool, optional
        Should be True if one wishes benchmarks to be kept, should be False if
        one wishes no benchmarks to be made. Default is False.
    logging: bool, optional
        Improvements will be logged to the command line if this variable is
        True. Default is True.

    Attributes
    ----------
    _problem : AbstractLocalSearchProblem
        Contains all the data needed for the specific problem.
    _termination_criterion : AbstractTerminationCriterion
        Implements a termination criterion to terminate the algorithm.
    _diff : method
        A method of a AbstractDiffState class to indicate how a move alters the
        state
    _list_size : int
        Size of the tabu list.
    _tabu_list : TabuList
        The used tabu list.
    _is_better
        Function used to determine if a certain value is an improvement.
    _minimise : bool
        Variable that indicates if the function is maximising or minimising.
    _best_found_delta_base_value : float
        Initialisation value for the delta value of each iteration. It's
        infinite when minimising or minus infinite when maximising.
    data : list of tuple
        Data useable for benchmarking. Will be None if no benchmarks are made.
    _data_append
        Function to append new data-points to data. Will do nothing if no
        benchmarks are made.
    _log_improvement
        Function to write logs to the command line. Will do nothing if no logs
        are made.

    Examples
    --------
    An example of minimising:

    .. doctest::

        >>> import numpy
        >>> import random
        >>> from lclpy.localsearch.tabusearch.tabu_search import TabuSearch
        >>> from lclpy.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from lclpy.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from lclpy.localsearch.tabusearch.sum_diff_state \\
        ...     import SumDiffState
        >>> from lclpy.problem.array_problem import ArrayProblem
        ... # seed random
        ... # (used here to always get the same output, this obviously is not
        ... #                                  needed in your implementation.)
        >>> random.seed(0)
        ... # init problem
        >>> distance_matrix = numpy.array(
        ... [[0, 2, 5, 8],
        ...  [2, 0, 4, 1],
        ...  [5, 4, 0, 7],
        ...  [8, 1, 7, 0]])
        >>> size = distance_matrix.shape[0]
        >>> move = TspArraySwap(size)
        >>> evaluation = TspEvaluationFunction(distance_matrix, move)
        >>> problem = ArrayProblem(evaluation, move, size)
        ... # init termination criterion
        >>> termination = MaxSecondsTerminationCriterion(10)
        ... # init diff_state_func
        >>> diff_state_func = SumDiffState()
        ... # init TabuSearch
        >>> tabu_search = TabuSearch(problem, termination, diff_state_func, 5, logging=False)
        ... # run algorithm
        >>> tabu_search.run()
        Results(best_order=array([0, 1, 3, 2]), best_value=15, data=None)

    An example of maximising, note that the distance matrix is different:

    .. doctest::

        >>> import numpy
        >>> import random
        >>> from lclpy.localsearch.tabusearch.tabu_search import TabuSearch
        >>> from lclpy.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from lclpy.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from lclpy.localsearch.tabusearch.sum_diff_state \\
        ...     import SumDiffState
        >>> from lclpy.problem.array_problem import ArrayProblem
        ... # seed random
        ... # (used here to always get the same output, this obviously is not
        ... #                                  needed in your implementation.)
        >>> random.seed(0)
        ... # init problem
        >>> distance_matrix = numpy.array(
        ... [[0, 8, 5, 2],
        ...  [8, 0, 4, 7],
        ...  [5, 4, 0, 1],
        ...  [2, 7, 1, 0]])
        >>> size = distance_matrix.shape[0]
        >>> move = TspArraySwap(size)
        >>> evaluation = TspEvaluationFunction(distance_matrix, move)
        >>> problem = ArrayProblem(evaluation, move, size)
        ... # init termination criterion
        >>> termination = MaxSecondsTerminationCriterion(10)
        ... # init diff_state_func
        >>> diff_state_func = SumDiffState()
        ... # init TabuSearch
        >>> tabu_search = TabuSearch(problem, termination, diff_state_func, 5,
        ...                          False, logging=False)
        ... # run algorithm
        >>> tabu_search.run()
        Results(best_order=array([0, 1, 3, 2]), best_value=21, data=None)


    """

    def __init__(self, problem, termination_criterion, diff_state_func,
                 list_size=7, minimise=True, benchmarking=False, logging=True):

        super().__init__()

        self._problem = problem
        self._termination_criterion = termination_criterion
        self._diff = diff_state_func.diff
        self._list_size = list_size
        self._tabu_list = TabuList(list_size)
        self._minimise = minimise

        if minimise:
            self._is_better = smaller
            self._best_found_delta_base_value = float("inf")
        else:
            self._is_better = bigger
            self._best_found_delta_base_value = float("-inf")

        if benchmarking:
            self.data = []
            self._data_append = add_to_data_func
        else:
            self.data = None
            self._data_append = pass_func

        if logging:
            self._log_improvement = log_improvement
        else:
            self._log_improvement = pass_func

    def run(self):
        """Starts running the tabu search.

        Returns
        -------
        best_order : numpy.ndarray
            The best found order.
        best_value : int or float
            The evaluation value of the best found order.
        data : None or collections.namedtuple
            Data useable for benchmarking. If no benchmarks were made, it will
            be None. The namedtuple contains the following data in
            numpy.ndarrays:
            time, iteration, value, best_value


        """

        # init
        base_value = self._problem.evaluate()
        self._problem.set_as_best(base_value)

        # init iteration (used to count the amount of iterations)
        iteration = 0

        # add to data
        self._data_append(self.data, iteration, base_value, base_value)

        # init termination criterion
        self._termination_criterion.check_first_value(base_value)
        self._termination_criterion.start_timing()

        # main loop
        while self._termination_criterion.keep_running():

            # search the neighbourhood for the best move
            best_found_delta = self._best_found_delta_base_value
            best_found_move = None

            for move in self._problem.get_moves():

                # check quality move
                delta = self._problem.evaluate_move(move)

                # checks how the move alters the current state
                diff = self._diff(move)

                # if not in tabu list --> not similar to earlier performed
                # moves --> if delta better than old best move
                # --> becomes the best move

                if not self._tabu_list.contains(diff) and \
                        self._is_better(best_found_delta, delta):
                    best_found_delta = delta
                    best_found_move = move
                    best_found_diff = diff

            # the best found move will be used as the next move
            # alter state problem
            base_value = base_value + best_found_delta

            # check if a move was found
            if best_found_move is not None:

                self._problem.move(best_found_move)

                # if better than best found --> new best_found
                if self._is_better(self._problem.best_order_value,
                                   base_value):
                    self._problem.set_as_best(base_value)
                    # log the better solution
                    self._log_improvement(base_value)

                # add diff to tabu list
                self._tabu_list.add(best_found_diff)

                # add to data
                self._data_append(self.data, iteration,
                                  base_value, self._problem.best_order_value)

                self._termination_criterion.check_new_value(base_value)

                # functions _termination_criterion called
                self._termination_criterion.check_new_value(base_value)

            else:
                # no move found --> we're stuck --> break loop
                break

            iteration += 1
            self._termination_criterion.iteration_done()

        # last data point
        self._data_append(self.data, iteration, base_value,
                          self._problem.best_order_value)

        # if we have data:
        # convert data to something easier to plot
        if self.data is not None:

            # convert to tuple of list
            data = convert_data(self.data)

            # make namedtuple
            DataAsLists = namedtuple(
                'Data', ['time', 'iteration', 'value', 'best_value'])

            data = DataAsLists(data[0], data[1], data[2], data[3])

        else:
            data = None

        # return results

        Results = namedtuple('Results', ['best_order', 'best_value', 'data'])

        return Results(self._problem.best_order,
                       self._problem.best_order_value,
                       data)

    def reset(self):
        """Resets the object back to it's state after init.

        Raises
        ------
        NotImplementedError
            If the problem or termination criterion have no reset method
            implemented.

        Examples
        --------
        An example of minimising, reset after run:

        .. doctest::

            >>> import numpy
            >>> import random
            >>> from lclpy.localsearch.tabusearch.tabu_search \\
            ...     import TabuSearch
            >>> from lclpy.localsearch.move.tsp_array_swap \\
            ...     import TspArraySwap
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.termination.max_iterations_termination_criterion \\
            ...     import MaxIterationsTerminationCriterion
            >>> from lclpy.localsearch.tabusearch.sum_diff_state \\
            ...     import SumDiffState
            >>> from lclpy.problem.array_problem import ArrayProblem
            ... # seed random
            ... # (used here to always get the same output, this obviously is
            ... #                           not needed in your implementation.)
            >>> random.seed(0)
            ... # init problem
            >>> distance_matrix = numpy.array(
            ... [[0, 2, 5, 8],
            ...  [2, 0, 4, 1],
            ...  [5, 4, 0, 7],
            ...  [8, 1, 7, 0]])
            >>> size = distance_matrix.shape[0]
            >>> move = TspArraySwap(size)
            >>> evaluation = TspEvaluationFunction(distance_matrix, move)
            >>> problem = ArrayProblem(evaluation, move, size)
            ... # init termination criterion
            >>> termination = MaxIterationsTerminationCriterion(5)
            ... # init TabuSearch
            ... # init diff_state_func
            >>> diff_state_func = SumDiffState()
            ... # init TabuSearch
            >>> tabu_search = TabuSearch(problem, termination, diff_state_func,
            ...                          5, True, logging=False)
            ... # state before running
            >>> tabu_search._problem._order
            array([0, 1, 2, 3])
            >>> tabu_search._termination_criterion.keep_running()
            True
            >>> len(tabu_search._tabu_list._list)
            0
            >>> # run algorithm
            >>> tabu_search.run()
            Results(best_order=array([0, 1, 3, 2]), best_value=15, data=None)
            >>> # tests reset
            >>> # before reset
            >>> tabu_search._problem._order
            array([0, 3, 2, 1])
            >>> tabu_search._termination_criterion.keep_running()
            True
            >>> len(tabu_search._tabu_list._list)
            3
            >>> # reset
            >>> tabu_search.reset()
            ... # after reset
            >>> tabu_search._problem._order
            array([0, 1, 2, 3])
            >>> tabu_search._termination_criterion.keep_running()
            True
            >>> len(tabu_search._tabu_list._list)
            0


        """

        self._problem.reset()
        self._termination_criterion.reset()

        self._tabu_list = TabuList(self._list_size)

        if self.data is not None:
            self.data = []
