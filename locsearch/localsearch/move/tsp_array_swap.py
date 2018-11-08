from locsearch.localsearch.move.array_swap import ArraySwap
import numpy


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
    possible_swaps : numpy.ndarray
        This 2 dimensional array contains all possible swaps that aren't with
        the first item of the array. The 2 points that are swapped in a single
        swap are saved as
        possible_swaps[index][0] and _possible_swaps[index][1].
        It contains the neighbourhood; all possible swaps are represented.
    neighbourhood_size : int
        The size of the neighboorhood. This is also the size of
        possible_swaps.

    Examples
    --------
    A simple example:

    ..doctest::

        >>> import numpy
        >>> from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
        >>> array = numpy.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> swap = TspArraySwap(len(array))
        >>> swap.neighbourhood_size
        36
        >>> swap.move(array, 12)
        >>> array
        array([0, 1, 7, 3, 4, 5, 6, 2, 8, 9])
        >>> swap.move(array, 30)
        >>> array
        array([0, 1, 7, 3, 4, 5, 2, 6, 8, 9])

    """

    def __init__(self, size):
        super().__init__(size)

        # remove swaps with the first item

        to_delete = []
        for i in range(self.neighbourhood_size):
            if self.possible_swaps[i][0] == 0 or \
                    self.possible_swaps[i][1] == 0:
                to_delete.append(i)

        self.possible_swaps = numpy.delete(self.possible_swaps, to_delete, 0)

        # update neighbourhood_size
        self.neighbourhood_size = self.possible_swaps.shape[0]

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
