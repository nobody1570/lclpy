from locsearch.aidfunc.error_func import _not_implemented

from locsearch.localsearch.simulatedannealing.simulated_annealing \
    import SimulatedAnnealing
from locsearch.localsearch.steepestdescent.steepest_descent \
    import SteepestDescent
from locsearch.localsearch.tabusearch.tabu_search import TabuSearch

from locsearch.localsearch.simulatedannealing.geometric_cooling_function \
    import GeometricCoolingFunction
from locsearch.localsearch.simulatedannealing.cnst_iterations_temp_function \
    import CnstIterationsTempFunction


def get_init_algorithm(algorithm_type, solution, termination_criterion,
                       minimise, dictionary):
    """Aid func to return initialised algorithm object.

    Currently only 3 algorithm_types are supported:

    +---------------------+---------------------+
    | Algorithm           | algorithm_type      |
    +=====================+=====================+
    | simulated annealing | simulated_annealing |
    +---------------------+---------------------+
    | steepest descent    | steepest_descent    |
    +---------------------+---------------------+
    | tabu search         | tabu_search         |
    +---------------------+---------------------+

    Parameters
    ----------
    algorithm_type : str
        The name of the algorithm type.
    solution : AbstractLocalSearchSolution
        The object that contains all problem-specific data.
    termination_criterion : AbstractTerminationCriterion
        The termination criterion that should be used.
    minimise : bool
        Should be True when one wishes to minimise the evaluation function,
        should be False when one wishes to maximise the evaluation function.
    dictionary : dict
        Contains optional parameters for the initialisation. These parameters
        differ for different algorithm types. A default value will be used if
        these parameters are absent.

        #. simulated_annealing:

            * alpha : float
                Cooling speed. Should be between 0 and 1.
                (A geometric cooling function is used.)
            * iterations_temp : int
                Amount of iterations for a certain temperature.
            * start_temperature : int
                The start temperature.

        #. steepest_descent:
            No optional parameters exist.

        #. tabu_search:

            * tabu_list_length : int
                The length of the tabu list.

    Returns
    -------
    AbstractLocalSearch
        The wanted localsearch object. If the type is not found, a function
        that raises an NotImplementedError will be returned.

    """

    if algorithm_type is 'simulated_annealing':

        if 'alpha' in dictionary:
            alpha = dictionary['alpha']
        else:
            alpha = 0.75

        if 'iterations_temp' in dictionary:
            iterations = dictionary['iterations_temp']
        else:
            iterations = 1000

        if 'start_temperature' in dictionary:
            start_temperature = dictionary['start_temperature']
        else:
            start_temperature = 2000

        # init cooling_function
        cooling_function = GeometricCoolingFunction(alpha)

        # init iterations_for_temp_f
        iterations_for_temp_f = CnstIterationsTempFunction(iterations)

        return SimulatedAnnealing(solution, termination_criterion,
                                  cooling_function, iterations_for_temp_f,
                                  start_temperature, minimise)

    elif algorithm_type is 'steepest_descent':

        return SteepestDescent(solution, minimise, termination_criterion)

    elif algorithm_type is 'tabu_search':

        if 'tabu_list_length' in dictionary:
            return TabuSearch(solution, termination_criterion,
                              dictionary['tabu_list_length'], minimise)
        else:
            return TabuSearch(solution, termination_criterion,
                              minimise=minimise)

    else:
        return _not_implemented
