from locsearch.localsearch.abstract_local_search import AbstractLocalSearch
from locsearch.localsearch.acceptance.simulated_annealing_acceptance_function \
    import SimulatedAnnealingAcceptanceFunction
from collections import namedtuple


class SimulatedAnnealing(AbstractLocalSearch):
    """performs a simulated annealing algorithm."""

    def __init__(self, solution, termination_criterion,
                 cooling_function, iterations_for_temp_f,
                 start_temperature=1000):
        super().__init__()

        self._solution = solution
        self._termination_criterion = termination_criterion
        self._cooling_function = cooling_function
        self._iterations_for_temp_f = iterations_for_temp_f
        self._temperature = start_temperature
        self._acceptance_function = SimulatedAnnealingAcceptanceFunction()

    def run(self):

        base_value = self._solution.evaluate()
        self._solution.set_as_best(base_value)

        self._termination_criterion.start_timing()

        while self._termination_criterion.keep_running():

            # start iterations
            iterations = self._iterations_for_temp_f.get_iterations(
                self._temperature)

            while iterations > 0 and \
                    self._termination_criterion.keep_running():

                    # get and evaluate move
                move = self._solution.get_random_move()
                delta = self._solution.evaluate_move(move)

                # accept or reject move
                if delta <= 0:
                    self._solution.move(move)
                    base_value = base_value + delta
                    # check if best state
                    if base_value < self._solution.best_order_value:
                        self._solution.set_as_best(base_value)
                """else:
                    if self._acceptance_function.accept(
                            delta, self._temperature):

                        self._solution.move(move)
                        base_value = base_value + delta"""

                self._termination_criterion.iteration_done()
                iterations -= 1

            # cooling
            self._temperature = self._cooling_function.next_temperature(
                self._temperature)

            self._termination_criterion.check_variable(self._temperature)

        Results = namedtuple('Results', ['best_order', 'best_value'])

        return Results(self._solution.best_order,
                       self._solution.best_order_value)
