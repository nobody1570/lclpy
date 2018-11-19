from abc import ABC, abstractmethod


class AbstrIterationsTempFunction(ABC):
    """Class for determining the number of iterations for a temperature.

    This class is meant to be used in a simulated annealing algorithm.
    It is used to determine the amount of iterations for a certain temperature.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_iterations(self):
        """Returns the amount of iterations for a certain temperature."""

        pass
