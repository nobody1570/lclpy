

def benchmark(solutions, algorithms, stop_criterion):
    """A function to perform multiple algorithms on multiple soltions.

    Parameters
    ----------
    solutions : iterable object
        Contains all the solutions.
    algorithms : iterable object
        Contains all the algorithms. Note that the algorithms can be
        initialised with None as solution and None as termination_criterion.
    stop_criterion : AbstractTerminationCriterion
        The termination criterion that will be used for all combinations of
        algorithms and solutions.

    Returns
    -------
    List of namedtuple
        A 2-dimensional list of namedtuple. These namedtuples are the results
        of the algorithms. The first indice represents an algoritm, the second
        a solution. The indices that should be used are the same as in
        algorithms and solutions respectively.

    """

    results = []

    for algorithm in algorithms:

        results_single_algorithm = []

        for solution in solutions:

            algorithm._solution = solution
            algorithm._termination_criterion = stop_criterion
            algorithm.reset()
            results_single_algorithm.append(algorithm.run())

        results.append(results_single_algorithm)

    return results
