
def _not_implemented(*not_used):
    """An error raising function that can take any amount of parameters.

    Parameters
    ----------
    *not_used
        Variable length argument list, it does not matter what or how many
        parameters you use.

    Raises
    ------
    NotImplementedError
        This error will always be raised.

    """
    raise NotImplementedError
