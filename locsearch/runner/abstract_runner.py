from abc import ABC, abstractmethod


class AbstractRunner(ABC):
    """Template to create runners.

    Runners are responsible for initializing and running an algorithm.
    I/O and, when needed, plotting data. Implementation can be easily done by
    inheriting from this class and implementing tha abstract methods. Use
    instance variables for data that needs to be remembered for use in other
    methods.

    Attributes
    ----------
    results : collections.namedtuple
        The results from the execution of the algorithm.

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def read(self, path):
        """Reads a file.

        Parameters
        ----------
        path : str
            The relative or absolute path to the file.

        """

        pass

    @abstractmethod
    def define_move_function(self):
        """Creating and initialising a move function."""

        pass

    @abstractmethod
    def define_evaluation_function(self):
        """Creating and initialising an evaluation function."""

        pass

    @abstractmethod
    def define_solution(self):
        """Creating and initialising a solution object."""

        pass

    def define_termination_criterion(self):
        """Creating and initialising a termination criterion, if needed.

        This function does not always need to be implemented.

        """

        pass

    @abstractmethod
    def define_algorithm(self):
        """Creating and initialising an AbstractLocalSearch instance."""

        pass

    @abstractmethod
    def run_algorithm(self):
        """Starts running the algorithm.

        Returns
        -------
        results : collections.namedtuple
            The results.
        """

        pass

    @abstractmethod
    def output(self):
        """Handles the output."""

        pass

    def run(self, path):
        """initializes and runs an instance of an AbstractLocalSearch class.

        Parameters
        ----------
        path : str
            The relative or absolute path to the file.

        """

        print('Starting runner...')
        # read data
        self.read(path)
        print('--- data read')

        # create move

        self.define_move_function()
        print('--- move function defined')

        # create evaluation function

        self.define_evaluation_function()
        print('--- evaluation function defined')

        # create and initialize solution

        self.define_solution()
        print('--- solution object defined')

        # if needed create and init termination criterion

        self.define_termination_criterion()
        print('--- termination criterion defined')

        # create instance of localsearch algorithm and set solution

        self.define_algorithm()
        print('--- algorithm defined')
        # get results from localsearch algorithm

        print('--- start running...')
        self.results = self.run_algorithm()
        print('--- ...running ended')

        # output
        self.output()
        print('--- output generated')
        print('... runner stopped')
