from locsearch.termination.abstract_termination_criterion import AbstractTerminationCriterion
import math


class NoImprovementTerminationCriterion(AbstractTerminationCriterion):
    """Criterion to terminate after a set amount of iterations without improvement.

    Parameters
    ----------
    max_iterations : int, optional
        The maximal amount of iterations without improvement. The default is
        100 iterations.
    improvement_is_bigger : bool, optional
        If this boolean is True, values that are bigger than the previous
        values will be considered as improvements. If it is False, values that
        are smaller than the previous values wil be considered improvements.
        The default is True.

    Attributes
    ----------
    _max_iterations : int
        The maximal amount of iterations without improvement.
    _iterations : int
        The amount of iterations with no improvement.
    _old_best_value : int
        The last best value. Is initialised as minus infinite
        (improvement_is_bigger = True)
        or infinite (improvement_is_bigger = False)
    _function : function
        The function used to judge if a value is an improvement. 

    Examples
    --------
    Default amount of iterations without improvement (100), always checking
    the new value. Bigger values are considered improvements. (default) The dataset 
    eval_values is generated. (1 improvement, 99 cases without improvement,
    1 improvement, 110 cases without improvement) After this the iterations
    start:

    .. doctest::

        >>> import numpy
        >>> from locsearch.termination.no_improvement_termination_criterion import NoImprovementTerminationCriterion
        >>> eval_values = numpy.concatenate((numpy.array([2]), numpy.random.randint(3, size=98), numpy.array([5]), numpy.random.randint(6, size=110)))
        >>> index=0
        >>> test = NoImprovementTerminationCriterion()
        >>> while test.keep_running():
        ...     pass # code to execute
        ...     test.check_new_value(eval_values[index])
        ...     pass # more code to execute
        ...     index += 1 # counting iterations + index
        ...     test.iteration_done()
        >>> index # Amount of iterations.
        200

    3 iterations without improvement, only checking improved values. Bigger
    values are considered improvements. (default) The dataset eval_values is
    hardcoded:

    .. doctest::

        >>> import numpy
        >>> from locsearch.termination.no_improvement_termination_criterion import NoImprovementTerminationCriterion
        >>> eval_values = numpy.array([0, 0, 2, 1, 3, 3, 3, 4, 2, 1, 0, 12])
        >>> index = 0
        >>> old_value = -1
        >>> test = NoImprovementTerminationCriterion(3)
        >>> while test.keep_running():
        ...     pass # code to execute
        ...     if eval_values[index] > old_value:
        ...         old_value = eval_values[index]
        ...         test.check_new_value(eval_values[index])
        ...     pass # more code to execute
        ...     index += 1 # counting iterations + index
        ...     test.iteration_done()
        >>> index # Amount of iterations.
        11

    Default amount of iterations without improvement (100). Smaller values are
    considered improvements. The dataset eval_values is generated.
    (1 improvement, 99 cases without improvement, 1 improvement, 110 cases
    without improvement) After this the iterations start:

    .. doctest::

        >>> import numpy
        >>> from locsearch.termination.no_improvement_termination_criterion import NoImprovementTerminationCriterion
        >>> eval_values = numpy.concatenate((numpy.array([1000]), numpy.random.randint(1000,2000, size=98), numpy.array([20]), numpy.random.randint(20,40, size=110)))
        >>> index=0
        >>> test = NoImprovementTerminationCriterion(improvement_is_bigger=False)
        >>> while test.keep_running():
        ...     pass # code to execute
        ...     test.check_new_value(eval_values[index])
        ...     pass # more code to execute
        ...     index += 1 # counting iterations + index
        ...     test.iteration_done()
        >>> index # Amount of iterations.
        200

    3 iterations without improvement. Smaller values are considered
    improvements. The dataset eval_values is hardcoded:

    .. doctest::

        >>> import numpy
        >>> from locsearch.termination.no_improvement_termination_criterion import NoImprovementTerminationCriterion
        >>> eval_values = numpy.array([20, 19, 21, 22, 23, 3])
        >>> index = 0
        >>> old_value = -1
        >>> test = NoImprovementTerminationCriterion(3, False)
        >>> while test.keep_running():
        ...     pass # code to execute
        ...     test.check_new_value(eval_values[index])
        ...     pass # more code to execute
        ...     index += 1 # counting iterations + index
        ...     test.iteration_done()
        >>> index # Amount of iterations.
        5




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

    def __init__(self, max_iterations=100, improvement_is_bigger=True):
        super().__init__()

        self._max_iterations = max_iterations
        self._iterations = 0

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
            The function returns true if the amount of iterations is smaller
            than _max_iterations, if the function returns false the amount of
            iterations is bigger than max_iterations

        """
        return self._iterations < self._max_iterations

    def iteration_done(self):
        """function to be called after every iteration

        Increments _iterations by 1.

        """

        self._iterations += 1

    def check_new_value(self, value):
        """function to be called after every improvement of the evaluation function.

        It's also possible to call this function every time when the
        evaluation value is calculated without ill effects.

        Parameters
        ----------
        value : int or long or float
            Is the best evaluation value found for a solution or the new
            evaluation value of a solution. It does not matter which one is
            used.

        """
        if self._function(value):
            self._iterations = -1
            self._old_best_value = value
