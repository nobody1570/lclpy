from abc import ABC, abstractmethod


class AbstractLocalSearchSolution(ABC):
    """Template to create Solution-classes for localsearch implemenatations.

    This Class is meant to be used as a template.
    It is supposed to be used when constructing your own solution objects for a
    specific problem.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def move(self, move):
        """Performs a move.

        Parameters
        ----------
        move : tuple of int
            A representation of a move.

        """

        pass

    @abstractmethod
    def undo_move(self, move):
        """Undoes a move.

        Parameters
        ----------
        move : tuple of int
            A representation of the move one wishes to undo.

        """

        pass

    @abstractmethod
    def get_moves(self):
        """Iterable. Returns all valid moves in the neighbourhood.

        Yields
        ------
        move : tuple of int
            A representation of the next move in the neighbourhood.

        """

        pass

    @abstractmethod
    def get_random_move(self):
        """Returns a random valid move from the neighbourhood.

        Returns
        -------
        tuple of int
            A representation of the move.

        """

        pass

    @abstractmethod
    def evaluate(self):
        """Evaluates the current state of the solution.

        Returns
        -------
        int or float
            An indication of the quality of the current state.

        """

        pass

    @abstractmethod
    def set_as_best(self):
        """Saves the current state as the best found state."""

        pass

    @abstractmethod
    def state(self):
        """Returns an immutable hashable object that identifies the current state."""

        pass

    def evaluate_move(self, move):
        """Calculates the effects a move would have on the evaluation of the state.

        This function does not need to be implemented.

        Parameters
        ----------
        move : tuple of int
            The move one would like to know the effects of.

        Returns
        -------
        int or float
            An indication of the difference in quality that would be caused by
            the move.

        """

        raise NotImplementedError
