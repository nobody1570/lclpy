import random
from locsearch.localsearch.move.abstract_move \
    import AbstractMove


class ArraySwap(AbstractMove):
    """Implements a swap move function for 1 dimensional numpy arrays.

    The move function performs and generates moves that swap 2 values in a
    one-dimensional array. Note that a move is represented as a tuple of int.
    The move (x, y) represents the swap of the values from the indices x and y
    of the array. Equivalent to 2-opt when the array is used to keep the
    visiting order of the items.

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
        >>> from locsearch.localsearch.move.array_swap import ArraySwap
        ... # init array, a move will be performed on this array
        >>> array = numpy.array([0, 1, 2, 3, 4])
        ... # init
        >>> swap = ArraySwap(len(array))
        ... # get all possible moves in all_moves
        >>> all_moves = []
        >>> for move in swap.get_moves():
        ...     all_moves.append(move)
        >>> all_moves
        [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        >>> # picking an arbitrary move
        >>> # Never pick a move like this yourself. It only is done here for
        >>> # the sake of showing you a clear example.
        >>> a_move = all_moves[5]
        >>> a_move
        (1, 3)
        >>> # performing the move on the array
        >>> swap.move(array, a_move)
        >>> array
        array([0, 3, 2, 1, 4])
        >>> # undoing the move on the array
        >>> swap.undo_move(array, a_move)
        >>> array
        array([0, 1, 2, 3, 4])

    An example of generating some random moves with get_random_move:

    .. doctest::

        >>> import random
        >>> from locsearch.localsearch.move.array_swap import ArraySwap
        ... # set seed random
        ... # not needed, is only used here to always get the same moves.
        >>> random.seed(0)
        ... # init
        >>> swap = ArraySwap(10)
        ... # tests
        >>> swap.get_random_move()
        (0, 6)
        >>> swap.get_random_move()
        (4, 8)
        >>> swap.get_random_move()
        (6, 7)
        >>> swap.get_random_move()
        (4, 7)

    """

    def __init__(self, size):
        super().__init__()

        self._size = size

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

    def changed_distances(self, move):
        """Aid function for delta evaluation.

        This function returns the pairs who would have an altered evaluation
        value due to the move.

        Parameters
        ----------
        move : tuple of int
            A tuple of 2 ints that represents a single unique move

        Returns
        -------
        set of tuple
            this set contains a tuple with every (from,to) pair that would have
            an altered evaluation value due to the move.

        Examples
        --------
        Some simple examples to demonstrate the behaviour:

        .. doctest::

            >>> from locsearch.localsearch.move.array_swap import ArraySwap
            ... # init
            >>> swap = ArraySwap(10)
            ... # tests
            ... # since the order of the items in a set might be different,
            ... # they are compared to an equivalent set.
            >>> changed = swap.changed_distances((4, 8))
            >>> changed == {(3, 4), (4, 5), (7, 8), (8,9)}
            True
            >>> changed = swap.changed_distances((4, 9))
            >>> changed == {(3, 4), (4, 5), (8, 9), (9, 0)}
            True
            >>> changed = swap.changed_distances((0, 8))
            >>> changed == {(9, 0), (0, 1), (7, 8), (8, 9)}
            True
            >>> changed = swap.changed_distances((0, 9))
            >>> changed == {(0, 1), (8, 9), (9, 0)}
            True

        """

        changed_dist = []

        # iterating over the 2 swapped indices
        for order_index in move:

            # get the change in the lower indices
            if order_index != 0:
                changed_dist.append((order_index - 1, order_index))
            else:

                # between index 0 and index _size-1, the pair is
                # (_size - 1, 0), this because we move from _size-1 to 0
                changed_dist.append((self._size - 1, 0))

            # get the change in the higher indices
            if order_index != self._size - 1:
                changed_dist.append((order_index, order_index + 1))
            else:
                changed_dist.append((self._size - 1, 0))

        return set(changed_dist)

    @staticmethod
    def transform_next_index_to_current_index(frm, to, move):
        """Transforms frm and to depending on a move

        This function transforms the indices frm and to so that they can
        be used as indices in the unaltered array, yet return the value
        they would have had if the move was actually performed and they
        were used as indices.

        Parameters
        ----------
        frm : int
            the from index that one wants to use in the array with if the
            move was performed.
        to : int
            the to index that one wants to use in the array with if the
            move was performed.
        move : tuple of int
            A tuple with that represents a single, unique move.

        Returns
        -------
        frm : int
            The index in the unaltered array that has the same value as the
            parameter frm in an array where the move was performed.
        to : int
            The index in the unaltered array that has the same value as the
            parameter to in an array where the move was performed.

        Examples
        --------
        Some simple examples, the indices remain the same, but the move
        changes:

        .. doctest::

            >>> from locsearch.localsearch.move.array_swap \\
            ...     import ArraySwap as AS
            >>> AS.transform_next_index_to_current_index(1, 5, (1, 5))
            (5, 1)
            >>> AS.transform_next_index_to_current_index(1, 5, (1, 3))
            (3, 5)
            >>> AS.transform_next_index_to_current_index(1, 5, (0, 5))
            (1, 0)
            >>> AS.transform_next_index_to_current_index(1, 5, (2, 3))
            (1, 5)


        """

        # check if the frm value is affected by the move
        if frm in move:

            # transform frm so it returns the value that from would have if the
            # move was performed.
            if frm == move[0]:
                frm = move[1]
            else:
                frm = move[0]

        # check if the to value is affected by the move
        if to in move:
            # transform to so it returns the value that from would have if the
            # move was performed.
            if to == move[0]:
                to = move[1]
            else:
                to = move[0]

        return (frm, to)
