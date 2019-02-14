import numpy
from locsearch.runner.aidfunc.move_picker import get_move
from locsearch.runner.aidfunc.algorithm_picker import get_init_algorithm

from locsearch.evaluation.tsp_evaluation_function import TspEvaluationFunction
from locsearch.solution.array_solution import ArraySolution

from locsearch.termination.max_seconds_termination_criterion \
    import MaxSecondsTerminationCriterion
from locsearch.termination.max_iterations_termination_criterion \
    import MaxIterationsTerminationCriterion
from locsearch.termination.no_improvement_termination_criterion \
    import NoImprovementTerminationCriterion
from locsearch.termination.must_improve_termination_criterion \
    import MustImproveTerminationCriterion
from locsearch.termination.multi_criterion import MultiCriterion


class TspRunner():
    """A runner class for tsp problems

    Parameters
    ----------
    distance_matrix
        The distance matrix for the problem.
    algorithm_type : str, optional
        The type of localsearch one wishes to use.
        Currently only 3 algorithm_types are supported:

        +----------------------+-+---------------------+
        | Algorithm            | | algorithm_type      |
        +======================+=+=====================+
        | simulated annealing  | | simulated_annealing |
        +----------------------+-+---------------------+
        | steepest descent     | | steepest_descent    |
        +----------------------+-+---------------------+
        | tabu search          | | tabu_search         |
        +----------------------+-+---------------------+

        The default is simulated_annealing.
    move_type : str, optional
        The type of move one wishes to use.
        Currently only 3 algorithm_types are supported:

        +--------------------+-+---------------------+
        | Move               | | move_type           |
        +====================+=+=====================+
        | ArraySwap          | | array_swap          |
        +--------------------+-+---------------------+
        | TspArraySwap       | | tsp_array_swap      |
        +--------------------+-+---------------------+
        | ArrayReverseOrder  | | array_reverse_order |
        +--------------------+-+---------------------+

        The default is array_swap.
    minimise : bool, optional
        Should be True if one wishes to minimise the evaluation function,
        Should be False if one wishes to maximise the evaluation function.
    order : array_like, optional
        A one dimensional array that contains the order of the points to start
        with. All values are int, unique and are within the interval
        [0,size[. Defaultly the numbers are ordered from small to big.
    max_seconds : int, optional
        The maximal amount of seconds. Note that only the time over the main
        loop is measured and that the function will finish 1 loop after the
        maximal amount of time has passed. If no max_seconds, no max_iterations
        and no max_iter_no_impr is defined, the maximal amount of seconds will
        be defaultly set to 300, unless the algorithm_type is steepest_descent.
        In that case, the function will stop when a local extreme is reached.
        But, since this might take a long time, it would be wise to set a time
        limit just in case.
    max_iterations : int, optional
        The maximal amount of iterations allowed. One iteration of the main
        loop is considered an iteration. Defaultly there are be no restrictions
        on the amount of iterations.
    max_iter_no_impr : int, optional
        The maximal amount of iterations without improvement. One iteration of
        the main loop is considered an iteration. Defaultly there are be no
        restrictions on the amount of iterations without improvement.
    alpha : float, optional
        Only used for the algorithm type simulated_annealing. Sets the cooling
        rate of the cooling function. Should be between 0 and 1. The default is
        0,75.
        (A geometric cooling function is used.)
    iterations_temp : int, optional
        Only used for the algorithm type simulated_annealing. Sets the amount
        of iterations for every temperature level. Default is 1000.
    start_temperature : int, optional
        Only used for the algorithm type simulated_annealing. The starting
        temperature for the simulated annealing. Default is 2000.
    tabu_list_length : int, optional
        Only used for the algorithm type tabu_search. The length of the tabu
        list. Default is 7.

    """

    def __init__(self, distance_matrix, algorithm_type='simulated_annealing',
                 move_type='array_swap', minimise=True, **kwargs):
        super().__init__()

        # init distance matrix
        distance_matrix = numpy.array(distance_matrix)

        # get size
        size = distance_matrix.shape[0]

        # init move function
        move_class = get_move(move_type)

        move_function = move_class(size)

        # init evaluation function
        evaluation_function = TspEvaluationFunction(
            distance_matrix, move_function)

        # init solution
        if 'order' in kwargs:
            order = numpy.array(kwargs['order'])
            solution = ArraySolution(evaluation_function,
                                     move_function, size, order)
        else:
            solution = ArraySolution(evaluation_function, move_function, size)

        # init termination criterion
        criteria = []

        if 'max_seconds' in kwargs:
            max_seconds = kwargs['max_seconds']
            criteria.append(MaxSecondsTerminationCriterion(max_seconds))
        if 'max_iterations' in kwargs:
            max_iterations = kwargs['max_iterations']
            criteria.append(MaxIterationsTerminationCriterion(max_iterations))
        if 'max_iter_no_impr' in kwargs:
            max_iter_no_impr = kwargs['max_iter_no_impr']
            criteria.append(
                NoImprovementTerminationCriterion(max_iter_no_impr, minimise))
        if algorithm_type is 'steepest_descent':
            criteria.append(
                MustImproveTerminationCriterion())

        if len(criteria) == 0:
            termination_criterion = MaxSecondsTerminationCriterion(300)
        elif len(criteria) == 1:
            termination_criterion = criteria[0]
        else:
            termination_criterion = MultiCriterion(criteria)

        # init algorithm
        self._algorithm = get_init_algorithm(
            algorithm_type, solution, termination_criterion, minimise, kwargs)

    def run(self):
        """Runs the algorithm.

        Returns
        -------
        best_order : numpy.ndarray
            The best found order.
        best_value : int
            The evaluation value for said order.

        """

        return self._algorithm.run()
