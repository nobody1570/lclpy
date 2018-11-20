from abc import ABC, abstractmethod


class AbstractLocalSearch(ABC):
    """Template for the implementation of local search algorithms

    This class should only contain the logic needed to run the local search.
    I/O and plotting should be handled by a runner.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def run():
        """start running the local search

        Returns
        -------
        Results : collections.namedtuple
            Contains the best found case and the evaluation value for said
            case.

        """

        pass
