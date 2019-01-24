from locsearch.localsearch.abstract_local_search import AbstractLocalSearch
from collections import deque, namedtuple
from locsearch.aidfunc.is_improvement_func import bigger, smaller
from locsearch.aidfunc.aid_deque import insert_in_sorted_deque
from locsearch.localsearch.tabusearch.tabu_list import TabuList


class TabuSearch(AbstractLocalSearch):
    """Performs a tabu search on the given solution.

    Parameters
    ----------
    solution : AbstractLocalSearchSolution
        Contains all the data needed for the specific problem.
    termination_criterion : AbstractTerminationCriterion
        Implements a termination criterion to terminate the algorithm.
    list_size : int, optional
        The size of the tabu list. The default is 7.
    minimise : bool, optional
        Will minimise if this parameter is True, maximise if it is False.
        The default is True.

    Attributes
    ----------
    _solution : AbstractLocalSearchSolution
        Contains all the data needed for the specific problem.
    _termination_criterion : AbstractTerminationCriterion
        Implements a termination criterion to terminate the algorithm.
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

    Examples
    --------
    An example of minimising:

    .. doctest::

        >>> import numpy
        >>> import random
        >>> from locsearch.localsearch.tabusearch.tabu_search import TabuSearch
        >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from locsearch.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from locsearch.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from locsearch.solution.tsp_solution import TspSolution
        ... # seed random
        ... # (used here to always get the same output, this obviously is not
        ... #                                  needed in your implementation.)
        >>> random.seed(0)
        ... # init solution
        >>> distance_matrix = numpy.array(
        ... [[0, 2, 5, 8],
        ...  [2, 0, 4, 1],
        ...  [5, 4, 0, 7],
        ...  [8, 1, 7, 0]])
        >>> size = distance_matrix.shape[0]
        >>> move = TspArraySwap(size)
        >>> evaluation = TspEvaluationFunction(distance_matrix, move)
        >>> solution = TspSolution(evaluation, move, size)
        ... # init termination criterion
        >>> termination = MaxSecondsTerminationCriterion(10)
        ... # init TabuSearch
        >>> tabu_search = TabuSearch(solution, termination, 5, True)
        ... # run algorithm
        >>> tabu_search.run()
        Results(best_order=array([0, 1, 3, 2]), best_value=15)

    An example of maximising, note that the distance matrix is different:

    .. doctest::

        >>> import numpy
        >>> import random
        >>> from locsearch.localsearch.tabusearch.tabu_search import TabuSearch
        >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from locsearch.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from locsearch.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from locsearch.solution.tsp_solution import TspSolution
        ... # seed random
        ... # (used here to always get the same output, this obviously is not
        ... #                                  needed in your implementation.)
        >>> random.seed(0)
        ... # init solution
        >>> distance_matrix = numpy.array(
        ... [[0, 8, 5, 2],
        ...  [8, 0, 4, 7],
        ...  [5, 4, 0, 1],
        ...  [2, 7, 1, 0]])
        >>> size = distance_matrix.shape[0]
        >>> move = TspArraySwap(size)
        >>> evaluation = TspEvaluationFunction(distance_matrix, move)
        >>> solution = TspSolution(evaluation, move, size)
        ... # init termination criterion
        >>> termination = MaxSecondsTerminationCriterion(10)
        ... # init TabuSearch
        >>> tabu_search = TabuSearch(solution, termination, 5, False)
        ... # run algorithm
        >>> tabu_search.run()
        Results(best_order=array([0, 1, 3, 2]), best_value=21)


    """

    def __init__(self, solution, termination_criterion,
                 list_size=7, minimise=True):
        super().__init__()

        self._solution = solution
        self._termination_criterion = termination_criterion
        self._list_size = list_size
        self._tabu_list = TabuList(list_size)
        self._minimise = minimise

        if minimise:
            self._is_better = smaller
            self._best_found_delta_base_value = float("inf")
        else:
            self._is_better = bigger
            self._best_found_delta_base_value = float("-inf")

    def run(self):
        """Starts running the tabu search.

        Returns
        -------
        best_order : numpy.ndarray
            A one dimensional numpy array that contains the order of the
            points for the best found solution.
        best_value : int or float
            The best found value of the evaluation function. This should be
            the evaluation value of best_order.

        """

        # init
        base_value = self._solution.evaluate()
        self._solution.set_as_best(base_value)

        # init termination criterion
        self._termination_criterion.check_new_value(base_value)
        self._termination_criterion.start_timing()

        # init deque
        # we need to remember one move more than there are items in the
        # tabu list, to enable us to always perform a move when it's possible.
        # The best moves should be at the right side of the deque, the worst
        # at the left side

        best_moves = deque(maxlen=self._list_size + 1)

        # main loop
        while self._termination_criterion.keep_running():

            # tabu implementation
            # search the neighbourhood for the best move
            best_moves.clear()

            for move in self._solution.get_moves():

                # check quality move
                delta = self._solution.evaluate_move(move)

                # if the move is better than those in the best_moves deque
                # --> insert in deque
                delta_move = (delta, move)

                if len(best_moves) <= self._list_size:
                    insert_in_sorted_deque(
                        best_moves, self._is_better, delta_move)

                elif any(self._is_better(item, delta_move)
                         for item in best_moves):
                    # remove the worst item (should be at the left)
                    best_moves.popleft()

                    # insert the item at the correct position
                    insert_in_sorted_deque(
                        best_moves, self._is_better, delta_move)

            # pick the best move that doesn't lead to a state in the tabu list

            while len(best_moves) > 0:

                # get the move and alter the state
                (delta, move) = best_moves.pop()

                self._solution.move(move)

                # check if state in tabu list
                if self._tabu_list.contains(self._solution.state()):

                    # if it's in there --> unwanted state --> undo move
                    self._solution.undo_move(move)

                else:
                    # state not in tabu list --> keep state

                    # update the cost value
                    base_value = base_value + delta
                    # add new state to tabu list
                    self._tabu_list.add(self._solution.state())
                    # check if best found state
                    # --> if best found state set as new best state
                    if self._is_better(
                            self._solution.best_order_value, base_value):
                        self._solution.set_as_best(base_value)

                    # good move found --> terminate search loop
                    break

            else:
                # no non-tabu move possible
                # --> we're stuck --> terminate main loop
                break

            # functions _termination_criterion called
            self._termination_criterion.check_new_value(base_value)
            self._termination_criterion.iteration_done()

        # return results

        Results = namedtuple('Results', ['best_order', 'best_value'])

        return Results(self._solution.best_order,
                       self._solution.best_order_value)