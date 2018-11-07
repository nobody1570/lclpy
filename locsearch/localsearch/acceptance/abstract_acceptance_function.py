from abc import ABC, abstractmethod


class AbstractAcceptanceFunction(ABC):
    """Template to create acceptance functions.

    Acceptance functions determine if a worse solution than the current
    solution is accepted as the new current solution.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def accept(self, current_solution):
        """Checks if the current_solution will be accepted

         Parameters
        ----------
        current_solution : AbstractSolution
        The current solution.

        Returns
        -------
        bool
            The function returns true if the solution is accepted,
            the function returns false if the solution is rejected.

        """
        pass
