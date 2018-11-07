from abc import ABC, abstractmethod


class AbstractEvaluationFunction(ABC):
    """Template to create evaluation functions.

    Evaluationfunctions are used to determine the quality of a solution.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def evaluate(self, current_solution):
        """Evaluates current_solution

        Parameters
        ----------
        current_solution : AbstractSolution
            The Solution to be evaluated

        Returns
        -------
        int or float
            an indication of the quality of current_solution

        """
        pass

    def delta_evaluate(self, other_solution, current_solution):
        """Evaluates the difference in quality between two solutions.

        This function does not need to be implemented. One should only
        consider to implement and use it if a delta evaluation is faster than
        the regular evaluate function or if it needs to be implemented to work
        with existing code.

        Parameters
        ----------
        other_solution : AbstractSolution
            The Solution that is evaluated.

        current_solution : AbstractSolution
            The Solution that other_solution is compared to.


        Returns
        -------
        int or float
            the difference in quality between other_solution
            and current_solution.
            Note that this is equivalent to
            evaluate(other_solution)-evaluate(current_solution).

        """
        raise NotImplementedError
