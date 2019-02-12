from locsearch.evaluation.deltaeval.delta_tsp import delta_tsp
from locsearch.evaluation.deltaeval.delta_qap import delta_qap


def delta_eval_func(problem_eval_func, move_func):
    """A function to retrieve the functions needed for delta evaluation.

    Parameters
    ----------
    problem_eval_func : AbstractEvaluationFunction
        The used evaluation function.
    move_type : AbstractMove
        The used move type.

    Returns
    -------
    delta_evaluate
        A function that can be used for the delta evaluation
    changed_distances
        Aid function to determine what should be recalculated.
    transform_next_index_to_current_index
        Aid function to determine the values that need to be used in the delta
        evaluation.

    """

    problem_type = problem_eval_func.get_problem_type()
    move_type = move_func.get_move_type()

    if problem_type is 'TSP':
        return delta_tsp(problem_eval_func, move_func)
    elif problem_type is 'QAP':
        return delta_qap(problem_eval_func, move_func)
    else:
        raise NotImplementedError
