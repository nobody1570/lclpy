from locsearch.evaluation.deltaeval.delta_tsp import delta_tsp

from locsearch.aidfunc.error_func import _not_implemented


def delta_eval_func(problem_type, move_type):
    """A function to retrieve the functions needed for delta evaluation.

    Parameters
    ----------
    problem_type : str
        The problem type.
    move_type : str
        The move type.

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

    if problem_type is 'TSP':
        return delta_tsp(move_type)
    else:
        return (_not_implemented, _not_implemented)
