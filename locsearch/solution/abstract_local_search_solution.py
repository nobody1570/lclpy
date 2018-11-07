from abc import ABC, abstractmethod


class AbstractLocalSearchSolution(ABC):
    """Template to create Solution-classes for localsearch implemenatations.

    This Class is meant to be used as a template.
    It is supposed to be used when constructing a heuristic to solve
    localsearch problems.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def move(self):
        """Performs a move on data.

        The neighbourhood is explored and the current solution is changed to a
        new solution. move_function is used and the data variable is changed.

        """
        pass


