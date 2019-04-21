from abc import ABC, abstractmethod


class AbstractTerminationCriterion(ABC):
    """Template to create termination criterions."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def keep_running(self):
        """Function to determine if the algorithm needs to continue running

        Returns
        -------
        bool
            The function returns true if the algorithm has to continue
            running, if the function returns false the algorithm needs to
            stop running.

        """

        pass

    def iteration_done(self):
        """Function to be called after every iteration.

        Does not need to be used or implemented.

        """

        pass

    def check_first_value(self, value):
        """Function that should be called once before the main loop.

        Parameters
        ----------
        value : int or float
            Is the evaluation value of the initial problem.

        """

        pass

    def check_new_value(self, value):
        """Checks a value.

        Does not need to be used or implemented.

        Parameters
        ----------
        value : int or float
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

    def reset(self):
        """Resets the object back to it's state after init."""

        raise NotImplementedError
