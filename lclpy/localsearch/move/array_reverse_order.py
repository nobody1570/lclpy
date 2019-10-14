import random
from lclpy.localsearch.move.abstract_move \
    import AbstractMove


class ArrayReverseOrder(AbstractMove):
    """Implements a reverse order move function for 1 dimensional numpy arrays.

    The move function performs and generates moves that reverses the order of
    values in an interval of a one-dimensional array. Note that a move is
    represented as a tuple of int. The move (x, y) represents reversing of the
    order of the values in the interval of indices [x, y] of the array.
    Note that the moves are equivalent to 2-opt.

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

    .. doctest::

        >>> import numpy
        >>> from lclpy.localsearch.move.array_reverse_order \\
        ...     import ArrayReverseOrder
        ... # init array, a move will be performed on this array
        >>> array = numpy.array([0, 1, 2, 3, 4])
        ... # init
        >>> reverse = ArrayReverseOrder(len(array))
        ... # get all possible moves in all_moves
        >>> all_moves = []
        >>> for move in reverse.get_moves():
        ...     all_moves.append(move)
        >>> all_moves
        [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        >>> # picking an arbitrary move
        >>> # Never pick a move like this yourself. It only is done here for
        >>> # the sake of showing you a clear example.
        >>> a_move = all_moves[2]
        >>> a_move
        (0, 3)
        >>> # performing the move on the array
        >>> reverse.move(array, a_move)
        >>> array
        array([3, 2, 1, 0, 4])
        >>> # undoing the move on the array
        >>> reverse.undo_move(array, a_move)
        >>> array
        array([0, 1, 2, 3, 4])

    An example of generating some random moves with get_random_move:

    .. doctest::

        >>> import random
        >>> from lclpy.localsearch.move.array_reverse_order \\
        ...    import ArrayReverseOrder
        ... # set seed random
        ... # not needed, is only used here to always get the same moves.
        >>> random.seed(0)
        ... # init
        >>> reverse = ArrayReverseOrder(10)
        ... # tests
        >>> reverse.get_random_move()
        (0, 6)
        >>> reverse.get_random_move()
        (4, 8)
        >>> reverse.get_random_move()
        (6, 7)
        >>> reverse.get_random_move()
        (4, 7)

    """

    def __init__(self, size):
        super().__init__()
        self._size = size

    def get_move_type(self):
        """Returns the move type.

        Returns
        -------
        str
            The move type.

        """

        return 'array_reverse_order'

    def move(self, array, move):
        """Performs the move asked.

        Parameters
        ----------
        array : numpy.ndarray
            The array that will be altered.
        move : tuple of int
            Represents 1 unique move. Valid moves can be retrieved by using
            get_random_move and get_move.

        """

        (index_1, index_2) = move

        # calulate the mean of index_1 and index_2
        middle = (index_1 + index_2) / 2

        # swap all pairs in the range [index_1, index_2].
        # This will change the order of the values in the range.
        while(index_1 < middle):

            array[index_1], array[index_2] = array[index_2], array[index_1]

            index_1 += 1
            index_2 -= 1

    def undo_move(self, array, move):
        """Undoes the move asked.

        Parameters
        ----------
        array : numpy.ndarray
            The array that will be altered.
        move : tuple of int
            Represents 1 unique move. Valid moves can be retrieved by using
            get_random_move and get_move.

        """

        self.move(array, move)

    def get_moves(self):
        """Iterate over all valid moves.

        Yields
        ------
        tuple of int
            The next valid move.

        """

        for i in range(self._size):
            for j in range(i + 1, self._size):
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

        # generate random numbers
        i = random.randrange(self._size)
        j = random.randrange(self._size)

        # ensure the number are different
        while i == j:
            j = random.randrange(self._size)

        # Puts the smallest number first, not needed, but ensures that every
        # move will have only 1 representation that will be used.
        if j < i:
            i, j = j, i

        return (i, j)
