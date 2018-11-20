from locsearch.localsearch.move.array_swap import ArraySwap
import random


class TspArraySwap(ArraySwap):
    """Implements a swap move for 1 dimensional numpy arrays for tsp problems.

    In tsp swapping the first location for another is pointless. This class'
    constructor removes the swaps with the first location from the
    neighbourhood. In all other respects this class is identical to
    locsearch.localsearch.move.array_swap.ArraySwap .

    Parameters
    ----------
    size : int
        The size of the numpy array that will be altered.
    Attributes
    ----------
    size : int
        The size of the numpy array that is altered.

    Examples
    --------
    Get all possible moves, you should NEVER do this. You should evaluate only
    one move at a time. This example is simply to show the behaviour of
    get_moves and how to perform and undo a move:

    ..doctest::

        >>> import numpy
        >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
        >>> array = numpy.array([0, 1, 2, 3, 4])
        >>> swap = TspArraySwap(len(array))
        >>> all_moves = []
        >>> for move in swap.get_moves():
        ...     all_moves.append(move)
        >>> all_moves
        [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        >>> a_move = all_moves[1] # picking a move (don't do it like this)
        >>> a_move
        (1, 3)
        >>> swap.move(array, a_move) # actually performing a move
        >>> array
        array([0, 3, 2, 1, 4])
        >>> swap.undo_move(array, a_move) # undoes the move
        >>> array
        array([0, 1, 2, 3, 4])

    An example of generating a random move with get_random_move:

    .. doctest::

        >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
        >>> swap = TspArraySwap(10)
        >>> test = swap.get_random_move()
        >>> 1 <= test[0] < 10 # checking if the move is valid
        True
        >>> 1 <= test[1] < 10 # checking if the move is valid
        True
        >>> test[0] != test[1] # checking if the move is valid
        True

    """

    def __init__(self, size):
        super().__init__(size)

    def get_moves(self):
        """This is a generator used to return all valid moves.

        Note that the swaps with the first position aren't included. When
        solving TSP problems, the start position doesn't matter, after all.

        Returns
        -------
        tuple of int
            The next valid move.

        """

        for i in range(1, self.size):
            for j in range(i + 1, self.size):
                yield (i, j)

    def get_random_move(self):
        """This method is used to generate one random move.

        Note that the swaps with the first position aren't included. When
        solving TSP problems, the start position doesn't matter, after all.

        Returns
        -------
        tuple of int
            A random valid move.
        """

        # It's possible to simply generate an i and then generate a bigger j,
        # but this wouldn't give us a proper distribution. Moves with a bigger
        # i would have a higher chance to be chosen than those with a smaller
        # i.

        i = random.randrange(1, self.size)
        j = random.randrange(1, self.size)

        while i == j:
            j = random.randrange(1, self.size)

        if j < i:
            i, j = j, i

        return (i, j)
