from abc import ABC, abstractmethod


class AbstractTerminationCriterion(ABC):
    """Template to create terminationcriterions.

    This is a template for termination criterions. It's possible to use
    multiple criterions at once.

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

    def iteration_done(self):
        """function to be called after every iteration.

        Does not need to be used or implemented.

        """
        pass

    def check_new_value(self, value):
        """Checks a value.

        Does not need to be used or implemented.

        Parameters
        ----------
        value : int, float
            A value from the evaluation function.

        """

        pass

    def check_variable(self, variable):
        """Checks a variable specific to an implementation.

        Does not need to be used or implemented

        Parameters
        ----------
        variable
            The value of a certain value of a specific algorithm.

        """

        pass

    def start_timing(self):
        """Starts an internal timer if needed.

        Does not need to be used or implemented.

        """

        pass


