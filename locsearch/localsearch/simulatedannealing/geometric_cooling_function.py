from locsearch.localsearch.simulatedannealing.abstract_cooling_function import AbstractCoolingFunction


class GeometricCoolingFunction(AbstractCoolingFunction):
    """Implements a geometric cooling function for simulated annealing.

    Parameters
    ----------
    alpha : float
        A parameter that influences the cooling rate. Should be a positive
        number smaller than 1.

    Attributes
    ----------
    _alpha : float
        A parameter that influences the cooling rate.

    Examples
    --------
    A simple example:

    .. doctest::

        >>> from locsearch.localsearch.simulatedannealing.geometric_cooling_function import GeometricCoolingFunction
        >>> import math
        >>> test = GeometricCoolingFunction()
        >>> temperature = 1000
        >>> test.next_temperature(1000)
        750.0

    An example with an alpha of 0.5:

    .. doctest::

        >>> from locsearch.localsearch.simulatedannealing.geometric_cooling_function import GeometricCoolingFunction
        >>> import math
        >>> test = GeometricCoolingFunction(0.5)
        >>> temperature = 1000
        >>> test.next_temperature(1000)
        500.0

    """

    def __init__(self, alpha=0.75):
        super().__init__()
        self._alpha = alpha

    def next_temperature(self, old_temperature):
        """Function to get the next temperature

        Parameters
        ----------
        old_temperature : int or float
            The old temperature

        Returns
        -------
        float
            The new temperature. This temperature is _alpha*old_temperature.

        """
        return self._alpha*old_temperature
