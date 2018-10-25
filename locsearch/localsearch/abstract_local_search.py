from abc import ABC, abstractmethod


class AbstractLocalSearch(ABC):
    """Template for the implementation of local search algorithms

    This class should only contain the logic needed to run the local search.
    I/O and plotting should be handled by a runner.
    The localsearch should contain a working terminationCriterion.
    """

    def __init__(self, solution):
        """__init__

        Parameters
        ----------
        solution : AbstractLocalSearchSolution
            An object derived from AbstractLocalSearchSolution that contains
            the data needed to perform the local search.

        """

        super().__init__()
        self.solution = solution

    @abstractmethod
    def run():
        """start running the local search

        Returns
        -------
        AbstractLocalSearchSolution or dict
            The best found solution or a dictionary with the best found
            solution and optionally other information about the terminated
            localsearch.

        """

        pass
