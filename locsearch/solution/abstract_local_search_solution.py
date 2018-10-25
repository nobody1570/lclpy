from abc import ABC, abstractmethod


class AbstractLocalSearchSolution(ABC):
    """Template to create Solution-classes for localsearch implemenatations.

    This Class is meant to be used as a template.
    It is supposed to be used when constructing a heuristic to solve
    localsearch problems.

    Attributes
    ----------
    data
        Contains the main datastructure needed to find the solution.
    best_solution : AbstractLocalsearchSolution`
        Is used to remember the best solution found.
    move_function : AbstractMove
        Defines the move function used for the problem.
    evaluation_function : AbstractEvaluation
        Defines the evaluation function used for the problem

    """

    data = None
    best_solution = None
    move_function = None
    evaluation_function = None

    def __init__(self):
        super().__init__()

    # TODO check copy methods python --> needs to be fast
    # perhap altering an existing object might be better
    @abstractmethod
    def copy(Solution):
        """copy method

        Returns
        -------
        AbstractLocalSearchSolution
            deep copy of the object

        """
        pass

    @abstractmethod
    def move(self):
        """Performs a move on data.

        The neighbourhood is explored and the current solution is changed to a
        new solution. move_function is used and the data variable is changed.

        """
        pass

    @abstractmethod
    def evaluate(self):
        """Evaluates the current solution

        Returns
        -------
        int or float
            The value of the evaluation function for the current solution.

        """

        pass
