"""
..module: devtools.testing
"""

from __future__ import annotations

from typing import (Callable, Any, Iterable, Optional, Dict, List, Tuple,
                    get_type_hints)
from inspect import getfullargspec

def check_properties(obj: Any,
                     gettable_props: Iterable[str] = [],
                     settable_props: Iterable[str] = [],
                     dettable_props: Iterable[str] = [],
                     slots: Optional[Iterable[str]] = None) -> None:
    """
    Check properties of an object, :code:`obj`.

    Parameters
    ----------
    obj : Any
        Any object.
    gettable_props : Iterable[str], optional
        Gettable properties.

        The default is [].
    settable_props : Iterable[str], optional
        Settable properties.

        The default is [].
    dettable_props : Iterable[str], optional
        Deletable properties.

        The default is [].
    slots : Iterable[str], optional
        Deletable properties.

        The default is None.

    Returns
    -------
    None.

    """

    # Check slots
    if slots is not None:
        assert hasattr(obj, '__slots__')
        assert not hasattr(obj, '__dict__')
        assert obj.__slots__ == slots
    else:
        assert not hasattr(obj, '__slots__')
        assert hasattr(obj, '__dict__')

    # All props
    props = set(gettable_props + settable_props + dettable_props)

    for prop in props:
        assert hasattr(obj, prop)

        # Gettable
        try:
            p_ = getattr(obj, prop)
        except AttributeError:
            if prop in gettable_props:
                raise AssertionError

        # Settable
        try:
            setattr(obj, prop, p_)
        except AttributeError:
            if prop in settable_props:
                raise AssertionError

        # Dettable
        try:
            delattr(obj, prop)
        except AttributeError:
            if prop in dettable_props:
                raise AssertionError

def check_signature(clb: Callable,
                    annotations: Dict[str, Any] = {},
                    args: List[str] = [],
                    defaults: Optional[Tuple[Any]] = None,
                    varargs: Optional[str] = None,
                    varkw: Optional[str] = None,
                    kwonlyargs: List[str] = [],
                    kwonlydefaults: Optional[Tuple[Any]] = None) -> None:    
    """
    Check signature of a Callable, :code:`clb`.


    Parameters
    ----------
    clb : Callable
        DESCRIPTION.
    annotations : Dict[str, Any], optional
        Evaluated type hints.

        To be specified as {str: Any} rather than {str: str} (after
        evaluation).

        The default is {}.
    args : List[str], optional
        Positional arguments.

        The default is [].
    varargs : Optional[str], optional
        Handle for the variable positional arguments.

        The default is None.
    varkw : Optional[str], optional
        Handle for the variable keyword arguments.

        The default is None.
    kwonlyargs : List[str], optional
        Keyword-only arguments.

        The default is [].
    kwonlydefaults : Optional[Tuple[Any]], optional
        Defaults for keyword-only arguments.

        The default is None.

    Returns
    -------
    None.

    """
    
    
    # Get full arg spec
    gfas = getfullargspec(clb)

    # PEP 563 compliant
    assert annotations == get_type_hints(clb)

    for attr in ['annotations', 'args', 'varargs', 'varkw', 'defaults',
                 'kwonlyargs', 'kwonlydefaults']:
        assert getattr(gfas, attr) == locals()[attr]
