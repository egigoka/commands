#! python3
# -*- coding: utf-8 -*-
"""Internal module to help with bash."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import shlex
    from typing import List, Optional

from .module import LazyModule, LazyProperty

__version__ = "0.1.0"
Console = LazyProperty(".console", "Console")

if not TYPE_CHECKING:
    shlex = LazyModule("shlex")


class Bash:
    """Class to help with bash commands and argument escaping."""

    def __init__(self, command: str = "") -> None:
        self.command = command

    def run(self, pure_shell: bool = True) -> str:
        """Run the stored command and return output."""
        if not self.command:
            raise ValueError("No command to run")
        output = Console.get_output(self.command, pure_shell=pure_shell)
        return str(output)

    def __call__(self, pure_shell: bool = True) -> str:
        """Run the stored command and return output."""
        return self.run(pure_shell=pure_shell)

    def append(self, *args: str) -> "Bash":
        """Append escaped arguments to the command."""
        escaped = [shlex.quote(arg) for arg in args]
        if self.command:
            self.command = self.command + " " + " ".join(escaped)
        else:
            self.command = " ".join(escaped)
        return self

    def escape(self, argument: Optional[str] = None) -> str:
        """Escape an argument for safe shell usage using shlex."""
        if argument is None:
            return shlex.quote(self.command)
        return shlex.quote(argument)

    def split(self) -> List[str]:
        """Split the command into a list of arguments using shlex."""
        return shlex.split(self.command)
