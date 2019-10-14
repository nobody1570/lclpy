from lclpy.localsearch.acceptance.abstract_acceptance_function \
    import AbstractAcceptanceFunction
import random
import math


class SimulatedAnnealingAcceptanceFunction(AbstractAcceptanceFunction):
    """An acceptance function for simulated annealing.

    A smaller quality value is assumed to be better than a bigger one.

    Parameters
    ----------
    diff_multiplier : int or float, optional
        The delta_value will be multiplied by this multiplier. A bigger value
        leads to more solutions being accepted, while a smaller value will
        lead to less solutions being accepted.
        Positive values will initialise the class for minising, negative values
        will intialise the function for maximising.
        The default value is 1.
    multiplier : int or float, optional
        Will be multiplied with the whole probability. Must be positive.
        Should be in the interval ]0,1]. This multiplier can be used to
        decrease the odds of values being accepted. While it is possible to use
        a multiplier greater than 1, this might cause weird behaviour.
        The default value is 1.

    Attributes
    ----------
    _diff_multiplier : int or float
        The delta_value will be multiplied by this multiplier.
    _multiplier : int or float
        Is multiplied with the whole probability.

    Examples
    --------
    A simple example of the default behaviour, delta (200) and
    temperature (1000) are arbitrarily chosen, they have little meaning in
    this example:

    .. doctest::

        >>> import random
        >>> from lclpy.localsearch.acceptance.simulated_annealing_acceptance_function \\
        ...     import SimulatedAnnealingAcceptanceFunction
        ... # set seed of random
        ... # this isn't needed, it's only used to make sure the results will
        ... # always be the same.
        >>> random.seed(2)
        ... # init
        >>> test = SimulatedAnnealingAcceptanceFunction()
        ... # tests
        >>> test.accept(200, 1000)
        False
        >>> test.accept(200, 1000)
        False
        >>> test.accept(200, 1000)
        True
        >>> test.accept(200, 1000)
        True
        >>> test.accept(200, 1000)
        False

    """

    def __init__(self, diff_multiplier=1, multiplier=1):
        super().__init__()

        self._diff_multiplier = diff_multiplier
        self._multiplier = multiplier

    def accept(self, delta_value, temperature):
        """Function to reject or accept certain potential solutions.

        In most cases, a value better than the current value will always be
        accepted. When this is the case, it might be wise to use an
        if-statement to handle those instead of passing them to this method.

        The chance of a state being accepted is equal to:

        .. math::

            \\_multiplier*e^{\\dfrac{\\_diff\\_multiplier*delta\\_value}{temperature}}

        .. The formula:
           _multiplier*e^(-(_diff_multiplier*delta_value)/temperature)

        Parameters
        ----------
        delta_value : int or float
            The difference in quality between 2 possible solutions.
        temperature : int or float
            A value that determines the chance of a state being accepted.
            How bigger this value, how higher the chance of a solution being
            accepted.

        Returns
        -------
        bool
            True if the solution is accepted, False if the solution isn't
            accepted.

        """

        # calculate probability
        probability = self._multiplier * \
            math.exp(-(self._diff_multiplier * delta_value) / temperature)

        # generates a random number in the interval [0, 1[
        random_number = random.random()

        return probability > random_number
