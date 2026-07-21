#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for managing processes."""
from __future__ import annotations
from .module import LazyModule, LazyProperty

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Optional, Union, cast
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value
__version__ = "2.0.0"
OS = LazyProperty(".os", "OS")
Console = LazyProperty(".console", "Console")


class Process:
    """Class with functions for managing processes."""

    def __init__(self, target: Optional[Union[str, int]] = None) -> None:
        self.target = target

    def _ensure(self) -> None:
        if self.target is None:
            raise ValueError("Process target is not set")

    def __call__(self, target: Optional[Union[str, int]] = None) -> Any:
        """Set target if provided, otherwise kill stored target."""
        if target is not None:
            self.target = target
            return self
        return self.kill_target()

    def kill_target(self) -> Any:
        """Kill the currently stored target."""
        self._ensure()
        target = self.target
        assert target is not None
        return self.__class__.kill(target)

    @classmethod
    def kill(cls, process: Union[str, int]) -> Any:
        """Terminate a process by name or PID.

        <br>`param process` process name or PID
        <br>`return` None
        """
        process_str = str(process)
        if OS.windows:
            try:
                int(process_str)
                command_ = "taskkill /f /pid " + process_str
            except ValueError:
                if not process_str.endswith(".exe"):
                    process_str = process_str + ".exe"
                command_ = "taskkill /f /im " + process_str
        elif OS.unix_family:
            command_ = "killall " + process_str
            try:
                int(process_str)
                command_ = "kill " + process_str
            except ValueError:
                pass
        else:
            raise NotImplementedError("OS not supported, now only Windows and unix-like")
        return Console.get_output(command_)

    @classmethod
    def start(
        cls,
        *command: Any,
        pureshell: bool = False,
        pure_shell: Optional[bool] = None,
        print_std: bool = False,
        **kwargs: Any
    ) -> Any:
        """Run a command and return its output (small helper used across the project)."""
        if pure_shell is None:
            pure_shell = pureshell
        if len(command) == 1:
            command = command[0]
        return Console.get_output(command, pure_shell=pure_shell, print_std=print_std, **kwargs)
