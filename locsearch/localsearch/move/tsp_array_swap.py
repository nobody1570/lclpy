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

    def changed_distances(self, move):
        """Aid function for delta evaluation.

        Parameters
        ----------
        move : tuple
            A tuple of 2 ints that represents a single unique move

        Returns
        -------
        set
            this set contains a tuple with every distance that will change
            because of the move. Note that this function only works properly
            when this move-class is used.

        Examples
        --------
        Some simple examples to demonstrate the behaviour:

        .. doctest::

            >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
            >>> swap = TspArraySwap(10)
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
            >>> changed == {(9, 0), (0, 1), (8, 9), (9, 0)}
            True

        """
        changed_dist = []

        for order_index in move:
            # lower changed indices
            if order_index != 0:
                changed_dist.append((order_index - 1, order_index))
            else:
                changed_dist.append((self.size - 1, 0))

            # higher changed indices
            if order_index != self.size - 1:
                changed_dist.append((order_index, order_index + 1))
            else:
                changed_dist.append((self.size - 1, 0))

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
            move was performed.array
        move : tuple of int
            A tuple with 2 ints that represents a single, unique move.

        Returns
        -------
        frm : int
            The index in the unaltered array that corresponds with the
            same value as the parameter from in an array where the move
            was performed.
        to : int
            The index in the unaltered array that corresponds with the
            same value as the parameter to in an array where the move was
            performed.

        Examples
        --------
        Some simple examples, the indices remain the same, but the move
        changes:

        .. doctest::

            >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap as TAS
            >>> TAS.transform_next_index_to_current_index(1, 5, (1, 5))
            (5, 1)
            >>> TAS.transform_next_index_to_current_index(1, 5, (1, 3))
            (3, 5)
            >>> TAS.transform_next_index_to_current_index(1, 5, (0, 5))
            (1, 0)
            >>> TAS.transform_next_index_to_current_index(1, 5, (2, 3))
            (1, 5)


        """

        if frm in move:
            if frm == move[0]:
                frm = move[1]
            else:
                frm = move[0]

        if to in move:
            if to == move[0]:
                to = move[1]
            else:
                to = move[0]

        return (frm, to)
