from locsearch.aidfunc.error_func import _not_implemented
from locsearch.localsearch.move.array_swap import ArraySwap
from locsearch.localsearch.move.tsp_array_swap import TspArraySwap
from locsearch.localsearch.move.array_reverse_order import ArrayReverseOrder


def get_move(move_type):
    """Aid func to return move classes.

    Currently only 3 move types are supported:

    +-------------------+---------------------+
    | Move              | move_type           |
    +===================+=====================+
    | ArraySwap         | array_swap          |
    +-------------------+---------------------+
    | TspArraySwap      | tsp_array_swap      |
    +-------------------+---------------------+
    | ArrayReverseOrder | array_reverse_order |
    +-------------------+---------------------+

    Parameters
    ----------
    move_type : str
        The name of the algorithm type.

    Returns
    -------
    AbstractMove
        The wanted move class. If the type is not found, a function that raises
        an NotImplementedError will be returned.

    """

    if move_type is 'array_swap':
        return ArraySwap
    elif move_type is 'tsp_array_swap':
        return TspArraySwap
    elif move_type is 'array_reverse_order':
        return ArrayReverseOrder
    else:
        return _not_implemented
