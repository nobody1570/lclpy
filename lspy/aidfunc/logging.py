

def log_improvement(value):
    """function to log improvements to the command line.

    Parameters
    ----------
    value : int or float
            The value for the improvement

    """

    print("Improvement : " + str(value))


def log_passed_worse(value):
    """function to log the passing of worse solutions to the command line.

    Parameters
    ----------
    value : int or float
            The value for the improvement

    """

    print("Passed worse: " + str(value))
