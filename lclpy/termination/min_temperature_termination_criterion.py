from lclpy.termination.abstract_termination_criterion \
    import AbstractTerminationCriterion


class MinTemperatureTerminationCriterion(AbstractTerminationCriterion):
    """A termination criterion for use with a simulated annealing algorithm.

    This termination criterion ends the algorithm if the current temperature
    is lower than the minimal temperature.

    Parameters
    ----------
    min_temperature : int, optional
        The minimal temperature. The default is 10.

    Attributes
    ----------
    min_temperature : int
        The minimal temperature.
    _run : bool
        True if no temperature lower than the minimal has been encountered,
        False if a temperature lower than the minimal has been encountered.

    Examples
    --------
    A simple example of the default behaviour:

    .. doctest::

        >>> from lclpy.termination.min_temperature_termination_criterion \\
        ...     import MinTemperatureTerminationCriterion
        ... # init
        >>> test = MinTemperatureTerminationCriterion()
        ... # tests
        >>> test.keep_running()
        True
        >>> test.check_variable(1000.0)
        >>> test.keep_running()
        True
        >>> test.check_variable(10.0)
        >>> test.keep_running()
        True
        >>> test.check_variable(9.0)
        >>> test.keep_running()
        False
        >>> test.keep_running()
        False

    Example with a minimal temperature of 100:

    .. doctest::

        >>> from lclpy.termination.min_temperature_termination_criterion \\
        ...     import MinTemperatureTerminationCriterion
        ... # init
        >>> test = MinTemperatureTerminationCriterion(100)
        ... # tests
        >>> test.keep_running()
        True
        >>> test.check_variable(1000.0)
        >>> test.keep_running()
        True
        >>> test.check_variable(100.0)
        >>> test.keep_running()
        True
        >>> test.check_variable(10.0)
        >>> test.keep_running()
        False

    """

    def __init__(self, min_temperature=10):
        super().__init__()
        self._min_temperature = min_temperature
        self._run = True

    def keep_running(self):
        """function to determine if the algorithm needs to continue running.

        Returns
        -------
        bool
            The function returns true if the current temperature is higher than
            or equal to the minimal temperature, else it returns false.

        """

        return self._run

    def check_variable(self, current_temperature):
        """Checks if the current temperature is lower than the minimal temperature.

        This function should always be called if the temperature is lowered.

        Parameters
        ----------
        current_temperature : int or float
            The current temperature of the algorithm.

        """

        if self._run:
            self._run = current_temperature >= self._min_temperature

    def reset(self):
        """Resets the object back to it's state after init.

        Examples:

        A simple example with the default min_temperature:

        .. doctest::

            >>> from lclpy.termination.min_temperature_termination_criterion \\
            ...     import MinTemperatureTerminationCriterion
            ... # init
            >>> test = MinTemperatureTerminationCriterion()
            ... # run 1
            >>> test.keep_running()
            True
            >>> test.check_variable(1000.0)
            >>> test.keep_running()
            True
            >>> test.check_variable(10.0)
            >>> test.keep_running()
            True
            >>> test.check_variable(9.0)
            >>> test.keep_running()
            False
            >>> test.keep_running()
            False
            >>> # reset
            >>> test.reset()
            ... # run 2
            >>> test.keep_running()
            True
            >>> test.check_variable(1000.0)
            >>> test.keep_running()
            True
            >>> test.check_variable(10.0)
            >>> test.keep_running()
            True
            >>> test.check_variable(9.0)
            >>> test.keep_running()
            False
            >>> test.keep_running()
            False


        """

        self._run = True
