from lclpy.localsearch.move.array_swap import ArraySwap
import random


class TspArraySwap(ArraySwap):
    """Implements a swap move for 1 dimensional numpy arrays for tsp problems.

    In TSP problems swapping the first location with another is pointless. This
    class does not generate swaps with the first location from the
    neighbourhood. In all other respects this class is identical to it's base
    class Arrayswap.

    The move function performs and generates moves that swap 2 values in a
    one-dimensional array. Note that a move is represented as a tuple of int.
    The move (x, y) represents the swap of the values from the indices x and y
    of the array.

    Parameters
    ----------
    size : int
        The size of the numpy array that will be altered.
    Attributes
    ----------
    _size : int
        The size of the numpy array that is altered.

    Examples
    --------
    Get all possible moves, you should NEVER do this. You should evaluate only
    one move at a time. This example is simply to show the behaviour of
    get_moves and how to perform and undo a move:

    ..doctest::

        >>> import numpy
        >>> from lclpy.localsearch.move.tsp_array_swap import TspArraySwap
        ... # init array, a move will be performed on this array
        >>> array = numpy.array([0, 1, 2, 3, 4])
        ... # init
        >>> swap = TspArraySwap(len(array))
        ... # get all possible moves in all_moves
        >>> all_moves = []
        >>> for move in swap.get_moves():
        ...     all_moves.append(move)
        >>> all_moves
        [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        >>> # picking an arbitrary move
        >>> # Never pick a move like this yourself. It only is done here for
        >>> # the sake of showing you a clear example.
        >>> a_move = all_moves[1]
        >>> a_move
        (1, 3)
        >>> # performing the move on the array
        >>> swap.move(array, a_move)
        >>> array
        array([0, 3, 2, 1, 4])
        >>> # undoing the move on the array
        >>> swap.undo_move(array, a_move) # undoes the move
        >>> array
        array([0, 1, 2, 3, 4])

    An example of generating some random moves with get_random_move:

    .. doctest::

        >>> import random
        >>> from lclpy.localsearch.move.tsp_array_swap import TspArraySwap
        ... # set seed random
        ... # not needed, is only used here to always get the same moves.
        >>> random.seed(0)
        ... # init
        >>> swap = TspArraySwap(10)
        ... # tests
        >>> swap.get_random_move()
        (1, 7)
        >>> swap.get_random_move()
        (5, 9)
        >>> swap.get_random_move()
        (7, 8)
        >>> swap.get_random_move()
        (5, 8)

    """

    def __init__(self, size):
        super().__init__(size)

    def get_moves(self):
        """This is a generator used to return all valid moves.

        Note that the swaps with the first position aren't included. When
        solving TSP problems, the start position doesn't matter.

        Yields
        ------
        tuple of int
            The next valid move.

        """

        for i in range(1, self._size):
            for j in range(i + 1, self._size):
                yield (i, j)

    def get_random_move(self):
        """This method is used to generate one random move.

        Note that the swaps with the first position aren't included. When
        solving TSP problems, the start position doesn't matter.

        Returns
        -------
        tuple of int
            A random valid move.
        """

        # It's possible to simply generate an i and then generate a bigger j,
        # but this wouldn't give us a proper distribution. Moves with a bigger
        # i would have a higher chance to be chosen than those with a smaller
        # i.

        # generate random numbers
        i = random.randrange(1, self._size)
        j = random.randrange(1, self._size)

        # ensure the number are different
        while i == j:
            j = random.randrange(1, self._size)

        # Puts the smallest number first, not needed, but ensures that every
        # move will have only 1 representation that will be used.
        if j < i:
            i, j = j, i

        return (i, j)
