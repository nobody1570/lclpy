from abc import ABC, abstractmethod


class AbstractMove(ABC):
    """Template to create Move-objects.

    This object is used to explore a neighbourhood and alter the state of a
    solution. It can also be used to generate valid moves in the neighbourhood.

    """

    def __init__(self):
        super(AbstractMove, self).__init__()

    def get_move_type(self):
        """Returns the move type.

        This function is used in the implementation of delta evaluation. If
        this is not implemented or wanted, this method does not need to be
        implemented.

        Returns
        -------
        str
            The move type.

        """

        raise NotImplementedError

    @abstractmethod
    def move(self, data, move):
        """Performs a move.

        Parameters
        ----------
        data
            The dataset that is being explored. It will be altered after the
            method call.
        move : tuple of int
            A representation of a valid move.

        """

        pass

    @abstractmethod
    def undo_move(self, data, move):
        """Undoes a move.

        Make sure you only undo a move after it's has been performed.

        Parameters
        ----------
        data
            The dataset that is being explored. It will be altered after the
            method call.
        move : tuple of int
            A representation of the move one wishes to undo

        """

        pass

    @abstractmethod
    def get_moves(self):
        """A generator used to return all valid moves in the neighbourhood.

        Yields
        ------
        tuple of int
            The next valid move.

        """

        pass

    @abstractmethod
    def get_random_move(self):
        """A method used to generate a random move in the neighbourhood.

        Returns
        -------
        tuple of int
            A random valid move.
        """

        pass
