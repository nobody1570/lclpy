from abc import ABC, abstractmethod


class AbstractLocalSearchProblem(ABC):
    """Template to create Problem-classes for localsearch implemenatations.

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
        """An iterable that returns all valid moves in the complete neighbourhood.

        Yields
        ------
        move : tuple of int
            A representation of the next move in the neighbourhood.

        """

        pass

    @abstractmethod
    def get_random_move(self):
        """A function to return a random move from the complete neighbourhood.

        Returns
        -------
        tuple of int
            A representation of the move.

        """

        pass

    def evaluate_move(self, move):
        """Evaluates the quality gained or lost by a potential move.

        This function does not need to be implemented.

        Parameters
        ----------
        move : tuple of int
            Represents a unique valid move.

        Returns
        -------
        int or float
            The change in value of the eval-function if the move is performed.

        """

        raise NotImplementedError

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
        """Returns an immutable hashable object that describes the current state.

        Returns
        -------
        tuple
            A representation of the current state.

        """

        pass

    def first_neighbourhood(self):
        """Changes the current neighbourhood to the first neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.

        Raises
        ------
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

        """

        raise NotImplementedError

    def next_neighbourhood(self):
        """Changes the current neighbourhood to the next neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.
        If this function is called when the last neighbourhood is the current
        neighbourhood, the last neighbourhood will remain the current
        neighbourhood and an exception will be raised.

        Raises
        ------
        NoNextNeighbourhood
            If there is no next neighbourhood. This is simply an indication
            that the current neighbourhood was the last neighbourhood.
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

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
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

        """

        raise NotImplementedError

    def select_get_moves(self):
        """Function to get all moves from the current neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.

        Returns
        -------
        generator
            An iterable generator object that contains all the moves of the
            current neighbourhood.

        Raises
        ------
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

        """

        raise NotImplementedError

    def select_random_move(self):
        """A method used to generate a random move from the current neighbourhood.

        Note that this function will only be useable if the neighbourhood given
        to the constructor is a MultiNeighbourhood.

        Returns
        -------
        tuple of int
            A random valid move from the current neighbourhood.

        Raises
        ------
        WrongMoveTypeError
            If the move_function isn't a MultiNeighbourhood.

        """

        raise NotImplementedError

    @abstractmethod
    def reset(self):
        """Resets the object back to it's state after init."""

        pass
