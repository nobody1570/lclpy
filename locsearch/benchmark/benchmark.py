from random import seed


def benchmark(problems, algorithms, stop_criterion, runs=10, seeds=None):
    """A function to perform multiple algorithms on multiple soltions.

    Parameters
    ----------
    problems : iterable object
        Contains all the problems.
    algorithms : iterable object
        Contains all the algorithms. Note that the algorithms can be
        initialised with None as solution and None as termination_criterion.
    stop_criterion : AbstractTerminationCriterion
        The termination criterion that will be used for all combinations of
        algorithms and solutions.
    runs : int, optional
        The amount of runs that will be performed for a single
        algorithm-solution pair.
    seeds : list of int or tuple of int
        The seeds that will be used in the runs. Note that the length of the
        tuple or array needs to be equal to the amount of runs.

    Returns
    -------
    List of namedtuple
        A 3-dimensional list of namedtuple. These namedtuples are the results
        of the algorithms. The first indice represents an algorithm, the second
        a problem, the third a run of the algorithm-problem pair. The indices
        that should be used are the same as in algorithms and solutions
        respectively for the first 2 indices. The third indice is used to
        choose between the runs. The possible indices for runs are always in
        the interval [0, runs-1].

    """

    if seeds is None:
        seeds = range(runs)

    results = []

    for algorithm in algorithms:

        results_single_algorithm = []

        for problem in problems:

            algorithm._problem = problem
            algorithm._termination_criterion = stop_criterion

            different_seed_results = []

            for i in seeds:
                seed(i)
                algorithm.reset()
                different_seed_results.append(algorithm.run())

            results_single_algorithm.append(different_seed_results)

        results.append(results_single_algorithm)

    return results
