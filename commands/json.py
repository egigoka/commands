#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with JSON."""
from __future__ import annotations
from .module import LazyModule, LazyProperty

from typing import Any, Iterator, TYPE_CHECKING, cast
if TYPE_CHECKING:
    import json
    import os
    from typing import List, Mapping, Optional, Protocol, Union

    class Dict(Protocol):
        """Typing protocol for dictionary helpers."""

        @classmethod
        def all_keys_lambda(cls, input_dict: Mapping[Any, Any], function: Any) -> dict[Any, Any]:
            """Apply a function to every dictionary key."""
            ...
__version__ = "4.3.0"
if not TYPE_CHECKING:
    json = LazyModule("json")
    os = LazyModule("os")
Print = LazyProperty(".print", "Print")
File = LazyProperty(".file", "File")
if not TYPE_CHECKING:
    Dict = LazyProperty(".dict", "Dict")


class Json:
    """Class to work with JSON."""

    def __init__(
        self,
        filename: str,
        verbose: bool = False,
        ensure_ascii: bool = False,
        debug: bool = False
    ) -> None:
        self.filename = filename
        self.ensure_ascii = ensure_ascii
        self.verbose = verbose
        self.debug = debug
        self.string: Any = {}

        self.load(verbose=verbose)

    def __call__(
        self,
        key: Optional[Any] = None,
        value: Any = None,
        save: bool = False,
        default: Any = None
    ) -> Any:
        """Shortcut: no args returns data; key returns element or default; save=True persists current state."""
        if save:
            self.save(verbose=self.verbose, debug=self.debug)
            return self.string
        if key is None:
            return self.string
        try:
            return self.string[key]
        except Exception:  # KeyError/IndexError/TypeError
            return default

    def __len__(self) -> int:
        """Return number of stored items."""
        return len(self.string)

    def __contains__(self, item: Any) -> bool:
        """Return True if item exists in stored data."""
        return item in self.string

    def __repr__(self) -> str:
        """Return a pretty string representation."""
        pretty = Print.prettify(self.string, verbose=False)
        return f"JSON '{self.filename}':\n{pretty}"

    __print__ = __repr__

    def pop(self, *args: Any, **kwargs: Any) -> Any:
        """Remove and return an item from stored data."""
        output = self.string.pop(*args, **kwargs)
        return output

    def save(self, verbose: bool = False, debug: bool = False) -> None:
        """Save JSON data to disk.

        <br>`param verbose` boolean, suppress print to console
        <br>`param debug` boolean, needed for debugging
        <br>`return`
        """
        if debug:
            print(self.string)
        # try:
        File.wipe(self.filename)
        with open(self.filename, "w", encoding="utf8") as settings_json_text_io:

            if isinstance(self.string, dict):
                self.string = Dict.all_keys_lambda(self.string, str)  # make sure that all keys is strings

            json.dump(self.string, settings_json_text_io, ensure_ascii=self.ensure_ascii)
        if verbose:
            Print.multithread_safe("JSON successfully saved")

    def load(self, verbose: bool = False, debug: bool = False) -> None:
        """Load JSON data from disk.

        <br>`param verbose` suppress print to console
        <br>`param debug` boolean, needed for debugging
        <br>`return` None
        """
        if not os.path.isfile(self.filename):
            try:
                File.create(self.filename)
                self.string = {}
                self.save()
            except FileExistsError:  # if file created while this code running
                pass
        with open(self.filename, encoding="utf8") as file_handle:
            try:
                self.string = json.load(file_handle)
            except json.decoder.JSONDecodeError as e:
                empty_content = File.read(self.filename)
                if not empty_content:
                    self.string = {}
                else:
                    raise e
        if verbose:
            print("JSON successfully loaded")
        if debug:
            print(self.string)


class JsonDict(Json):
    """JSON-backed dictionary helper."""

    def __init__(self, filename: str, verbose: bool = False, ensure_ascii: bool = False, debug: bool = False) -> None:
        Json.__init__(self=self, filename=filename, verbose=verbose, ensure_ascii=ensure_ascii, debug=debug)
        if not isinstance(self.string, dict):
            raise TypeError(f"Json file {filename} is not containing dict")

    def __call__(
        self,
        key: Optional[Any] = None,
        value: Any = None,
        save: bool = False,
        default: Any = None
    ) -> Any:
        """Shortcut: without args returns dict; key/value sets; save persists."""
        if key is None and value is None and not save:
            return self.string
        if key is not None and value is not None:
            self.string[key] = value
        if save:
            self.save(verbose=self.verbose, debug=self.debug)
        if key is not None and value is None:
            return self.string.get(key, default)
        return self.string

    def __getitem__(self, item: Any) -> Any:
        """Return a value for the given key."""
        try:
            return self.string.__getitem__(item)
        except KeyError:
            info_string = f'''self={self}
self.string={self.string}")
item={item}
item not found!'''
            raise KeyError(info_string)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set a value for the given key."""
        self.string.__setitem__(key, value)

    def __iter__(self) -> Iterator[Any]:
        """Return an iterator over stored data."""
        return cast(Iterator[Any], iter(self.string))

    def __str__(self) -> str:
        """Return a prettified string representation."""
        return str(Print.prettify(self.string, verbose=False))

    def items(self) -> Any:
        """Return dictionary items."""
        return self.string.items()

    def values(self) -> Any:
        """Return dictionary values."""
        return self.string.values()

    def keys(self) -> Any:
        """Return dictionary keys."""
        return self.string.keys()

    def clear(self) -> Any:
        """Clear stored dictionary data."""
        return self.string.clear()


class JsonList(Json):
    """JSON-backed list helper."""

    __getitem__ = JsonDict.__getitem__
    __setitem__ = JsonDict.__setitem__

    def __init__(self, filename: str, verbose: bool = False, ensure_ascii: bool = False, debug: bool = False) -> None:
        Json.__init__(self=self, filename=filename, verbose=verbose, ensure_ascii=ensure_ascii, debug=debug)
        if self.string == {}:  # if it's empty (new) file
            self.string = []
            self.save()
        if not isinstance(self.string, list):
            raise TypeError(f"Json file {filename} is not containing list")

    def __call__(
        self,
        key: Optional[Any] = None,
        value: Any = None,
        save: bool = False,
        default: Any = None
    ) -> Any:
        """Shortcut: no args returns list; value appends then optionally saves."""
        if key is None and value is None and not save:
            return self.string
        if key is not None:
            self.append(key)
        elif value is not None:
            self.append(value)
        if save:
            self.save(verbose=self.verbose, debug=self.debug)
        return self.string

    def __str__(self) -> str:
        """Return a prettified string representation."""
        return str(Print.prettify(self.string, verbose=False))

    def index(self, *args: Any, **kwargs: Any) -> Any:
        """Return index of a list element."""
        output = self.string.index(*args, **kwargs)
        return output

    def append(self, element: Any) -> None:
        """Append an element to the list."""
        self.string.append(element)

    def sort(self, *args: Any, **kwargs: Any) -> None:
        """Sort the list in place."""
        self.string.sort(*args, **kwargs)

    def clear(self, *args: Any, **kwargs: Any) -> None:
        """Clear the list."""
        self.string.clear(*args, **kwargs)
