"""This package contains all the functions and classes needed for
delta-evaluation.

The easiest and fastest way to implement delta evaluation for new classes and
moves is to implement delta_evaluate in the evaluation function for a specific
evaluation-move class pair. The limitations of this approach are
obvious.

Alternatively, one can define it's own function that acts like delta_eval_func.
Obviously, one would need to use this function in the __init__ of your
evaluation classes instead of delta_eval_func. This means that the evaluation
functions defined by the library would need to be subclassed and given a
different __init__ method to be compatible with your function. The best way to
make your function use the already existing functionality would be like this:

.. code-block:: python

    def my_delta_eval_func(problem_eval_func, move_func):

        try:
            # try using existing functionality
            return delta_eval_func(problem_eval_func, move_func)

        except NotImplementedError:
            # a NotImplementedError was raised, so we know that delta_eval_func
            # couldn't find an implementation for a specific pair.

            # return of delta evaluation class for added classes you have
            # implemented
            return my_other_func(problem_eval_func, move_func)

Note that it might be possible to reuse classes, functions and code from
modules delta_qap, delta_tsp and delta_multi_neighbourhood.

"""
