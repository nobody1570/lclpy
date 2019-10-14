from lclpy.evaluation.deltaeval.delta_multi_neighbourhood \
    import delta_multi_neighbourhood
from lclpy.evaluation.deltaeval.delta_tsp import delta_tsp
from lclpy.evaluation.deltaeval.delta_qap import delta_qap


def delta_eval_func(problem_eval_func, move_func):
    """A function to retrieve classes and functions needed for delta evaluation.

    Parameters
    ----------
    problem_eval_func : AbstractEvaluationFunction
        The used evaluation function object.
    move_type : AbstractMove
        The used move object.

    Returns
    -------
    object
        A class with a function delta_evaluate to perform delta evaluation.

    """

    problem_type = problem_eval_func.get_problem_type()
    move_type = move_func.get_move_type()

    if move_type is 'multi_neighbourhood':
        return delta_multi_neighbourhood(problem_eval_func, move_func)
    if problem_type is 'TSP':
        return delta_tsp(problem_eval_func, move_func)
    elif problem_type is 'QAP':
        return delta_qap(problem_eval_func, move_func)
    else:
        raise NotImplementedError
