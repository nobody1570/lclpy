from locsearch.termination.abstract_termination_criterion import AbstractTerminationCriterion


class MustImproveTerminationCriterion(AbstractTerminationCriterion):
    """Criterion to terminate after an iteration without improvement.

    Parameters
    ----------
    improvement_is_bigger : bool
        If the improvement_is_bigger is True, bigger values will be considered
        improvements. If the improvement_is_bigger is False, smaller values
        will be considered improvements. The default is True.

    Attributes
    ----------
    _old_best_value: int
        The last value. Is initialised as minus infinite
        (improvement_is_bigger = True)
        or infinite (improvement_is_bigger = False)
    _function : function
        The function used to judge if a value is an improvement.
    _run : bool
        True if no worse value has been encountered, False if this isn't the
        case.

    Examples
    --------
    Bigger values are considered improvements. (default) 5 iterations with
    improvement. After that there are no more improvements.The dataset
    eval_values is hardcoded:

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

    Smaller values are considered improvements. 8 iterations with
    improvement. After that there are no more improvements.The dataset
    eval_values is hardcoded:

    .. doctest::

            >>> import numpy
            >>> from locsearch.termination.must_improve_termination_criterion import MustImproveTerminationCriterion
            >>> eval_values = numpy.array([10, 9, 8, 7, 6, 5, 4, 3, 4, 3, 5, 12])
            >>> index = 0
            >>> test = MustImproveTerminationCriterion(False)
            >>> while test.keep_running():
            ...     pass # code to execute
            ...     test.check_new_value(eval_values[index])
            ...     pass # more code to execute
            ...     index += 1 # counting iterations + index
            >>> index # Amount of iterations.
            9



    """

    def _bigger_is_improvement(self, value):
        """Checks if a value is an improvement. Bigger values are improvements.

        Parameters
        ----------
        value : int or float
            The value that is checked.

        Returns
        -------
        bool
            Returns true if the current value is bigger than the best old
            value, else returns false.

        """
        return value > self._old_best_value

    def _smaller_is_improvement(self, value):
        """Checks if a value is an improvement. Smaller values are improvements.

        Parameters
        ----------
        value : int or float
            The value that is checked.

        Returns
        -------
        bool
            Returns true if the current value is smaller than the best old
            value, else returns false.

        """
        return value < self._old_best_value

    def __init__(self, improvement_is_bigger=True):
        super().__init__()

        self._run = True

        if improvement_is_bigger:
            self._function = self._bigger_is_improvement
            self._old_best_value = float("-inf")
        else:
            self._function = self._smaller_is_improvement
            self._old_best_value = float("inf")

    def keep_running(self):
        """function to determine if the algorithm needs to continue running

        Returns
        -------
        bool
            The function returns True if there hasn't been encountered a
            non-improving value. The function returns False if a non-improving
            value is encountered.
        """
        return self._run

    def check_new_value(self, value):
        """function to be called after every calculation of the evaluation function.

        Parameters
        ----------
        value : int or long or float
            Is the new evaluation value of a solution.

        """
        if self._function(value):
            self._old_best_value = value
        else:
            self._run = False
