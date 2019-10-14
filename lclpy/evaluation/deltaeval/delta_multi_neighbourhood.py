"""This module contains the classes and functions for delta-evaluation with a
MultiNeighbourhood.

"""


# class for multi neighbourhood delta evaluation

class MultiMoveDeltaEvaluate():
    """Class to perform delta evaluation with a MultiNeighbourhood.

    Parameters
    ----------
    problem_eval_func : AbstractEvaluationFunction
        The used evaluation function object.
    move_type : MultiNeighbourhood
        The used move object.

    Attributes
    ----------
    delta_eval_classes : tuple or list
        Contains the classes used to perform delta evaluation for each
        move type.
    delta_evaluation_func : tuple or list
        Contains the functions of the classes in delta_eval_classes that are
        called when delta-evaluation is performed.

    """

    def __init__(self, eval_func, move_func):
        # import is here because of circular dependency.
        from lclpy.evaluation.deltaeval.delta_eval_func \
            import delta_eval_func

        self.delta_eval_classes = []

        for move in move_func._move_func_list:
            self.delta_eval_classes.append(delta_eval_func(eval_func, move))

        self.delta_eval_classes = tuple(self.delta_eval_classes)

        self.delta_evaluation_func = []

        for instance in self.delta_eval_classes:
            self.delta_evaluation_func.append(instance.delta_evaluate)

        self.delta_evaluation_func = tuple(self.delta_evaluation_func)

    def delta_evaluate(self, current_order, move):

        return self.delta_evaluation_func[move[0]](current_order, move[1])


# The method to return the class

def delta_multi_neighbourhood(eval_func, move_func):
    """Returns delta-eval class for a problem with a multi-neighbourhood.

    Note that if no methods for a move or the evaluation function can be found,
    that a placeholder method will be used. The placeholder methods will raise
    a NotImplementedError when called.

    Parameters
    ----------
    eval_func : AbstractEvaluationFunction
        The used evaluation function.
    move_func : AbstractMove
        The used move function.

    Returns
    -------
    MultiMoveDeltaEvaluate
        Class useable for delta evaluation of TSP problems.

    """

    return MultiMoveDeltaEvaluate(eval_func, move_func)
