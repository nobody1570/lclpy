from collections import deque


class TabuList(object):
    """Implements a tabu list for use with TabuSearch.

    When using big items, it would be wise to save space by hashing them.

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

        >>> from lclpy.localsearch.tabusearch.tabu_list import TabuList
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
        """Adds an item to the tabu list.

        Parameters
        ----------
        item
            A hashable, immutable object.

        """

        self._list.append(item)

    def contains(self, item):
        """A method that checks if an item is in the tabu list.

        Parameters
        ----------
        item
            A hashable, immutable object.

        Returns
        -------
        bool
            Will return true if the item is in the tabu list, false if it
            isn't in the tabu list.

        """
        return item in self._list
