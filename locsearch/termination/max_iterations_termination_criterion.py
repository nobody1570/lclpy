from locsearch.termination.abstract_termination_criterion import AbstractTerminationCriterion


class MaxIterationsTerminationCriterion(AbstractTerminationCriterion):
    """Termination criterion that terminates after a set amount of iterations.

    Attributes
    ----------
    max_iterations : int
        The maximal amount of iterations. Is normally set to 1000, if you
        need it to be more or less simply change this after constructing
        the criterion.
    _iterations : int
        The amount of iterations.

    """

    def __init__(self):
        super().__init__()
        self.max_iterations = 1000
        self._iterations = 0

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

        Increments _iteration by 1.
        """
        self._iterations += 1
