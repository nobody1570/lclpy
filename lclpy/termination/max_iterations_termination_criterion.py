from lclpy.termination.abstract_termination_criterion \
    import AbstractTerminationCriterion


class MaxIterationsTerminationCriterion(AbstractTerminationCriterion):
    """Termination criterion to terminate after a set amount of iterations.

    Parameters
    ----------
    max_iterations : int, optional
        The maximal amount of iterations. The default is 1000 iterations.

    Attributes
    ----------
    _max_iterations : int
        The maximal amount of iterations.
    _iterations : int
        The amount of iterations.

    Examples
    --------
    Default amount of iterations:

    .. doctest::

        >>> from lclpy.termination.max_iterations_termination_criterion \\
        ...     import MaxIterationsTerminationCriterion
        ... # the variable iterations will be used to count the amount of
        ... # iterations.
        >>> iterations = 0
        ... # init
        >>> test = MaxIterationsTerminationCriterion()
        ... # test
        >>> while test.keep_running():
        ...     pass # other code to be executed
        ...     # counting amount of iterations
        ...     iterations += 1
        ...     test.iteration_done()
        >>> iterations
        1000

    50 iterations:

    .. doctest::

        >>> from lclpy.termination.max_iterations_termination_criterion \\
        ...     import MaxIterationsTerminationCriterion
        ... # the variable iterations will be used to count the amount of
        ... # iterations.
        >>> iterations = 0
        ... # init
        >>> test = MaxIterationsTerminationCriterion(50)
        ... # test
        >>> while test.keep_running():
        ...     pass # other code to be executed
        ...     # counting amount of iterations
        ...     iterations += 1
        ...     test.iteration_done()
        >>> iterations
        50

    """

    def __init__(self, max_iterations=1000):
        super().__init__()
        self._max_iterations = max_iterations
        self._iterations = 0

    def keep_running(self):
        """function to determine if the algorithm needs to continue running.

        Returns
        -------
        bool
            The function returns true if the amount of iteration is smaller
            than max_iterations, if the function returns false the amount of
            iterations is bigger than max_iterations

        """

        return self._iterations < self._max_iterations

    def iteration_done(self):
        """function to be called after every iteration.

        Increments _iterations by 1.

        """

        self._iterations += 1

    def reset(self):
        """Resets the object back to it's state after init.

        Examples
        --------
        Default amount of iterations:

        .. doctest::

            >>> from lclpy.termination.max_iterations_termination_criterion \\
            ...     import MaxIterationsTerminationCriterion
            ... # the variable iterations will be used to count the amount of
            ... # iterations.
            >>> iterations = 0
            ... # init
            >>> test = MaxIterationsTerminationCriterion()
            ... # run 1
            >>> while test.keep_running():
            ...     pass # other code to be executed
            ...     # counting amount of iterations
            ...     iterations += 1
            ...     test.iteration_done()
            >>> iterations
            1000
            >>> # reset
            >>> test.reset()
            ... # run 2
            >>> iterations = 0
            >>> while test.keep_running():
            ...     pass # other code to be executed
            ...     # counting amount of iterations
            ...     iterations += 1
            ...     test.iteration_done()
            >>> iterations
            1000

        """

        self._iterations = 0
