from locsearch.localsearch.move.abstract_move import AbstractMove
import numpy


class ArraySwap(object):
    """Implements a swap move for 1 dimensional numpy arrays.

    Parameters
    ----------
    size : int
        The size of the numpy array that will be altered.

    Attributes
    ----------
    possible_swaps : numpy.ndarray
        This 2 dimensional array contains all possible swaps. The 2 points
        that are swapped in a single swap are saved as
        possible_swaps[index][0] and possible_swaps[index][1].
        It contains the neighbourhood; all possible swaps are represented.
    neighbourhood_size : int
        The size of the neighboorhood.

    Examples
    --------
    A simple example:

    ..doctest::

        >>> import numpy
        >>> from locsearch.localsearch.move.array_swap import ArraySwap
        >>> array = numpy.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> swap = ArraySwap(len(array))
        >>> swap.neighbourhood_size
        45
        >>> swap.move(array, 21)
        >>> array
        array([0, 1, 7, 3, 4, 5, 6, 2, 8, 9])
        >>> swap.move(array, 39)
        >>> array
        array([0, 1, 7, 3, 4, 5, 2, 6, 8, 9])

    """

    def __init__(self, size):
        super().__init__()

        # generate all possible swaps --> this is the neighbourhood
        possible_swaps = []

        for i in range(size):
            for j in range(i + 1, size):
                possible_swaps.append([i, j])

        self.possible_swaps = numpy.array(possible_swaps)

        self.neighbourhood_size = len(possible_swaps)

    def move(self, array, move_number):
        """Performs the move asked.

        Parameters
        ----------
        array : numpy.ndarray
            The array where items will be swapped.
        move_number : int
            Has no real meaning. For a certain value, it will always perform
            the same move. The value needs to be in the interval
            [0,neighbourhood_size[.

        """
        self._swap(
            array,
            self.possible_swaps[move_number][0],
            self.possible_swaps[move_number][1])

    def _swap(self, array, index_1, index_2):
        """swaps the values of index_1 and index_2 in the array.


        Parameters
        ----------
        array : numpy.ndarray
            The one-dimensional array where the swap move will be performed on.
        index_1, index_2 : int
            The indexes of the values of the array that need to be swapped.

        """

        array[index_1], array[index_2] = array[index_2], array[index_1]
