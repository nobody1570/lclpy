from abc import ABC, abstractmethod


class AbstractCoolingFunction(ABC):
    """A class that implements a cooling function for simulated annealing."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def next_temperature(self, old_temperature):
        """Function to get the next temperature

        Parameters
        ----------
        old_temperature : int or float
            The old temperature

        Returns
        -------
        int or float
            The new temperature

        """
        pass
