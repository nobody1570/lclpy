import matplotlib.pyplot as plt


def plot(data):
    """Plots the data in a time-value plot.

    Parameters
    ----------
    data : collections.namedtuple
        The data tuple one gets by performing a localsearch algorithm.

    """

    # get the data from the data object
    time = data.time
    values = data.value

    plt.plot(time, values, label='value')

    if hasattr(data, 'best_value'):
        best_values = data.best_value

        plt.plot(time, best_values, label='best value found')

    plt.xlabel('time (s)')
    plt.ylabel('evaluation value')

    plt.title("Time - evaluation value plot.")

    plt.legend()

    plt.show()


def iterations_plot(data):
    """Plots the data in an iterations-value plot.

    Parameters
    ----------
    data : collections.namedtuple
        The data tuple one gets by performing a localsearch algorithm.

    """

    # get the data from the data object
    iterations = data.iteration
    values = data.value

    plt.plot(iterations, values, label='value')

    if hasattr(data, 'best_value'):
        best_values = data.best_value

        plt.plot(iterations, best_values, label='best value found')

    plt.xlabel('iterations')
    plt.ylabel('evaluation value')

    plt.title("Iterations - evaluation value plot.")

    plt.legend()

    plt.show()
