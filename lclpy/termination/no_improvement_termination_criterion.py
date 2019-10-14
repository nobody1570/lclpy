from lclpy.termination.abstract_termination_criterion \
    import AbstractTerminationCriterion
from lclpy.aidfunc.is_improvement_func import bigger, smaller


class NoImprovementTerminationCriterion(AbstractTerminationCriterion):
    """Criterion to terminate after a set amount of iterations without improvement.

    Parameters
    ----------
    max_iterations : int, optional
        The maximal amount of iterations without improvement. The default is
        100 iterations.
    minimise : bool, optional
        If the goal is to minimise the evaluation function, this should be
        True. If the goal is to maximise the evlauation function, this should
        be False. The default is True.

    Attributes
    ----------
    _max_iterations : int
        The maximal amount of iterations without improvement.
    _iterations : int
        The amount of iterations with no improvement.
    _run : bool
        Will be True if the maximal amount of iterations without improvement
        hasn't been reached yet, will be false if this isn't the case.
    _old_best_value : int
        The last best value. Is initialised as minus infinite
        (improvement_is_bigger = True)
        or infinite (improvement_is_bigger = False)
    _function : function
        The function used to judge if a value is an improvement.

    Examples
    --------
    Default amount of iterations without improvement (100), always checking
    the new value. Smaller values are considered improvements(default). The
    dataset eval_values is generated. (1 improvement, 99 cases without
    improvement, 1 improvement, 110 cases without improvement) After this the
    iterations start:

    .. doctest::

        >>> import numpy
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        ... # creation of an array that contains the values that will be given
        ... # to our termination criterion
        >>> eval_values = numpy.concatenate(
        ...     (numpy.array([1000]), numpy.random.randint(1000,2000, size=98),
        ...      numpy.array([20]), numpy.random.randint(20,40, size=110)))
        ... # index is used to get values from the array.
        ... # index is also used to count the amount of iterations
        >>> index=0
        ... # init
        >>> test = NoImprovementTerminationCriterion()
        ... # loop
        >>> while test.keep_running():
        ...     pass # other code to execute
        ...     # check the next value
        ...     test.check_new_value(eval_values[index])
        ...     pass # other code to execute
        ...     # counting iterations + increment index
        ...     index += 1
        ...     test.iteration_done()
        >>> index # == amount of iterations.
        200

    3 iterations without improvement, only checking improved values. Smaller
    values are considered improvements(default). The dataset eval_values is
    hardcoded:

    .. doctest::

        >>> import numpy
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        ... # creation of an array that contains the values that will be given
        ... # to our termination criterion
        >>> eval_values = numpy.array([20, 19, 21, 22, 23, 3])
        ... # index is used to get values from the array.
        ... # index is also used to count the amount of iterations
        >>> index = 0
        ... # old value is the last encountered best value
        >>> old_value = -1
        ... # init
        >>> test = NoImprovementTerminationCriterion(3)
        ... # loop
        >>> while test.keep_running():
        ...     pass # other code to execute
        ...     # only check next value if it's better than the last best value
        ...     if eval_values[index] > old_value:
        ...         old_value = eval_values[index]
        ...         test.check_new_value(eval_values[index])
        ...     pass # other code to execute
        ...     # counting iterations + increment index
        ...     index += 1
        ...     test.iteration_done()
        >>> index # == amount of iterations.
        4

    Default amount of iterations without improvement (100). Bigger values are
    considered improvements. The dataset eval_values is generated.
    (1 improvement, 99 cases without improvement, 1 improvement, 110 cases
    without improvement) After this the iterations start:

    .. doctest::

        >>> import numpy
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        ... # creation of an array that contains the values that will be given
        ... # to our termination criterion
        >>> eval_values = numpy.concatenate(
        ...     (numpy.array([2]), numpy.random.randint(3, size=98),
        ...      numpy.array([5]), numpy.random.randint(6, size=110)))
        ... # index is used to get values from the array.
        ... # index is also used to count the amount of iterations
        >>> index=0
        ... # init
        >>> test = NoImprovementTerminationCriterion(minimise=False)
        ... # loop
        >>> while test.keep_running():
        ...     pass # other code to execute
        ...     # check next value
        ...     test.check_new_value(eval_values[index])
        ...     pass # other code to execute
        ...     # counting iterations + increment index
        ...     index += 1
        ...     test.iteration_done()
        >>> index # == amount of iterations.
        200

    3 iterations without improvement. Bigger values are considered
    improvements. The dataset eval_values is hardcoded:

    .. doctest::

        >>> import numpy
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        ... # creation of an array that contains the values that will be given
        ... # to our termination criterion
        >>> eval_values = numpy.array([0, 0, 2, 1, 3, 3, 3, 4, 2, 1, 0, 12])
        ... # index is used to get values from the array.
        ... # index is also used to count the amount of iterations
        >>> index = 0
        ... # init
        >>> test = NoImprovementTerminationCriterion(3, False)
        ... # loop
        >>> while test.keep_running():
        ...     pass # other code to execute
        ...     # check next value
        ...     test.check_new_value(eval_values[index])
        ...     pass # other code to execute
        ...     # counting iterations + increment index
        ...     index += 1
        ...     test.iteration_done()
        >>> index # == amount of iterations.
        11




    """

    def __init__(self, max_iterations=100, minimise=True):
        super().__init__()

        # init
        self._max_iterations = max_iterations
        self._iterations = 0
        self._run = True

        # choose intial _old_best_value value + pick judge function
        if minimise:
            self._function = smaller
            self._old_best_value = float("inf")
        else:
            self._function = bigger
            self._old_best_value = float("-inf")

    def keep_running(self):
        """Function to determine if the algorithm needs to continue running.

        Returns
        -------
        bool
            The function returns true if the amount of iterations is smaller
            than _max_iterations, if the function returns false the amount of
            iterations is bigger than max_iterations

        """
        return self._run

    def iteration_done(self):
        """Function to be called after every iteration.

        Increments _iterations by 1.

        """

        self._iterations += 1

        if self._iterations == self._max_iterations:
            self._run = False

    def check_first_value(self, value):
        """Function that should be called once before the main loop.

        Parameters
        ----------
        value : int or float
            Is the evaluation value of the initial solution.

        """

        self._old_best_value = value

    def check_new_value(self, value):
        """Function to be called after every improvement of the evaluation function.

        It's also possible to call this function every time when the
        evaluation value is calculated without ill effects.

        Parameters
        ----------
        value : int or float
            Is the best evaluation value found for a solution or the new
            evaluation value of a solution. It does not matter which one is
            used.

        """
        if self._function(self._old_best_value, value):
            self._iterations = -1
            self._old_best_value = value

    def reset(self):
        """Resets the object back to it's state after init.

        Examples
        --------

        3 iterations without improvement. Bigger values are considered
        improvements. The dataset eval_values is hardcoded. After this, the
        criterion is resetted and the loop is repeated:

        .. doctest::

            >>> import numpy
            >>> from lclpy.termination.no_improvement_termination_criterion \\
            ...     import NoImprovementTerminationCriterion
            ... # creation of an array that contains the values that will be
            ... #  given to our termination criterion
            >>> eval_values = numpy.array(
            ...     [0, 0, 2, 1, 3, 3, 3, 4, 2, 1, 0, 12])
            ... # init
            >>> test = NoImprovementTerminationCriterion(3, False)
            ... # run 1
            ... #
            ... # index is used to get values from the array.
            ... # index is also used to count the amount of iterations
            >>> index = 0
            ... # loop
            >>> while test.keep_running():
            ...     pass # other code to execute
            ...     # check next value
            ...     test.check_new_value(eval_values[index])
            ...     pass # other code to execute
            ...     # counting iterations + increment index
            ...     index += 1
            ...     test.iteration_done()
            >>> index # == amount of iterations.
            11
            >>> # reset
            >>> test.reset()
            ... # run 2
            >>> index = 0
            ... # loop
            >>> while test.keep_running():
            ...     pass # other code to execute
            ...     # check next value
            ...     test.check_new_value(eval_values[index])
            ...     pass # other code to execute
            ...     # counting iterations + increment index
            ...     index += 1
            ...     test.iteration_done()
            >>> index # == amount of iterations.
            11

        """

        self._run = True
        self._iterations = 0

        # restore old_best value
        if self._function is smaller:
            # if minimising
            self._old_best_value = float("inf")
        else:
            # if maximising
            self._old_best_value = float("-inf")
