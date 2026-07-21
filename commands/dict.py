#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with dicts."""
from __future__ import annotations

from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from ast import literal_eval
    from collections import OrderedDict
    from typing import Callable, Dict as DictType, ItemsView, Mapping, NoReturn, Optional, Tuple, Type, Union

    class _ImDictBase(dict[Any, Any]):
        pass
else:
    class _ImDictBase(dict):
        pass

from .module import LazyModule, LazyProperty

__version__ = "0.5.1"
if not TYPE_CHECKING:
    literal_eval = LazyProperty("ast", "literal_eval")
    OrderedDict = LazyProperty("collections", "OrderedDict")


class ImDict(_ImDictBase):
    """Rejected PEP 351."""

    def __hash__(self) -> int:  # type: ignore[override]
        """Return a hash based on object identity."""
        return id(self)

    def _immutable(self, *args: Any, **kws: Any) -> NoReturn:
        raise TypeError('object is immutable')

    def __setitem__(self, key: Any, value: Any) -> None:
        """Prevent setting items on immutable dict."""
        self._immutable()

    def __delitem__(self, key: Any) -> None:
        """Prevent deleting items on immutable dict."""
        self._immutable()

    def clear(self) -> None:
        """Prevent clearing an immutable dict."""
        self._immutable()

    def update(self, *args: Any, **kws: Any) -> None:
        """Prevent updating an immutable dict."""
        self._immutable()

    def setdefault(self, key: Any, default: Any = None) -> Any:
        """Prevent setting defaults on an immutable dict."""
        self._immutable()

    def pop(self, key: Any, default: Any = ...) -> Any:
        """Prevent popping values from an immutable dict."""
        self._immutable()

    def popitem(self) -> Tuple[Any, Any]:
        """Prevent popping items from an immutable dict."""
        self._immutable()


class Dict:
    """Class to work with dicts."""

    def __init__(self, data: Optional[DictType[Any, Any]] = None) -> None:
        self.data: DictType[Any, Any] = data if data is not None else {}

    def _ensure(self) -> None:
        if self.data is None:
            raise ValueError("Dict data is not set")

    def __getattribute__(self, name: str) -> Any:
        """Forward selected methods to stored dict data."""
        instance_forward = {"iterable", "isinstance_keys", "isinstance_values",
                            "all_keys_lambda", "all_values_lambda", "sorted_by_key"}
        if name in instance_forward:
            def _wrapper(*args: Any, **kwargs: Any) -> Any:
                self._ensure()
                method: Callable[..., Any] = object.__getattribute__(self.__class__, name).__get__(self, self.__class__)
                return method(self.data, *args, **kwargs)
            return _wrapper
        return object.__getattribute__(self, name)

    @classmethod
    def iterable(cls, dict_: DictType[Any, Any], copy_dict: bool = False) -> ItemsView[Any, Any]:
        """Return an iterable view of a dict.

        <br>`param dict_` input dict
        <br>`param copy_dict` bool, if True, return iterable copy of dict
        <br>`return` iterable dict
        """
        if not isinstance(dict_, dict):
            raise TypeError("There must be dict in input")
        if copy_dict:
            return dict_.copy().items()
        return dict_.items()

    @classmethod
    def str_lower_of_dict_key(cls, dict_item: Tuple[Any, Any]) -> str:
        """Return a lowercased key from a dict item."""
        return str.lower(dict_item[0])

    @classmethod
    def get_dict_key(cls, dict_item: Tuple[Any, Any]) -> Any:
        """Return the key from a dict item."""
        return dict_item[0]

    @classmethod
    def sorted_by_key(
        cls,
        dict_: DictType[Any, Any],
        case_insensitive: bool = False,
        func: Optional[Callable[[Tuple[Any, Any]], Any]] = None
    ) -> "OrderedDict[Any, Any]":
        """Return a dict sorted by key.

        <br>`param dict_` input dict
        <br>`param case_insensitive` sort dict insensitive
        <br>`return` OrderedDict
        """
        if func is None:
            if case_insensitive:
                func = cls.str_lower_of_dict_key
            else:
                func = cls.get_dict_key

        output: OrderedDict[Any, Any] = OrderedDict()
        for i in sorted(dict_.items(), key=func):
            output[i[0]] = i[1]
        return output

    @classmethod
    def from_str(cls, string: str) -> DictType[Any, Any]:
        """Create a dict from a string representation.

        <br>`param string` string
        <br>`return` dict
        """
        dict_ = literal_eval(string)
        assert isinstance(dict_, dict), f"Output must be dict, {type(dict_)} was found"
        return dict_

    @classmethod
    def isinstance_keys(cls, dict_: DictType[Any, Any], types: Union[Type[Any], Tuple[Type[Any], ...]]) -> bool:
        """Return True if all keys are instances of provided types."""
        for key, value in cls.iterable(dict_):
            if not isinstance(key, types):
                return False
        return True

    @classmethod
    def isinstance_values(cls, dict_: DictType[Any, Any], types: Union[Type[Any], Tuple[Type[Any], ...]]) -> bool:
        """Return True if all values are instances of provided types."""
        for key, value in cls.iterable(dict_):
            if not isinstance(value, types):
                return False
        return True

    @classmethod
    def all_keys_lambda(
        cls,
        dict_: DictType[Any, Any],
        func: Callable[..., Any],
        args: Tuple[Any, ...] = (),
        kwargs: Mapping[str, Any] = ImDict({})
    ) -> DictType[Any, Any]:
        """Apply a function to all keys and return a new dict."""
        output_dict: DictType[Any, Any] = {}
        for key, value in cls.iterable(dict_):
            output_dict[func(key, *args, **kwargs)] = value
        return output_dict

    @classmethod
    def all_values_lambda(
        cls,
        dict_: DictType[Any, Any],
        func: Callable[..., Any],
        args: Tuple[Any, ...] = (),
        kwargs: Mapping[str, Any] = ImDict({})
    ) -> DictType[Any, Any]:
        """Apply a function to all values and return a new dict."""
        output_dict: DictType[Any, Any] = {}
        for key, value in cls.iterable(dict_):
            output_dict[key] = func(value, *args, **kwargs)
        return output_dict
