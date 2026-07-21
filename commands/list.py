#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with lists."""
from __future__ import annotations
from .module import LazyModule, LazyProperty

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import builtins
    import collections
    import copy
    import fnmatch
    import random
    from collections import OrderedDict
    from collections.abc import Iterable
    from operator import itemgetter
    from typing import Any, Callable, Dict, List as ListType, Optional, Sequence, Set, Tuple
__version__ = "0.10.3"
if not TYPE_CHECKING:
    copy = LazyModule("copy")
    fnmatch = LazyModule("fnmatch")
    collections = LazyModule("collections")
    random = LazyModule("random")
    builtins = LazyModule("builtins")
    OrderedDict = LazyProperty("collections", "OrderedDict")
    Iterable = LazyProperty("collections.abc", "Iterable")
    itemgetter = LazyProperty("operator", "itemgetter")


class List:
    """Class to work with lists."""

    data: Optional[ListType[Any]]

    def __getattribute__(self, name: str) -> Any:
        """Forward selected methods to stored list data."""
        instance_forward: Set[str] = {"flatterize", "split_every", "shuffle", "remove_duplicates"}
        if name in instance_forward:
            def _wrapper(*args: Any, **kwargs: Any) -> Any:
                self._ensure()
                data = self.data
                assert data is not None
                result = getattr(self.__class__, name)(data, *args, **kwargs)
                if name in {"flatterize", "shuffle", "remove_duplicates"}:
                    self.data = result
                return result
            return _wrapper
        return object.__getattribute__(self, name)

    def __init__(self, data: Optional[ListType[Any]] = None) -> None:
        self.data = data

    def _ensure(self) -> None:
        if self.data is None:
            raise ValueError("List data is not set")

    def __call__(self) -> Optional[ListType[Any]]:
        """Return underlying data for quick access."""
        return self.data

    @classmethod
    def flatterize(cls, input_list: Sequence[Any]) -> ListType[Any]:
        """Remove nesting from lists.

        <br>`param input_list` list
        <br>`return` list with all contents of input list but without nesting
        """
        if not isinstance(input_list, (list, tuple)):
            raise TypeError("object of type '" + str(type(input_list)) + "' can't be flatterized")
        output_list: ListType[Any] = copy.deepcopy(list(input_list))
        cnt = 0
        for object_ in output_list:
            if not isinstance(object_, (str, int, float)):
                output_list.pop(cnt)
                for item in reversed(object_):
                    output_list.insert(cnt, item)
            cnt += 1
        return output_list

    @classmethod
    def split_every(cls, list_input: ListType[Any], count: int) -> ListType[ListType[Any]]:
        """Split list into sublists of N elements.

        <br>`param list_input` list
        <br>`param count` int with N
        <br>`return` list of lists
        """
        count = int(count)
        if count == 0:
            return [[list_input[x]] for x in range(0, len(list_input))]
        elif count > len(list_input):
            return [list_input, ]
        output_lists = [list_input[x:x+count] for x in range(0, len(list_input), count)]
        # https://stackoverflow.com/questions/9671224/split-a-python-list-into-other-sublists-i-e-smaller-lists
        return output_lists  # todo отдебажить пограничные моменты

    @classmethod
    def wildcard_search(cls, list_input: Sequence[str], regexp: str) -> ListType[str]:
        """Search a list with shell-like wildcard patterns.

        <br>`param list_input` list
        <br>`param regexp` string with shell-like wildcards` ? for one character or * for multiple characters.
        <br>`return` list of result of search
        """
        return fnmatch.filter(list_input, regexp)

    @classmethod
    def replace_string(cls, list: Sequence[Any], old_string: str, new_string: str) -> ListType[str]:
        """Replace substrings in all list elements."""
        return [str(string).replace(old_string, new_string) for string in list]

    @classmethod
    def apply_lambda_to_all_elements(cls, list: Sequence[Any], function: Callable[[Any], Any]) -> ListType[Any]:
        """Apply a function to all list elements."""
        return [function(string) for string in list]

    @classmethod
    def to_strings(cls, list: Sequence[Any]) -> ListType[str]:
        """Convert all elements to strings."""
        return cls.apply_lambda_to_all_elements(list, str)

    @classmethod
    def remove_duplicates(cls, source_list: Sequence[Any], preserve_order: bool = True) -> ListType[Any]:
        """Remove duplicates from a list."""
        if preserve_order:
            return list(OrderedDict((x, True) for x in source_list).keys())
        else:
            return list(set(source_list))

    @classmethod
    def most_common(cls, list: Sequence[Any], count: int) -> ListType[Tuple[Any, int]]:
        """Return most common elements and their counts."""
        c = collections.Counter(list)
        return c.most_common(count)

    @classmethod
    def shuffle(cls, list: Sequence[Any]) -> ListType[Any]:
        """Return a shuffled copy of the list."""
        copy_list = copy.deepcopy(builtins.list(list))
        random.shuffle(copy_list)
        return copy_list

    @classmethod
    def remove_empty_strings(cls, list_: ListType[str]) -> ListType[str]:
        """Remove empty strings from a list."""
        list_new = list_.copy()
        for cnt, item in enumerate(list_new):
            if item == "":
                list_new.pop(cnt)
        return list_new

    @classmethod
    def itemgetter_with_casting(cls, item: Any, *items: Any, cast_to: Any) -> Callable[[Any], Any]:
        """Return an itemgetter with optional casting."""
        try:
            iter(cast_to)
        except TypeError:
            cast_to = (cast_to, )
        else:
            if isinstance(cast_to, str):
                cast_to = (cast_to, )

        if not items:
            def func(obj: Any) -> Any:
                for type_to in cast_to:
                    try:
                        return type_to(obj[item])
                    except:
                        pass
                return obj[item]
        else:
            items = (item,) + items

            def func(obj: Any) -> Any:
                new_list: ListType[Any] = []
                for i in items:
                    added = False
                    for type_to in cast_to:
                        try:
                            new_list.append(type_to(obj[i]))
                            added = True
                            break
                        except:
                            pass
                    if not added:
                        new_list.append(obj[i])
                return tuple(new_list)
        return func

    @classmethod
    def sort_by(cls, list_input: ListType[Any], *sort_keys: Any, cast_to: Any = ()) -> ListType[Any]:
        """Sort a list by one or more keys."""
        return sorted(list_input, key=cls.itemgetter_with_casting(*sort_keys, cast_to=cast_to))

    @classmethod
    def enum_by(cls, list_input: ListType[Any], *enum_keys: Any, cast_to: Any = ()) -> Dict[Any, Any]:
        """Return a dict keyed by selected fields."""
        new_dict: Dict[Any, Any] = {}
        for value in list_input:
            itemgetter_current = itemgetter(*enum_keys)
            key = itemgetter_current(value)

            for type_to in cast_to:
                try:
                    value = type_to(value)
                    break
                except:
                    pass

            new_dict[key] = value
        return new_dict
