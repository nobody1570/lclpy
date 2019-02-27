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
        """Returns an immutable hashable object that identifies the current state.

        Returns
        -------
        tuple
            A representation of the current state.

        """

        pass

    @abstractmethod
    def reset(self):
        """Resets the object back to it's state after init."""

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

    def next_neighbourhood(self):
        """Changes the current neighbourhood to the next neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.
        If this function is called when the last neighbourhood is the current
        neighbourhood, the first neighbourhood will become the current
        neighbourhood.

        Raises
        ------
        WrongMoveType
            If the neighbourhood isn't a MultiNeighbourhood.

        """

        raise NotImplementedError

    def previous_neighbourhood(self):
        """Changes the current neighbourhood to the previous neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.
        If this function is called when the first neighbourhood is the current
        neighbourhood, the first neighbourhood will remain the current
        neighbourhood.

        Raises
        ------
        WrongMoveType
            If the neighbourhood isn't a MultiNeighbourhood.

        """

        raise NotImplementedError

    def select_get_moves(self):
        """Function to get all moves from a specific neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.

        Parameters
        ----------
        neighbourhood_nr : int
            Number of the neighbourhood. This number is the index of the
            neighbourhood in the list of move functions given to the
            constructor.

        Returns
        -------
        generator
            An iterable generator object that contains all the moves of the
            current neighbourhood.

        Raises
        ------
        WrongMoveType
            If the neighbourhood isn't a MultiNeighbourhood.

        """

        raise NotImplementedError

    def select_random_move(self):
        """A method used to generate a random move from a specific neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.

        Parameters
        ----------
        neighbourhood_nr : int
            Number of the neighbourhood. This number is the index of the
            neighbourhood in the list of move functions given to the
            constructor.

        Returns
        -------
        tuple of int
            A random valid move from the current neighbourhood.

        Raises
        ------
        WrongMoveType
            If the neighbourhood isn't a MultiNeighbourhood.

        """

        raise NotImplementedError
