from lclpy.localsearch.tabusearch.abstract_diff_state import AbstractDiffState


class SumDiffState(AbstractDiffState):
    """A class that implement a diff_state_func for tabu search.

    Examples
    --------
    A simple example:

    .. doctest::

        >>> from lclpy.localsearch.tabusearch.sum_diff_state \\
        ... 	import SumDiffState
        ... # init
        >>> test = SumDiffState()
        ... # tests
        >>> test.diff((12, 24))
        36
        >>> test.diff((3, 8))
        11
        >>> test.diff((50, 70))
        120

    """

    def __init__(self):
        super().__init__()

    def diff(self, move):
        """Indicates how the move would alter the state if it was performed.

        Parameters
        ----------
        move : tuple of int
            A tuple of 2 ints.

        Returns
        -------
        int
            The sum of the values of the tuple.

        """

        return move[0] + move[1]
