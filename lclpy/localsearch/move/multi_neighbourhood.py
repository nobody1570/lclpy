import random
import itertools
import numpy
from lclpy.localsearch.move.abstract_move \
    import AbstractMove


class MultiNeighbourhood(AbstractMove):
    """Implements a class that can be used to combine different move functions.

    Moves are represented in the following way: \n
    (index move function, a representation of a move from said move function)\n
    Note that all move functions must work on the same type of data structure.
    Combining move functions meant for different data structures won't work.

    Parameters
    ----------
    move_func_list : list of AbstractMove or tuple of AbstractMove
        A list or tuple that contains the move functions one wishes to combine.
    weights : list of int or tuple of int, optional
        A list or tuple that contains weights to increase or decrease the
        chance of a move function being used to generate a random move. The
        weight for a function must have the same index as the function.
        Weights are positive numbers and need to be defined for every move
        function. In the default case, every function will have the same
        weight. Note that it's perfectly possible to pass the probabilities
        instead of the weights.

    Attributes
    ----------
    _move_func_list : tuple of AbstractMove
        Contains all used move functions.
    _size : int
        The size of _move_func_list.
    _tresholds : tuple of float
        Tresholds associated with the move functions.

    Examples
    --------
    Get all possible moves, you should NEVER do this. You should evaluate only
    one move at a time. This example is simply to show the behaviour of
    get_moves and how to perform and undo a move:

    .. doctest::

        >>> import numpy
        >>> from lclpy.localsearch.move.array_swap import ArraySwap
        >>> from lclpy.localsearch.move.array_reverse_order \\
        ...     import ArrayReverseOrder
        >>> from lclpy.localsearch.move.multi_neighbourhood \\
        ...     import MultiNeighbourhood
        ... # init array, a move will be performed on this array
        >>> array = numpy.array([0, 1, 2])
        ... # init
        >>> swap = ArraySwap(len(array))
        >>> reverse = ArrayReverseOrder(len(array))
        >>> move_func_list = [swap, reverse]
        >>> multi = MultiNeighbourhood(move_func_list)
        ... # get all possible moves in all_moves
        >>> all_moves = []
        >>> for move in multi.get_moves():
        ...     all_moves.append(move)
        >>> all_moves
        [(0, (0, 1)), (0, (0, 2)), (0, (1, 2)), (1, (0, 1)), (1, (0, 2)), (1, (1, 2))]
        >>> # picking an arbitrary move
        >>> # Never pick a move like this yourself. It only is done here for
        >>> # the sake of showing you a clear example.
        >>> a_move = all_moves[2]
        >>> a_move
        (0, (1, 2))
        >>> # performing the move on the array
        >>> multi.move(array, a_move)
        >>> array
        array([0, 2, 1])
        >>> # undoing the move on the array
        >>> multi.undo_move(array, a_move)
        >>> array
        array([0, 1, 2])

    An example of generating some random moves with get_random_move with
    default weights (every move function has the same chance of being chosen):

    .. doctest::

        >>> import random
        >>> from lclpy.localsearch.move.array_swap import ArraySwap
        >>> from lclpy.localsearch.move.array_reverse_order \\
        ...     import ArrayReverseOrder
        >>> from lclpy.localsearch.move.multi_neighbourhood \\
        ...     import MultiNeighbourhood
        ... # set seed random
        ... # not needed, is only used here to always get the same moves.
        >>> random.seed(0)
        ... # init
        >>> swap = ArraySwap(10)
        >>> reverse = ArrayReverseOrder(10)
        >>> move_func_list = [swap, reverse]
        >>> multi = MultiNeighbourhood(move_func_list)
        ... # tests
        >>> multi.get_random_move()
        (1, (0, 6))
        >>> multi.get_random_move()
        (0, (7, 8))
        >>> multi.get_random_move()
        (0, (4, 7))
        >>> multi.get_random_move()
        (0, (3, 8))

    An example of generating some random moves with get_random_move with
    defined weights (swap weight: 1, reverse weight: 3):

    .. doctest::

        >>> import random
        >>> from lclpy.localsearch.move.array_swap import ArraySwap
        >>> from lclpy.localsearch.move.array_reverse_order \\
        ...     import ArrayReverseOrder
        >>> from lclpy.localsearch.move.multi_neighbourhood \\
        ...     import MultiNeighbourhood
        ... # set seed random
        ... # not needed, is only used here to always get the same moves.
        >>> random.seed(0)
        ... # init
        >>> swap = ArraySwap(10)
        >>> reverse = ArrayReverseOrder(10)
        >>> move_func_list = [swap, reverse]
        >>> weights = [1, 3]
        >>> multi = MultiNeighbourhood(move_func_list, weights)
        ... # tests
        >>> multi.get_random_move()
        (1, (0, 6))
        >>> multi.get_random_move()
        (1, (7, 8))
        >>> multi.get_random_move()
        (1, (4, 7))
        >>> multi.get_random_move()
        (1, (3, 8))
        >>> multi.get_random_move()
        (0, (1, 2))

    An example of generating some random moves with get_random_move with
    defined probabilities (swap probability: 0.25, reverse probability: 0.75).
    Note that the results are exactly the same as the results of the previous
    doctest:

    .. doctest::

        >>> import random
        >>> from lclpy.localsearch.move.array_swap import ArraySwap
        >>> from lclpy.localsearch.move.array_reverse_order \\
        ...     import ArrayReverseOrder
        >>> from lclpy.localsearch.move.multi_neighbourhood \\
        ...     import MultiNeighbourhood
        ... # set seed random
        ... # not needed, is only used here to always get the same moves.
        >>> random.seed(0)
        ... # init
        >>> swap = ArraySwap(10)
        >>> reverse = ArrayReverseOrder(10)
        >>> move_func_list = [swap, reverse]
        >>> weights = [0.25, 0.75]
        >>> multi = MultiNeighbourhood(move_func_list, weights)
        ... # tests
        >>> multi.get_random_move()
        (1, (0, 6))
        >>> multi.get_random_move()
        (1, (7, 8))
        >>> multi.get_random_move()
        (1, (4, 7))
        >>> multi.get_random_move()
        (1, (3, 8))
        >>> multi.get_random_move()
        (0, (1, 2))

    Test of using delta evaluation with a multineighbourhood:

    .. doctest::

        >>> import numpy
        >>> from lclpy.localsearch.move.array_swap import ArraySwap
        >>> from lclpy.localsearch.move.array_reverse_order \\
        ...     import ArrayReverseOrder
        >>> from lclpy.localsearch.move.multi_neighbourhood \\
        ...     import MultiNeighbourhood
        >>> from lclpy.evaluation.quadratic_assignment_evaluation_function \\
        ...     import QuadraticAssignmentEvaluationFunction
        ... # init array, a move will be performed on this array
        >>> array = numpy.array([0, 1, 2, 3])
        ... # init multineighbourhood
        >>> swap = ArraySwap(len(array))
        >>> reverse = ArrayReverseOrder(len(array))
        >>> move_func_list = [swap, reverse]
        >>> multi = MultiNeighbourhood(move_func_list)
        ... # init evaluation function
        >>> dist_matrix = numpy.array(
        ... [[0, 2, 9, 5],
        ...  [2, 0, 4, 6],
        ...  [9, 4, 0, 3],
        ...  [5, 6, 3, 0]])
        ... # init flow matrix
        >>> flow_matrix = numpy.array(
        ... [[0, 2, 0, 0],
        ...  [2, 0, 4, 0],
        ...  [0, 4, 0, 8],
        ...  [0, 0, 8, 0]])
        ... # init evaluation function
        >>> eval_func = QuadraticAssignmentEvaluationFunction(dist_matrix,
        ...                                                   flow_matrix,
        ...                                                   multi)
        ... # tests
        >>> order = [0, 1, 2, 3]
        >>> eval_func.evaluate([0, 1, 2, 3])
        44
        >>> eval_func.evaluate([0, 1, 3, 2])
        52
        >>> eval_func.delta_evaluate(order, (0, (2, 3)))
        8
        >>> eval_func.delta_evaluate(order, (1, (2, 3)))
        8
        >>> eval_func.evaluate([0, 3, 2, 1])
        54
        >>> eval_func.delta_evaluate(order, (0, (1, 3)))
        10
        >>> eval_func.delta_evaluate(order, (1, (1, 3)))
        10
        >>> eval_func.evaluate([3, 2, 1, 0])
        38
        >>> eval_func.delta_evaluate(order, (1, (0, 3)))
        -6

    """

    def __init__(self, move_func_list, weights=None):
        super().__init__()

        # init
        self._move_func_list = tuple(move_func_list)

        self._size = len(move_func_list)

        if weights is None:
            weights = numpy.ones(self._size)

        # calculate weight

        total_weight = sum(weights)

        # calculate probabilities

        probabilities = numpy.empty(self._size)

        for i in range(self._size):

            probabilities[i] = weights[i] / total_weight

        self._tresholds = numpy.array(
            list(itertools.accumulate(probabilities)))

    def get_move_type(self):
        """Returns the move type.

        Returns
        -------
        str
            The move type.

        """

        return 'multi_neighbourhood'

    def move(self, data, move):
        """Performs a move.

        Parameters
        ----------
        data
            The dataset that is being explored. It will be altered after the
            method call.
        move : tuple of int
            A representation of a valid move.

        """

        # pick the right move_function and perform the move
        self._move_func_list[move[0]].move(data, move[1])

    def undo_move(self, data, move):
        """Undoes a move.

        Make sure you only undo a move after it's has been performed.

        Parameters
        ----------
        data
            The dataset that is being explored. It will be altered after the
            method call.
        move : tuple of int
            A representation of the move one wishes to undo.

        """

        # pick the right move_function and undo the move
        self._move_func_list[move[0]].undo_move(data, move[1])

    def get_moves(self):
        """A generator used to return all valid moves in the neighbourhood.

        Note that all moves of all neighbourhoods are included. Duplicate moves
        are possible. All moves are generated for one neighbourhood, after
        which they will all be generated for next neighbourhood until no
        remain. The neighbourhoods will be visited in the order their
        move functions had in move_func_list when it was passed to the
        constructor.

        Yields
        ------
        tuple of int
            The next valid move.

        """

        # iterating over all move functions
        for i in range(self._size):

            # get the neighbourhood from the move_function
            neighbourhood = self._move_func_list[i].get_moves()

            # yield all moves from said neighbourhood
            for move in neighbourhood:
                yield (i, move)

    def get_random_move(self):
        """A method used to generate a random move in the neighbourhood.

        Returns
        -------
        tuple of int
            A random valid move.

        """

        # generate a random number
        random_number = random.random()

        # compare random number with all tresholds, expept the last.
        for i in range(self._size - 1):

            # if the random number is smaller than the treshold,
            # the move function that corresponds to the threshold is chosen to
            # generate the random move

            if(random_number < self._tresholds[i]):
                return (i, self._move_func_list[i].get_random_move())

        # The only treshold that we haven't checked yet is the last one, but
        # this one will always be one, thus it will always be bigger than our
        # random number. Therefore we can return a move from the corresponding
        # move function without checks.

        return (self._size - 1,
                self._move_func_list[self._size - 1].get_random_move())

    def size(self):
        """Function to get amount of neighbourhoods in the multi neighbourhood.

        Returns
        -------
        int
            The amount of neighbourhoods.

        """

        return len(self._move_func_list)

    def select_get_moves(self, neighbourhood_nr):
        """A generator used to return all moves from a specific neighbourhood.

        Yields
        ------
        tuple of int
            The next valid move from the specified neighbourhood.

        """

        # get the neighbourhood from the _move_func_list
        neighbourhood = self._move_func_list[neighbourhood_nr].get_moves()

        # yield all moves from said neighbourhood
        for move in neighbourhood:
            yield (neighbourhood_nr, move)

    def select_random_move(self, neighbourhood_nr):
        """A method used to generate a random move from a specific neighbourhood.

        Parameters
        ----------
        neighbourhood_nr : int
            Number of the neighbourhood. This number is the index of the
            neighbourhood in the list of move functions given to the
            constructor.

        Returns
        -------
        tuple of int
            A random valid move from the specified neighbourhood.

        """

        return (neighbourhood_nr,
                self._move_func_list[neighbourhood_nr].get_random_move())
