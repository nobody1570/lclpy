from collections import deque


class TabuList(object):
    """Implements a tabu list for use with TabuSearch.

    Note that only hashes of the items are kept in the tabu list. This is done
    to save memory.

    Parameters
    ----------
    length : int
        The maximal amount of items in the tabu list.

    Attributes
    ----------
    _list : deque
        A list that contains hashes of all the items that are considered part
        of the tabu list.

    Examples
    --------
    A simple example, the lists are converted to tuples, because they're
    mutable objects and thus can't be hashed with the default implementation of
    hash:

    .. doctest::

        >>> from locsearch.localsearch.tabusearch.tabu_list import TabuList
        >>> test = TabuList(3)
        >>> test.add(tuple([0, 1, 2]))
        >>> test.add(tuple([1, 0, 2]))
        >>> test.add(tuple([0, 2, 1]))
        >>> test.add(tuple([2, 1, 0]))
        >>> test.contains(tuple([0, 1, 2]))
        False
        >>> test.contains(tuple([1, 0, 2]))
        True
        >>> test.contains(tuple([0, 2, 1]))
        True
        >>> test.contains(tuple([2, 1, 0]))
        True

    """

    def __init__(self, length):
        super().__init__()
        self._list = deque(maxlen=length)

    def add(self, item):
        self._list.append(hash(item))

    def contains(self, item):
        return hash(item) in self._list
