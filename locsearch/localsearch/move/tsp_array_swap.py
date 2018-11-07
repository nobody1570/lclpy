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
