from lclpy.localsearch.abstract_local_search import AbstractLocalSearch
from lclpy.termination.always_true_criterion import AlwaysTrueCriterion

from lclpy.aidfunc.is_improvement_func import bigger, smaller
from lclpy.aidfunc.pass_func import pass_func
from lclpy.aidfunc.add_to_data_func import add_to_data_func
from lclpy.aidfunc.convert_data import convert_data
from lclpy.aidfunc.logging import log_improvement

from collections import namedtuple


class SteepestDescent(AbstractLocalSearch):
    """Performs a steepest descent algorithm on the given problem.

    Parameters
    ----------
    problem : AbstractLocalSearchProblem
        Contains all the data needed for the specific problem.
    minimise : bool, optional
        If the goal is to minimise the evaluation function, this should be
        True. If the goal is to maximise the evaluation function, this should
        be False. The default is True.
    termination_criterion : AbstractTerminationCriterion, optional
        The termination criterion that is used.
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
    _log_improvement
        Function to write logs to the command line. Will do nothing if no logs
        are made.

    Examples
    --------
    An example of minimising:

    .. doctest::

        >>> import numpy
        >>> from lclpy.localsearch.steepestdescent.steepest_descent \\
        ...     import SteepestDescent
        >>> from lclpy.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from lclpy.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from lclpy.problem.array_problem import ArrayProblem
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
        ... # init SteepestDescent
        >>> steepest_descent = SteepestDescent(problem, logging=False)
        ... # run algorithm
        >>> steepest_descent.run()
        Results(best_order=array([0, 1, 3, 2]), best_value=15, data=None)

    An example of maximising, note that the distance matrix is different:

    .. doctest::

        >>> import numpy
        >>> from lclpy.localsearch.steepestdescent.steepest_descent \\
        ...     import SteepestDescent
        >>> from lclpy.localsearch.move.tsp_array_swap import TspArraySwap
        >>> from lclpy.evaluation.tsp_evaluation_function \\
        ...     import TspEvaluationFunction
        >>> from lclpy.problem.array_problem import ArrayProblem
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
        ... # init SteepestDescent
        >>> steepest_descent = SteepestDescent(problem, False, logging=False)
        ... # run algorithm
        >>> steepest_descent.run()
        Results(best_order=array([0, 1, 3, 2]), best_value=21, data=None)



    """

    def __init__(self, problem, minimise=True, termination_criterion=None,
                 benchmarking=False, logging=True):
        super().__init__()

        self._problem = problem

        if termination_criterion is None:
            self._termination_criterion = AlwaysTrueCriterion()
        else:
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

        if logging:
            self._log_improvement = log_improvement
        else:
            self._log_improvement = pass_func

    def run(self):
        """Starts running the steepest descent.

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
            time, iteration, value


        """

        # init problem
        base_value = self._problem.evaluate()
        self._problem.set_as_best(base_value)

        # init iteration (used to vount the amount of iterations)
        iteration = 0

        # add to data
        self._data_append(self.data, iteration, base_value)

        # init termination criterion
        self._termination_criterion.check_first_value(base_value)
        self._termination_criterion.start_timing()

        while self._termination_criterion.keep_running():

            # search the neighbourhood for the best move
            best_found_delta = self._best_found_delta_base_value
            best_found_move = None

            for move in self._problem.get_moves():

                # check quality move
                delta = self._problem.evaluate_move(move)

                # keep data best move
                if self._function(best_found_delta, delta):
                    best_found_delta = delta
                    best_found_move = move

            # check if the best_found_move improves the delta, if this is the
            # case perform the move and set a new best problem
            base_value = base_value + best_found_delta

            self._termination_criterion.check_new_value(base_value)

            if self._function(self._problem.best_order_value, base_value):
                # if the found value is better

                # perform move and set new state as best.
                self._problem.move(best_found_move)
                self._problem.set_as_best(base_value)

                # log if needed
                self._log_improvement(base_value)

                # add to data
                self._data_append(self.data, iteration, base_value)

            else:

                # if it's worse: stop iterating by breaking from the loop
                break

            iteration += 1
            self._termination_criterion.iteration_done()

        # last data point
        self._data_append(self.data, iteration, base_value)

        # if we have data:
        # convert data to something easier to plot
        if self.data is not None:

            # convert to tuple of list
            data = convert_data(self.data)

            # make namedtuple
            DataAsLists = namedtuple('Data', ['time', 'iteration', 'value'])

            data = DataAsLists(data[0], data[1], data[2])

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
            >>> from lclpy.localsearch.steepestdescent.steepest_descent \\
            ...     import SteepestDescent
            >>> from lclpy.localsearch.move.tsp_array_swap \\
            ...     import TspArraySwap
            >>> from lclpy.evaluation.tsp_evaluation_function \\
            ...     import TspEvaluationFunction
            >>> from lclpy.problem.array_problem import ArrayProblem
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
            ... # init SteepestDescent
            >>> steepest_descent = SteepestDescent(problem, logging=False)
            ... # state before running
            >>> steepest_descent._problem._order
            array([0, 1, 2, 3])
            >>> steepest_descent._termination_criterion.keep_running()
            True
            >>> # run algorithm
            >>> steepest_descent.run()
            Results(best_order=array([0, 1, 3, 2]), best_value=15, data=None)
            >>> # tests reset
            >>> # before reset
            >>> steepest_descent._problem._order
            array([0, 1, 3, 2])
            >>> steepest_descent._termination_criterion.keep_running()
            True
            >>> # reset
            >>> steepest_descent.reset()
            ... # after reset
            >>> steepest_descent._problem._order
            array([0, 1, 2, 3])
            >>> steepest_descent._termination_criterion.keep_running()
            True


        """

        self._problem.reset()
        self._termination_criterion.reset()

        if self.data is not None:
            self.data = []
