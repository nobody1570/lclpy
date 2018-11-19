from locsearch.localsearch.acceptance.abstract_acceptance_function \
    import AbstractAcceptanceFunction
import random
import math


class SimulatedAnnealingAcceptanceFunction(AbstractAcceptanceFunction):
    """An acceptance function for simulated annealing.

    Parameters
    ----------
    diff_multiplier : int or float
        The delta_value will be multiplied by this multiplier. A bigger value
        leads to more solutions being accepted, while a smaller value will
        lead to less solutions being accepted. Using a negative value is
        possible, but this should only be attempted when you know what you're
        doing.
    multiplier : int or float
        Is multiplied with the whole probability. Must be positive. Should be
        in the interval ]0,1[. This multiplier can be used to decrease the
        odds of values being accepted. While it is possible to use a
        multiplier greater than 1, don't do this if you don't know what you're
        doing.

    Attributes
    ----------
    _diff_multiplier : int or float
        The delta_value will be multiplied by this multiplier.
    _multiplier : int or float
        Is multiplied with the whole probability.

    """

    def __init__(self, diff_multiplier=1, multiplier=1):
        super().__init__()

        self._diff_multiplier = diff_multiplier
        self._multiplier = multiplier

    def accept(self, delta_value, temperature):
        """Function to reject or accept certain solutions.

        The chance of a solution being accepted is
        _multiplier*e^(-(self._diff_multiplier*delta_value)/temperature).

        Parameters
        ----------
        delta_value : int or float
            The difference in quality between 2 possible solutions. This value
            should be positive. While working with negative numbers is
            possible, you'll probably will just be wasting processing power
            when making normal use of this class; Solutions will be always
            accepted after all. Only do it when you know what you're doing.
        temperature : int or float
            A value that determines the chance of a solution being accepted.
            How bigger this value, how higher the chance of a solution being
            accepted.

        Returns
        -------
        bool
            True if the solution is accepted, False if the solution isn't
            accepted.

        """

        probability = self._multiplier * \
            math.exp(-(self._diff_multiplier * delta_value) / temperature)

        # generates a random number in the interval [0, 1[
        random_number = random.random()

        return probability > random_number
