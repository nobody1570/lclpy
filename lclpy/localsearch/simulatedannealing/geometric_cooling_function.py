from lclpy.localsearch.simulatedannealing.abstract_cooling_function \
    import AbstractCoolingFunction


class GeometricCoolingFunction(AbstractCoolingFunction):
    """Implements a geometric cooling function for simulated annealing.

    Parameters
    ----------
    alpha : float, optional
        A parameter that influences the cooling rate. Should be a positive
        number smaller than 1. Default is 0.75.

    Attributes
    ----------
    _alpha : float
        A parameter that influences the cooling rate.

    Examples
    --------
    A simple example:

    .. doctest::

        >>> from lclpy.localsearch.simulatedannealing.geometric_cooling_function \\
        ...     import GeometricCoolingFunction
        ... # init
        >>> test = GeometricCoolingFunction()
        ... # tests
        >>> test.next_temperature(1000)
        750.0
        >>> test.next_temperature(100)
        75.0
        >>> test.next_temperature(10)
        7.5

    An example with an alpha of 0.5:

    .. doctest::

        >>> from lclpy.localsearch.simulatedannealing.geometric_cooling_function \\
        ...     import GeometricCoolingFunction
        ... # init
        >>> test = GeometricCoolingFunction(0.5)
        ... # tests
        >>> test.next_temperature(1000)
        500.0
        >>> test.next_temperature(100)
        50.0
        >>> test.next_temperature(10)
        5.0

    """

    def __init__(self, alpha=0.75):
        super().__init__()
        self._alpha = alpha

    def next_temperature(self, old_temperature):
        """Function to get the next temperature.

        Parameters
        ----------
        old_temperature : int or float
            The old temperature.

        Returns
        -------
        float
            The new temperature. This temperature is equal to:

            .. math::
                \\_alpha*old\\_temperature

            .. The formula:
                _alpha*old_temperature

        """

        return self._alpha * old_temperature
