from locsearch.localsearch.move.abstract_move import AbstractMove
import numpy
import random


class ArraySwap(object):
    """Implements a swap move for 1 dimensional numpy arrays.

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
        >>> from locsearch.localsearch.move.array_swap import ArraySwap
        >>> array = numpy.array([0, 1, 2, 3, 4])
        >>> swap = ArraySwap(len(array))
        >>> all_moves = []
        >>> for move in swap.get_moves():
        ...     all_moves.append(move)
        >>> all_moves
        [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        >>> a_move = all_moves[5] # picking a move (don't do it like this)
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

        >>> from locsearch.localsearch.move.array_swap import ArraySwap
        >>> swap = ArraySwap(10)
        >>> test = swap.get_random_move()
        >>> 0 <= test[0] < 10 # checking if the move is valid
        True
        >>> 0 <= test[1] < 10 # checking if the move is valid
        True
        >>> test[0] != test[1] # checking if the move is valid
        True

    """

    def __init__(self, size):
        super().__init__()

        self.size = size

    def move(self, array, move):
        """Performs the move asked.

        Parameters
        ----------
        array : numpy.ndarray
            The array where items will be swapped.
        move : tuple of int
            Represents 1 unique move. Valid moves can be retrieved by using
            get_random_move and get_move.

        """

        (index_1, index_2) = move

        array[index_1], array[index_2] = array[index_2], array[index_1]

    def undo_move(self, array, move):
        """Undoes the move asked.

        Parameters
        ----------
        array : numpy.ndarray
            The array where items will be swapped.
        move : tuple of int
            Represents 1 unique move. Valid moves can be retrieved by using
            get_random_move and get_move.

        """

        self.move(array, move)

    def get_moves(self):
        """This is a generator used to return all valid moves.

        Returns
        -------
        tuple of int
            The next valid move.

        """

        for i in range(self.size):
            for j in range(i + 1, self.size):
                yield (i, j)

    def get_random_move(self):
        """This method is used to generate one random move.

        Returns
        -------
        tuple of int
            A random valid move.
        """

        # It's possible to simply generate an i and then generate a bigger j,
        # but this wouldn't give us a proper distribution. Moves with a bigger
        # i would have a higher chance to be chosen than those with a smaller
        # i.
        i = 0
        j = 0
        while i == j:
            i = random.randrange(self.size)
            j = random.randrange(self.size)

        if j < i:
            i, j = j, i

        return (i, j)
