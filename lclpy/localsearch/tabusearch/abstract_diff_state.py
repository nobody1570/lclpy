from abc import ABC, abstractmethod


class AbstractDiffState(ABC):
    """A template class to implement a diff_state_func for tabu search.

    Implementations of this class are meant to be used in a tabu search
    algorithm. Implementations are supposed to implement the diff function.
    A specific implementation might be needed for different move types.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def diff(self, move):
        """Indicates how the move would alter the state if it was performed.

        Parameters
        ----------
        move : tuple of int
            A representation of a move.

        Returns
        -------
        int
            An indication of how the move alters the state.

        """

        pass
