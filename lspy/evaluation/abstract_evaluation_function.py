from abc import ABC, abstractmethod


class AbstractEvaluationFunction(ABC):
    """A template to create evaluation functions.

    Evaluationfunctions are used to determine the quality of a problem.

    """

    def __init__(self):
        super().__init__()

    def get_problem_type(self):
        """Returns the problem type.

        Returns
        -------
        str
            The problem type.

        """
        raise NotImplementedError

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

        The two compared solutions are the current problem and the problem
        if the move was performed. The move is not actually performed.

        For this function to work, get_problem_type needs to be implemented,
        the move-object(s) need to have get_move_type implemented and the
        delta evaluate methods need to be properly implemented in the deltaeval
        package.

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
