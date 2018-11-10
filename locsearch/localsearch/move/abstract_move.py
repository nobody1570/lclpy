from abc import ABC, abstractmethod


class AbstractMove(ABC):
    """Template to create Move-objects.def

    This object is used to explore new Solutions in a neighbourhood.
    """

    def __init__(self):
        super(AbstractMove, self).__init__()

    @abstractmethod
    def move(self, data, move):
        """performs a move

        Parameters
        ----------
        data
            The dataset that is being explored. It will be altered after the
            method call.
        move
            A representation of a valid move.

        """

        pass

    @abstractmethod
    def undo_move(self, data, move):
        """performs a move

        Parameters
        ----------
        data
            The dataset that is being explored. It will be altered after the
            method call.
        move
            A representation of the move one wishes to undo

        """

        pass

    @abstractmethod
    def get_moves(self):
        """A generator used to return all valid moves.

        Returns
        -------
        tuple of int
            The next valid move.

        """

        pass

    @abstractmethod
    def get_random_move(self):
        """A method used to generate a random move.

        Returns
        -------
        tuple of int
            A random valid move.
        """

        pass
