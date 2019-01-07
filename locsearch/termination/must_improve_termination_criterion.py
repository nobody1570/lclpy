from locsearch.termination.abstract_termination_criterion \
    import AbstractTerminationCriterion
from aidfunc.is_improvement_func import bigger, smaller


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
    Bigger values are considered improvements(default). 5 iterations with
    improvement. After that there are no more improvements. The dataset
    eval_values is hardcoded:

    .. doctest::

        >>> import numpy
        >>> from locsearch.termination.must_improve_termination_criterion \\
        ...     import MustImproveTerminationCriterion
        ... # creation of an array that contains the values that will be given
        ... # to our termination criterion
        >>> eval_values = numpy.array([0, 2, 14, 15, 20, 3, 3, 4, 2, 1, 0, 12])
        ... # index is used to get values from the array.
        ... # index is also used to count the amount of iterations
        >>> index = 0
        ... # init
        >>> test = MustImproveTerminationCriterion()
        ... # loop
        >>> while test.keep_running():
        ...     pass # other code to execute
        ...     # check the next value
        ...     # not_used is only used to suppress the output of
        ...     # check_new_value
        ...     not_used = test.check_new_value(eval_values[index])
        ...     pass # other code to execute
        ...     # counting iterations + increment index
        ...     index += 1
        >>> index # == amount of iterations.
        6

    Smaller values are considered improvements. 8 iterations with
    improvement. After that there are no more improvements. The dataset
    eval_values is hardcoded:

    .. doctest::

        >>> import numpy
        >>> from locsearch.termination.must_improve_termination_criterion \\
        ...     import MustImproveTerminationCriterion
        ... # creation of an array that contains the values that will be given
        ... # to our termination criterion
        >>> eval_values = numpy.array([10, 9, 8, 7, 6, 5, 4, 3, 4, 3, 5, 12])
        ... # index is used to get values from the array.
        ... # index is also used to count the amount of iterations
        >>> index = 0
        ... # init
        >>> test = MustImproveTerminationCriterion(False)
        ... # loop
        >>> while test.keep_running():
        ...     pass # other code to execute
        ...     # check the next value
        ...     # not_used is only used to suppress the output of
        ...     # check_new_value
        ...     not_used = test.check_new_value(eval_values[index])
        ...     pass # more code to execute
        ...     # counting iterations + increment index
        ...     index += 1
        >>> index # == amount of iterations.
        9



    """

    def __init__(self, improvement_is_bigger=True):
        super().__init__()

        # init
        self._run = True

        # choose intial _old_best_value value + pick judge function
        if improvement_is_bigger:
            self._function = bigger
            self._old_best_value = float("-inf")
        else:
            self._function = smaller
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

        Returns
        -------
        bool
            The function returns True if the value is an improvement, else it
            returns False.

        """

        check = self._function(self._old_best_value, value)
        if check:
            self._old_best_value = value
        else:
            self._run = False

        return check
