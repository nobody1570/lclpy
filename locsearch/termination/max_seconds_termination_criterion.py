from locsearch.termination.abstract_termination_criterion import AbstractTerminationCriterion
import time


class MaxSecondsTerminationCriterion(AbstractTerminationCriterion):
    """Termination criterion to terminate after a set amount of seconds.

    Attributes
    ----------
    max_seconds : float
        The maximal amount of seconds passed. Is normally set to 60 seconds,
        if you need it to be more or less simply change this after
        constructing the criterion.
    _seconds : float
        The amount of seconds passed since the start of the iterations
    _start : float
        The moment when the time starts to be measured in seconds measured
        from the epoch.

    """

    def __init__(self):
        super().__init__()
        self._start = 0
        self.max_seconds = 60
        self._seconds = 0

    def keep_running(self):
        """function to determine if the algorithm needs to continue running

        Returns
        -------
        bool
            The function returns true if the amount of time passed is smaller
            than max_seconds, if the function returns false the amount of
            time passed is bigger than max_seconds

        """
        return self._seconds < self.max_seconds

    def start_timing(self):
        """function to be called before the iterations

        Sets _start to the current time in seconds from the epoch.
        
        """
        self._start = time.time()

    def iteration_done(self):
        """function to be called after every iteration

        Sets _seconds to be the difference between the current time and the
        start time.

        """
        self._seconds = time.time() - self._start
