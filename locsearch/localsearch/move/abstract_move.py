from abc import ABC, abstractmethod


class AbstractMove(ABC):
    """Template to create Move-objects.def

    This object is used to explore new Solutons in a neighbourhood.
    """

    def __init__(self):
        super(AbstractMove, self).__init__()

    @abstractmethod
    def move(data):
        """performs a move

        Parameters
        ----------
        data
            The dataset that is being explored. =It will be altered after the
            method call.

        """
        pass
