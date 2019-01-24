
def insert_in_sorted_deque(sorted_deque, function, item):
    """Inserts an item in the correct position of an existing sorted deque.

    The deque is supposed to be sorted from worst (left) to best (right).
    Inserting item in an empty deque is possible.

    Parameters
    ----------
    sorted_deque : collections.deque
        The deque where an item will be inserted in.
    function
        A function that returns a bool that is used to sort the list.
    item
        The item one wishes to insert.

    Examples
    --------
    An example of inserting in a "smaller is better" deque:

    .. doctest::

        >>> from collections import deque
        >>> from locsearch.aidfunc.is_improvement_func import smaller
        >>> from locsearch.aidfunc.aid_deque import insert_in_sorted_deque
        >>> test = deque(reversed(range(0, 10, 2)))
        >>> test
        deque([8, 6, 4, 2, 0])
        >>> insert_in_sorted_deque(test, smaller, 5)
        >>> test
        deque([8, 6, 5, 4, 2, 0])

    An example of inserting in a "bigger is better" deque:

    .. doctest::

        >>> from collections import deque
        >>> from locsearch.aidfunc.is_improvement_func import bigger
        >>> from locsearch.aidfunc.aid_deque import insert_in_sorted_deque
        >>> test = deque(range(0, 10, 2))
        >>> test
        deque([0, 2, 4, 6, 8])
        >>> insert_in_sorted_deque(test, bigger, 5)
        >>> test
        deque([0, 2, 4, 5, 6, 8])

    """

    # find the first item in the deque that's better than the item we have

    insert_position = 0
    for deque_item in sorted_deque:

        if(function(item, deque_item)):
            break

        insert_position += 1

    # insert the item
    sorted_deque.insert(insert_position, item)
