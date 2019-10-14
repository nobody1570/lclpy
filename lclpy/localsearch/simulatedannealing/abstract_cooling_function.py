from abc import ABC, abstractmethod


class AbstractCoolingFunction(ABC):
    """A template class to implement a cooling function for simulated annealing.

    Implementations of this class are meant to be used in a simulated annealing
    algorithm. Implementations are supposed to implement the cooling function.

    """

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
