from locsearch.termination.abstract_termination_criterion import AbstractTerminationCriterion


class MustImproveTerminationCriterion(AbstractTerminationCriterion):
    """Criterion to terminate after a set amount of iterations without improvement.


    Attributes
    ----------
    _old_best_value: int
        The last best value. Is initialised as -1.

    Examples
    --------

    5 iterations with improvement. After that there are no more
    improvements.The dataset eval_values is hardcoded:

    .. doctest::

            >>> import numpy
            >>> from locsearch.termination.must_improve_termination_criterion import MustImproveTerminationCriterion
            >>> eval_values = numpy.array([0, 2, 14, 15, 20, 3, 3, 4, 2, 1, 0, 12])
            >>> index = 0
            >>> test = MustImproveTerminationCriterion()
            >>> while test.keep_running():
            ...     pass # code to execute
            ...     test.check_new_value(eval_values[index])
            ...     pass # more code to execute
            ...     index += 1 # counting iterations + index
            >>> index # Amount of iterations.
            6



    """

    def __init__(self):
        super().__init__()
        self._old_best_value = -1
        self.run = True

    def keep_running(self):
        """function to determine if the algorithm needs to continue running

        Returns
        -------
        bool
            The function returns True if there hasn't been encountered a
            non-improving value. The function returns False if a non-improving
            value is encountered.
        """
        return self.run

    def check_new_value(self, value):
        """function to be called after every calculation of the evaluation function.

        Parameters
        ----------
        value : int or long or float
            Is the new evaluation value of a solution. Value must be positive.

        """
        if value > self._old_best_value:
            self._old_best_value = value
        else:
            self.run = False
