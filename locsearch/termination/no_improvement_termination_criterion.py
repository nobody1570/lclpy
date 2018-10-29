from locsearch.termination.abstract_termination_criterion import AbstractTerminationCriterion


class NoImprovementTerminationCriterion(AbstractTerminationCriterion):
    """Criterion to terminate after a set amount of iterations without improvement.

    Attributes
    ----------
    max_iterations : int
        The maximal amount of iterations. Is normally set to 100, if you
        need it to be more or less simply change this after constructing
        the criterion.
    _iterations : int
        The amount of iterations with no improvement.
    _old_best_value: int
        The last best value.

    """

    def __init__(self):
        super().__init__()
        self.max_iterations = 100
        self._iterations = 0
        self._old_best_value = 0

    def keep_running(self):
        """function to determine if the algorithm needs to continue running

        Returns
        -------
        bool
            The function returns true if the amount of iteration is smaller
            than max_iterations, if the function returns false the amount of
            iterations is bigger than max_iterations

        """
        return self._iterations < self.max_iterations

    def iteration_done(self):
        """function to be called after every iteration

        Increments _iterations by 1 if no better value is found.

        """

        self._iterations += 1

    def check_new_value(self, value):
        if value > self._old_best_value:
            self._iterations = 0
            self._old_best_value = value
