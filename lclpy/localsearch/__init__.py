"""This package contains the classes and packages related to localsearch.

- acceptance : package for acceptance functions
- move : package for move functions

Local search algorithms:

- simulatedannealing : package for everything unique to simulated annealing
- steepestdescent : package for everything unique to steepest descent
- tabusearch : package for everything unique to tabu search
- vns : package for everything unique to variable neighbourhood search (VNS)

Note that all the local search algorithms use delta-evaluation.
If your evaluation function does not have it implemented, errors will be
raised.

When using moves and evaluation functions implemented by this library delta
evaluation can be easily enabled, by passing the move function as a parameter
to the evaluation function:

.. code-block:: python

    move = ImplementedMove(size)
    eval_func = \\
    ImplementedEvaluationFunction(parameter_1, parameter_2, move_function=move)

Note that the evaluation function might have less or more parameters than in
this example.

You can find information how to implement your own delta evaluation in the
docstring of lclpy.evaluation.deltaeval.__init__ or in the documentation of
lclpy.evaluation.deltaeval.

If you don't feel like implementing delta_evaluation for your own evaluation
and or move classes, for whatever reason, you can always do the implement
evaluate_move like this in your Problem class:

.. code-block:: python

    def evaluate_move(self, move):

        self.move(move)
        new_value = self._evaluation_function.evaluate(self._order)
        self.undo_move(move)

        return new_value - self._evaluation_function.evaluate(self._order)

If you want to use this method with an existing problem class from this
library, it's the best to define your own subclass that overwrites the default
behaviour of the method and use this subclass:

.. code-block:: python

    class MyProblemClass(ImplementedProblemClass):
        def evaluate_move(self, move):

            self.move(move)
            new_value = self._evaluation_function.evaluate(self._order)
            self.undo_move(move)

            return new_value - self._evaluation_function.evaluate(self._order)

Do remember not to pass a move function to the evaluation function's
constructor if you use these approaches.
Also note that there will be a significant slowdown.

"""
