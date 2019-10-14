from abc import ABC, abstractmethod


class AbstrIterationsTempFunction(ABC):
    """Template class for determining the number of iterations for a temperature.

    Implementations of this class are meant to be used in a simulated annealing
    algorithm. Implementations are supposed to be used to determine the amount
    of iterations for a certain temperature.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_iterations(self, temperature):
        """Returns the amount of iterations for a certain temperature.

        Parameters
        ----------
        Temperature : int or float
            The current temperature.

        """

        pass
