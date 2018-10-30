from abc import ABC, abstractmethod


class AbstractTerminationCriterion(ABC):
    """Template to create terminationcriterions.

    This is a template for termination criterions. It's possible to use
    multiple criterions at once. If the criterions use data that's different,
    it's better to not combine them, simply implement them as seperate
    termination criterions.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def keep_running(self):
        """function to determine if the algorithm needs to continue running

        Returns
        -------
        bool
            The function returns true if the algorithm has to continue
            running, if the function returns false the algorithm needs to
            stop running.

        """
        pass
