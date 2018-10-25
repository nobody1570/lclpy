from abc import ABC, abstractmethod


class AbstractRunner(ABC):
    """Template to create runners.

    Runners are responsible for initializing and running an algorithm.
    I/O and, when needed, plotting data.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def run():
        """start initialization and running of the algorithm

        Returns
        -------
        AbstractSolution or None
            The best found solution, a solution or nothing at all.
        """
        pass
