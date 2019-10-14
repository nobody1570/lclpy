from lclpy.termination.abstract_termination_criterion \
    import AbstractTerminationCriterion


class MultiCriterion(AbstractTerminationCriterion):
    """Class to combine multiple terminationcriteria.

    Parameters
    ----------
    criteria : list or tuple of AbstractTerminationCriterion
        An iterable object containing the intialised termination criterions one
        wishes to use.

    Attributes
    ----------
    criteria : list or tuple of AbstractTerminationCriterion
        An iterable object containing the intialised termination criterions one
        wishes to use.

    Examples
    --------
    3 termination criteria are used, three tests are done to ensure that all
    three criterions are capable of stopping the iterating correctly.

    MaxSecondsTerminationCriterion stops the iterating:

     .. doctest::

        >>> import time
        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from lclpy.termination.max_iterations_termination_criterion \\
        ...     import MaxIterationsTerminationCriterion
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        >>> from lclpy.termination.multi_criterion import MultiCriterion
        ... # init list
        >>> criteria = []
        >>> criteria.append(MaxSecondsTerminationCriterion(3))
        >>> criteria.append(MaxIterationsTerminationCriterion(10))
        >>> criteria.append(NoImprovementTerminationCriterion(3))
        ... # init MultiCriterion
        >>> multi_criterion = MultiCriterion(criteria)
        ... # test
        >>> start = time.time()
        >>> multi_criterion.start_timing()
        >>> while multi_criterion.keep_running():
        ...     multi_criterion.iteration_done()
        >>> stop = time.time()
        >>> time_passed = stop - start
        >>> time_passed < 4
        True


    MaxIterationsTerminationCriterion stops the iterating:

    .. doctest::

        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from lclpy.termination.max_iterations_termination_criterion \\
        ...     import MaxIterationsTerminationCriterion
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        >>> from lclpy.termination.multi_criterion import MultiCriterion
        ... # init list
        >>> criteria = []
        >>> criteria.append(MaxSecondsTerminationCriterion(3))
        >>> criteria.append(MaxIterationsTerminationCriterion(10))
        >>> criteria.append(NoImprovementTerminationCriterion(3))
        ... # init MultiCriterion
        >>> multi_criterion = MultiCriterion(criteria)
        ... # test
        >>> iterations = 0
        >>> values = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9]
        >>> multi_criterion.start_timing()
        >>> while multi_criterion.keep_running():
        ...     multi_criterion.check_new_value(values[iterations])
        ...     iterations += 1
        ...     multi_criterion.iteration_done()
        >>> iterations
        10

    NoImprovementTerminationCriterion stops the iterating:

    .. doctest::

        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from lclpy.termination.max_iterations_termination_criterion \\
        ...     import MaxIterationsTerminationCriterion
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        >>> from lclpy.termination.multi_criterion import MultiCriterion
        ... # init list
        >>> criteria = []
        >>> criteria.append(MaxSecondsTerminationCriterion(3))
        >>> criteria.append(MaxIterationsTerminationCriterion(10))
        >>> criteria.append(NoImprovementTerminationCriterion(3))
        ... # init MultiCriterion
        >>> multi_criterion = MultiCriterion(criteria)
        ... # test 1
        >>> iterations = 0
        >>> values = [9, 8, 7, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        >>> multi_criterion.start_timing()
        >>> while multi_criterion.keep_running():
        ...     multi_criterion.check_new_value(values[iterations])
        ...     iterations += 1
        ...     multi_criterion.iteration_done()
        >>> iterations
        6


    """

    def __init__(self, criteria):
        super().__init__()
        self.criteria = criteria

    def keep_running(self):
        """function to determine if the algorithm needs to continue running.

        Returns
        -------
        bool
            The function returns true if the algorithm has to continue
            running, if the function returns false the algorithm needs to
            stop running. If one or more of the composing termination
            criterions returns False if its keep_running method is called, this
            method will return False. Else the method will return True.

        """

        for criterion in self.criteria:
            if criterion.keep_running() is False:
                return False
        return True

    def iteration_done(self):
        """function to be called after every iteration."""

        for criterion in self.criteria:
            criterion.iteration_done()

    def check_new_value(self, value):
        """Checks a value.

        Parameters
        ----------
        value : int or float
            A value from the evaluation function.

        """

        for criterion in self.criteria:
            criterion.check_new_value(value)

    def start_timing(self):
        """Starts an internal timer if needed."""

        for criterion in self.criteria:
            criterion.start_timing()

    def check_variable(self, variable):
        """Checks a variable specific to an implementation.

        Does not need to be used or implemented

        Parameters
        ----------
        variable
            The value of a certain value of a specific algorithm.

        """

        for criterion in self.criteria:
            criterion.check_variable(variable)

    def reset(self):
        """Resets the object back to it's state after init.

        Examples
        --------
         MaxIterationsTerminationCriterion stops the iterating:

        .. doctest::

            >>> from lclpy.termination.max_seconds_termination_criterion \\
            ...     import MaxSecondsTerminationCriterion
            >>> from lclpy.termination.max_iterations_termination_criterion \\
            ...     import MaxIterationsTerminationCriterion
            >>> from lclpy.termination.no_improvement_termination_criterion \\
            ...     import NoImprovementTerminationCriterion
            >>> from lclpy.termination.multi_criterion \\
            ...     import MultiCriterion
            ... # init list
            >>> criteria = []
            >>> criteria.append(MaxSecondsTerminationCriterion(3))
            >>> criteria.append(MaxIterationsTerminationCriterion(10))
            >>> criteria.append(NoImprovementTerminationCriterion(3))
            ... # init MultiCriterion
            >>> multi_criterion = MultiCriterion(criteria)
            ... # run 1
            >>> iterations = 0
            >>> values = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9]
            >>> multi_criterion.start_timing()
            >>> while multi_criterion.keep_running():
            ...     multi_criterion.check_new_value(values[iterations])
            ...     iterations += 1
            ...     multi_criterion.iteration_done()
            >>> iterations
            10
            >>> # reset
            >>> multi_criterion.reset()
            ... # run 2
            >>> iterations = 0
            >>> values = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9]
            >>> multi_criterion.start_timing()
            >>> while multi_criterion.keep_running():
            ...     multi_criterion.check_new_value(values[iterations])
            ...     iterations += 1
            ...     multi_criterion.iteration_done()
            >>> iterations
            10

        """

        for criterion in self.criteria:
            criterion.reset()
