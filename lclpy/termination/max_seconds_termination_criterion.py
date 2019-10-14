from time import time
from lclpy.termination.abstract_termination_criterion \
    import AbstractTerminationCriterion


class MaxSecondsTerminationCriterion(AbstractTerminationCriterion):
    """Termination criterion to terminate after a set amount of seconds.

    Note that this terminationcriterion isn't exact. It will only terminate
    the algorithm after iterating longer than the set time AND if an iteration
    is finished. The extra time that the algorithm will run depends on the
    duration of the last iteration.

    Parameters
    ----------
    max_seconds : int or float, optional
        The maximal amount of seconds passed. The default is 60 seconds.

    Attributes
    ----------
    _max_seconds : int or float
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
        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        ... # init
        >>> test = MaxSecondsTerminationCriterion()
        ... # start and stop will be used to measure the time passed.
        >>> start = time.time()
        ... # start the timing of the termination criterion
        >>> test.start_timing()
        ... # loop
        >>> while test.keep_running():
        ...     pass # code to execute
        ...     test.iteration_done()
        ... # calculate and check the time passed
        >>> stop = time.time()
        >>> time_passed = stop - start
        >>> time_passed < 61
        True

    Running for 3 seconds:

    .. doctest::

        >>> import time
        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        ... # init
        >>> test = MaxSecondsTerminationCriterion(3)
        ... # start and stop will be used to measure the time passed.
        >>> start = time.time()
        ... # start the timing of the termination criterion
        >>> test.start_timing()
        ... # loop
        >>> while test.keep_running():
        ...     pass # code to execute
        ...     test.iteration_done()
        >>> stop = time.time()
        >>> time_passed = stop - start
        >>> time_passed < 4
        True

    """

    def __init__(self, max_seconds=60):
        super().__init__()
        self._start = 0
        self._max_seconds = max_seconds
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

        return self._seconds < self._max_seconds

    def start_timing(self):
        """function to be called before the iterations

        Sets _start to the current time in seconds from the epoch.

        """

        self._start = time()

    def iteration_done(self):
        """function to be called after every iteration

        Sets _seconds to be the difference between the current time and the
        start time.

        """

        self._seconds = time() - self._start

    def reset(self):
        """Resets the object back to it's state after init.

        Examples
        --------
        Running for 3 seconds:

        .. doctest::

            >>> import time
            >>> from lclpy.termination.max_seconds_termination_criterion \\
            ...     import MaxSecondsTerminationCriterion
            ... # init
            >>> test = MaxSecondsTerminationCriterion(3)
            ... # start and stop will be used to measure the time passed.
            ... # run 1
            >>> start = time.time()
            ... # start the timing of the termination criterion
            >>> test.start_timing()
            ... # loop
            >>> while test.keep_running():
            ...     pass # code to execute
            ...     test.iteration_done()
            >>> stop = time.time()
            >>> time_passed = stop - start
            >>> time_passed < 4
            True
            >>> # reset
            >>> test.reset()
            ... # run 2
            >>> start = time.time()
            ... # start the timing of the termination criterion
            >>> test.start_timing()
            ... # loop
            >>> while test.keep_running():
            ...     pass # code to execute
            ...     test.iteration_done()
            >>> stop = time.time()
            >>> time_passed = stop - start
            >>> time_passed < 4
            True



        """

        self._start = 0
        self._seconds = 0
