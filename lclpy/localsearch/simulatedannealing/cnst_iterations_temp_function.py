from lclpy.localsearch.simulatedannealing.abstr_iterations_temp_function \
    import AbstrIterationsTempFunction


class CnstIterationsTempFunction(AbstrIterationsTempFunction):
    """Class for determining the number of iterations for a temperature.

    This class is meant to be used in a simulated annealing algorithm.
    The amount of iterations is constant and is not influenced by the
    temperature.

    Parameters
    ----------
    iterations : int
        The amount of iterations for all temperatures.

    Attributes
    ----------
    _iterations : int
        The amount of iterations for all temperatures. Default is 1000.

    Examples
    --------
    Default behaviour:

    .. doctest::

        >>> from lclpy.localsearch.simulatedannealing.cnst_iterations_temp_function \\
        ...     import CnstIterationsTempFunction
        ... # init
        >>> test = CnstIterationsTempFunction()
        ... # tests
        >>> test.get_iterations(1000)
        1000
        >>> test.get_iterations(359)
        1000
        >>> test.get_iterations(0)
        1000

    With 800 iterations:

    .. doctest::

        >>> from lclpy.localsearch.simulatedannealing.cnst_iterations_temp_function \\
        ...     import CnstIterationsTempFunction
        ... # init
        >>> test = CnstIterationsTempFunction(800)
        ... # tests
        >>> test.get_iterations(1000)
        800
        >>> test.get_iterations(359)
        800
        >>> test.get_iterations(0)
        800

    """

    def __init__(self, iterations=1000):
        super().__init__()
        self._iterations = iterations

    def get_iterations(self, temperature):
        """Returns the amount of iterations for a certain temperature.

        Parameters
        ----------
        temperature : int or float
            The "temperature" in the simulated annealing algorithm.

        Returns
        -------
        int
            The amount of iterations for the temperature. (Here always
            _iterations)

        """

        return self._iterations
