
def _not_implemented(*args):
    """An error raising function that can take any amount of parameters.

    Parameters
    ----------
    *args
        Variable length argument list, it does not matter what or how many
        parameters you use. Does not accept keyword arguments.

    Raises
    ------
    NotImplementedError
        This error will always be raised.

    """

    raise NotImplementedError


class WrongMoveType(Exception):
    """Is raised when the wrong move type is used."""
    pass


def not_multi_move_type(*args):
    """An error raising function that can take any amount of parameters.

    Parameters
    ----------
    *args
        Variable length argument list, it does not matter what or how many
        parameters you use. Does not accept keyword arguments.

    Raises
    ------
    WrongMoveType
        This error will always be raised.

    """

    raise WrongMoveType('This method requires you to use an object of the '
                        'MultiNeighbourhood class as the move_function.')
