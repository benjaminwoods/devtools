"""
.. module: devtools.label._common

"""

from __future__ import annotations

from typing import Callable, Optional, Any, List, Dict, Iterable
from types import ModuleType

import warnings
from functools import wraps

from ._exceptions import RegistryWarning
from ._classes import _Registry, _LabelEnum

__all__ = ['register', 'getinfo', 'getinfomodule', 'getinfovars',
           'getinfoiter']

def register(*names: ...) -> Callable:
    """
    Decorates a callable (:code:`clb`) so that it appears in the devtools
    Registry.

    When the callable is called, it raises a RegistryWarning for each label.

    In addition, the callable can be found in the Registry if desired.

    Parameters
    ----------
    *names : ...
        Label names.

    Returns
    -------
    Callable
        A generic callable.

    """

    def _reg_callable(clb):
        @wraps(clb)
        def _inner(*args, **kwargs):
            # Raises a RegistryWarning for each label.

            if (reg[_inner] >> _LabelEnum['deprecated']) % 2:
                # Deprecated
                warnings.warn("Function is deprecated.", RegistryWarning)
            if (reg[_inner] >> _LabelEnum['pure']) % 2:
                # Deprecated
                warnings.warn("Function is pure.", RegistryWarning)
            if (reg[_inner] >> _LabelEnum['idempotent']) % 2:
                # Deprecated
                warnings.warn("Function is idempotent.", RegistryWarning)
            return clb(*args, **kwargs)

        # Get Registry
        reg = _Registry()

        # Warn if already registered
        if _inner in reg:
            warnings.warn(f"Callable ({clb.__name__}) already registered.")

        # Register clb
        reg[_inner] = sum(2**_LabelEnum[name] for name in names)

        return _inner
    return _reg_callable

def getinfo(clb: Callable, val: Optional[Any] = None) -> List[str]:
    """
    Get label info on a Callable, :code:`clb`.

    Parameters
    ----------
    clb : Callable
        A registered Callable.
    val : Optional[Any], optional
        If None, a KeyError is raised if :code:`clb` is not registered.
        Otherwise, return :code:`val`

        The default is None.

    Returns
    -------
    List[str]
        Labels.

    """

    reg = _Registry()

    try:
        info = reg.get_info(clb)
    except KeyError:
        if val is None:
            raise
        info = val 

    return info

def getinfovars(vs: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Get label info from a variables dictionary (i.e. vars, globals, locals).

    Returns a dictionary containing all of the Callable names and their
    labels.

    Parameters
    ----------
    module: ModuleType
        A module.

    Returns
    -------
    Dict[str, List[str]]
        Label info in a dictionary.

    """

    reg = _Registry()
    info = {}
    for item in vs.values():
        if callable(item):
            try:
                info[item.__name__] = reg.get_info(item)
            except KeyError:
                pass
    return info

def getinfomodule(module: ModuleType) -> Dict[str, List[str]]:
    """
    Get label info from a module.

    Returns a dictionary containing all of the Callable names and their
    labels.

    Parameters
    ----------
    module: ModuleType
        A module.

    Returns
    -------
    Dict[str, List[str]]
        Label info in a dictionary.

    """

    return getinfovars(vars(module))

def getinfoiter(iterable: Iterable) -> Dict[str, List[str]]:
    """
    Get label info from an Iterable.

    Returns a dictionary containing all of the Callable names and their
    labels.

    Parameters
    ----------
    module: ModuleType
        A module.

    Returns
    -------
    Dict[str, List[str]]
        Label info in a dictionary.

    """

    reg = _Registry()
    info = {}
    for item in iterable:
        if callable(item):
            try:
                info[item] = reg.get_info(item)
            except KeyError:
                pass
    return info
