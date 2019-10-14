from abc import ABC, abstractmethod


class AbstractAcceptanceFunction(ABC):
    """Template to create acceptance functions.

    Acceptance functions determine if a worse state than the current
    state is accepted as the new current state.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def accept(self, delta_value):
        """Checks if the worse state will be accepted

        Parameters
        ----------
        delta_value : int or float
            The difference in quality between the current state and the
            potential new state. This can be calculated by substracting the
            quality of the current state from the quality of the potential new
            state.

        Returns
        -------
        bool
            The function returns true if the problem is accepted,
            the function returns false if the problem is rejected.

        """
        pass
