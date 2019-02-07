
def _not_implemented(*args):
    """An error raising function that can take any amount of parameters.

    Parameters
    ----------
    args
        Variable length argument list, it does not matter what or how many
        parameters you use. Does not accept keyword arguments.

    Raises
    ------
    NotImplementedError
        This error will always be raised.

    """
    raise NotImplementedError
