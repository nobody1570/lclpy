from abc import ABC, abstractmethod


class AbstractEvaluationFunction(ABC):
    """Template to create evaluation functions.

    Evaluationfunctions are used to determine the quality of a solution.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def evaluate(self, current_data):
        """Evaluates current_solution

        Parameters
        ----------
        current_data
            A datastructure that contains information about the current state
            of an AbstractLocalSearchSolution.

        Returns
        -------
        int or float
            an indication of the quality of current_data

        """
        pass

    def delta_evaluate(self, current_data, move):
        """Evaluates the difference in quality between two solutions.

        The two compared solutions are the current solution and the solution
        if the move was performed. The move is not actually performed.

        This function does not need to be implemented. One should only
        consider to implement and use it if a delta evaluation is faster than
        the regular evaluate function or if it needs to be implemented to work
        with existing code.

        Parameters
        ----------
        current_data
            A datastructure that contains information about the current state
            of an AbstractLocalSearchSolution.

        move
            Represents a move. The potential result of this move is evaluated
            against the current state (current_data contains information about
            the current state.).


        Returns
        -------
        int or float
            the difference in quality between the current state and the
            potential next state.

        """
        raise NotImplementedError
