from locsearch.termination.abstract_termination_criterion import AbstractTerminationCriterion
import time


class MaxSecondsTerminationCriterion(AbstractTerminationCriterion):
    """Termination criterion to terminate after a set amount of seconds.

    Note that this terminationcriterion isn't exact. It will only terminate
    the algorithm after iterating longer than the set time AND if an iteration
    is finished. The extra time that the algorithm will run depends on the
    length of the last iteration.

    Parameters
    ----------
    max_seconds : float
        The maximal amount of seconds passed. The default is 60 seconds.

    Attributes
    ----------
    max_seconds : float
        The maximal amount of seconds passed.
    _seconds : float
        The amount of seconds passed since the start of the iterations
    _start : float
        The moment when the time starts to be measured in seconds measured
        from the epoch.

    Examples
    --------
    Running for 60 seconds (default):

    .. doctest::

        >>> import time
        >>> from locsearch.termination.max_seconds_termination_criterion import MaxSecondsTerminationCriterion
        >>> test = MaxSecondsTerminationCriterion()
        >>> start = time.time()
        >>> test.start_timing()
        >>> while test.keep_running():
        ...     pass # code to execute
        ...     test.iteration_done()
        >>> end = time.time()
        >>> time_passed = end - start
        >>> time_passed < 61
        True

    Running for 3 seconds:

    .. doctest::

        >>> import time
        >>> from locsearch.termination.max_seconds_termination_criterion import MaxSecondsTerminationCriterion
        >>> test = MaxSecondsTerminationCriterion(3)
        >>> start = time.time()
        >>> test.start_timing()
        >>> while test.keep_running():
        ...     pass # code to execute
        ...     test.iteration_done()
        >>> end = time.time()
        >>> time_passed = end - start
        >>> time_passed < 4
        True

    """

    def __init__(self, max_seconds=60):
        super().__init__()
        self._start = 0
        self.max_seconds = max_seconds
        self._seconds = 0

    def keep_running(self):
        """function to determine if an algorithm needs to continue running

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
