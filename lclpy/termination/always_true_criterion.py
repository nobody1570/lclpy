from lclpy.termination.abstract_termination_criterion \
    import AbstractTerminationCriterion


class AlwaysTrueCriterion(AbstractTerminationCriterion):
    """Termination criterion that will never terminate an algorithm.

    This criterion is only meant to be used as a default termination criterion
    in algorithms that will stop iterating when no improvement is found. Don't
    use it in any other case.

    """

    def __init__(self):
        super().__init__()

    def keep_running(self):
        """function to determine if the algorithm needs to continue running.

        Returns
        -------
        bool
            Will always be True.

        """

        return True

    def reset(self):
        """Resets the object back to it's state after init."""

        pass
