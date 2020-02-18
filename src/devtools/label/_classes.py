"""
..module: devtools.label._classes
"""

from __future__ import annotations

from typing import Callable, List, Iterator

from enum import IntEnum
from collections.abc import MutableMapping

__all__ = ['_Registry', '_LabelEnum']

class _Registry(MutableMapping):
    """
    An singleton class which holds information about labelled callables.
    """

    __slots__ = ['__data']
    __cache = {}
    def __new__(cls: type, *args: ..., **kwargs: ...) -> _Registry:
        """
        New instance.

        Parameters
        ----------
        cls : type
            Class or metaclass.
        *args : ...
            Instantiation positional arguments.
        **kwargs : ...
            Instantiation keyword arguments.

        Returns
        -------
        _Registry
            Instance of _Registry, or a subclass.

        """

        if cls not in cls.__cache:
            cls.__cache[cls] = super(_Registry, cls).__new__(cls,
                                                             *args, **kwargs)
            cls.__cache[cls].__data = {}

        return cls.__cache[cls]

    def __getitem__(self: _Registry, item: Callable) -> int:
        """
        Get binary representation of a Callable's labels.

        Parameters
        ----------
        item : Callable
            A callable.

        Returns
        -------
        int
            Binary representation of the Callable's labels.

        """

        return self.__data[item]

    def __setitem__(self: _Registry, clb: Callable, val: int) -> None:
        """
        Set binary representation of a Callable's labels.

        Parameters
        ----------
        clb : Callable
            A callable.
        val : int
            Binary representation of the Callable's labels.

        Returns
        -------
        None.

        """

        self.__data[clb] = val

    def __delitem__(self: _Registry, clb: Callable) -> None:
        """
        Remove a Callable from the Registry.

        Parameters
        ----------
        clb : Callable
            A callable.

        Returns
        -------
        None.

        """

        del self.__data[clb]

    def __iter__(self: _Registry) -> Iterator[Callable]:
        """
        Iterate through the Registry.

        Returns
        -------
        Iterator[Callable]
            The iterator.

        """

        return iter(self.__data)

    def __len__(self: _Registry) -> int:
        """
        Registry length.

        Returns
        -------
        int
            The length.

        """

        return len(self.__data)

    def __repr__(self: _Registry) -> str:
        """
        String representation of the Registry.

        Identical to the dictionary representation of the underlying data.

        Returns
        -------
        str
            The string representation.

        """

        return repr(self.__data)

    def get_info(self: _Registry, clb: Callable) -> List[str]:
        """
        Convert binary representation of a Callable :code:`clb` that appears
        in the Registry.

        Parameters
        ----------
        clb : Callable
            A callable.

        Raises
        ------
        ValueError
            If :code:`clb` is not callable, raise a ValueError.
        KeyError
            If :code:`clb` is not in the Registry, raise a KeyError.

        Returns
        -------
        List[str]
            List of labels.

        """

        if not callable(clb):
            raise ValueError('clb must be callable.')
        try:
            n = self.__data[clb]
        except KeyError:
            if hasattr(clb, '__name__'):
                raise KeyError(f'Callable ({clb.__name__}) not in Registry.')

            raise KeyError(f'Callable not in Registry.')

        # Convert from binary to labels using _LabelEnum.
        labels = []
        c = 0
        while n > 0:
            if n % 2:
                labels.append(_LabelEnum(c).name)
            n >>= 1
            c += 1

        return labels

class _LabelEnum(IntEnum):
    """
    A simple enumerate class to hold the labels.
    """

    deprecated = 0
    pure = 1
    idempotent = 2
